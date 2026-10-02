"""Check original proofs, exercises, IDs and metadata survive beginner-layer authoring."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
baseline=json.loads((root/'reviews/learning-original-content-baseline.json').read_text())
for row in baseline['anchors']:
    source=(root/row['path']).read_text();meta,body=source[8:].split('\n---\n',1)
    def digest(value):return hashlib.sha256(value.encode()).hexdigest()
    canonical=json.dumps(json.loads(meta),sort_keys=True,ensure_ascii=False,separators=(',',':'))
    assert digest(canonical)==row['metadata_sha256'],row['id']+': original lesson metadata changed'
    original=body.split('<details class="advanced-reading">',1)[1].split('</summary>',1)[1].strip()
    assert original.endswith('</details>'),row['id']+': missing final disclosure close'
    original=original[:-len('</details>')].strip()
    assert digest(original)==row['original_body_sha256'],row['id']+': an original proof, example or exercise was altered or dropped'
print(f'Original lesson preservation: all {len(baseline["anchors"])} metadata and complete original bodies unchanged from {baseline["base_commit"]}')
