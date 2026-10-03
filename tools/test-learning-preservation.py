"""Preserve original content, allowing only exact separately-reviewed revisions.

The original baseline is immutable. Any approved amendment records both its
original digest and exact reviewed replacement; unrelated edits still fail.
"""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
baseline = json.loads((root/'reviews/learning-original-content-baseline.json').read_text())
revision_path = root/'reviews/report-revision-preservation.json'
revision = json.loads(revision_path.read_text()) if revision_path.exists() else {'anchors': []}
approved = {row['id']: row for row in revision['anchors']}
assert len(approved) == len(revision['anchors']), 'Duplicate approved amendment'
assert set(approved) <= {r['id'] for r in baseline['anchors']}

def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()

for row in baseline['anchors']:
    source = (root/row['path']).read_text()
    meta, body = source[8:].split('\n---\n', 1)
    canonical = json.dumps(json.loads(meta), sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    original = body.split('<details class="advanced-reading">', 1)[1].split('</summary>', 1)[1].strip()
    assert original.endswith('</details>'), row['id']+': missing final disclosure close'
    original = original[:-len('</details>')].strip()
    amendment = approved.get(row['id'])
    for field, actual in [('metadata_sha256', digest(canonical)), ('original_body_sha256', digest(original))]:
        expected = row[field]
        if amendment and field in amendment:
            change = amendment[field]
            assert change['before'] == expected and change['before'] != change['after']
            assert amendment['reason'].strip() and amendment['review'].strip()
            expected = change['after']
        assert actual == expected, row['id']+': unreviewed change to '+field
print(f'Original lesson preservation: {len(baseline["anchors"])} exact anchors; {len(approved)} narrowly reviewed amendments; immutable base {baseline["base_commit"]}')
# New bridges wrap the previously published lesson verbatim; their new on-ramp
# sits before the disclosure, so no old proof or exercise can silently disappear.
bridges = revision.get('new_bridges', [])
if bridges:
    assert {b['id'] for b in bridges} == {'calculus-02','calculus-04','linear-algebra-05','linear-algebra-06'}
    for bridge in bridges:
        body = (root/bridge['path']).read_text()[8:].split('\n---\n',1)[1]
        original = body.split('<details class="advanced-reading">',1)[1].split('</summary>',1)[1].strip()
        for boundary in ['return-open:end','return-close:start','return-close:end']:
            marker = '<!-- math-revision-20261003:'+bridge['id']+'-'+boundary+' -->'
            assert original.count(marker) == 1, bridge['id']+': wrapper marker mismatch'
            original = original.replace(marker, '').strip()
        assert original.endswith('</details>')
        assert digest(original[:-len('</details>')].strip()) == bridge['original_body_sha256'], bridge['id']+': wrapped original content changed'
    print('New mathematics bridges: four original bodies preserved exactly inside the reading layer')
