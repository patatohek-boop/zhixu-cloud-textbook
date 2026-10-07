"""Auditable 1.5.0 -> 1.6.0 content preservation, independent of reader wrappers.

The immutable baseline is extracted from the published 1.5.0 source archive.
Reports never approve differences. Missing or changed features require an exact
before/after disposition with a human-readable reason. A reviewed-source digest
is a snapshot boundary, not a proof of mathematical correctness.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'reviews/reader-baseline-1.5.0.json'
PLAN = ROOT / 'reviews/reader-revision-1.6.0.json'
REPORT = ROOT / 'work/reader-revision-diff.json'
BASE_COMMIT = 'da07805e018e32e091476d13a94b19c64c4b3a9b'
HISTORICAL = [
    'reviews/learning-original-content-baseline.json',
    'reviews/report-revision-preservation.json',
    'reviews/report-revision-2026-10-03.json',
]
KINDS = ('code', 'display_math', 'inline_math', 'images')


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode('utf-8')).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def parse(source):
    assert source.startswith('---json\n'), 'Unsupported lesson metadata'
    metadata, body = source[8:].split('\n---\n', 1)
    return json.loads(metadata), body


def features(body):
    """Extract exact code and TeX tokens; normalize line breaks, not algebra.

    Multiplicities are retained, so removing a duplicated introductory formula
    still appears explicitly in the report. Equivalence of different formulas
    is never inferred by this script. All fenced blocks are checked, including
    pseudocode or console examples, which is stronger than runnable code alone.
    """
    code = []
    def take_code(match):
        code.append(match.group(1).strip().lower() + '\n' + match.group(2).strip('\n'))
        return '\n'
    prose = re.sub(r'^```([^\n]*)\n(.*?)^```\s*$', take_code, body, flags=re.M | re.S)
    # Dollar signs inside inline code are not mathematical delimiters.
    prose = re.sub(r'`[^`\n]*`', '', prose)
    display = []
    def take_math(match):
        display.append(re.sub(r'\s+', ' ', match.group(1)).strip())
        return '\n'
    prose = re.sub(r'\$\$(.*?)\$\$', take_math, prose, flags=re.S)
    inline = [re.sub(r'\s+', ' ', x).strip() for x in re.findall(r'(?<![\\$])\$(?!\$)([^\n]*?)(?<!\\)\$(?!\$)', prose)]
    images = re.findall(r'!\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', body)
    images += re.findall(r'<img\b[^>]*\bsrc=[\"\']([^\"\']+)', body, flags=re.I)
    result = {}
    for kind, values in zip(KINDS, (code, display, inline, images)):
        counts = Counter(values)
        result[kind] = {sha(text): {'text': text, 'count': count} for text, count in sorted(counts.items())}
    return result


def lesson_record(path, source):
    metadata, body = parse(source)
    return {'id': metadata['id'], 'path': path, 'source_sha256': sha(source),
            'quiz': metadata['quiz'], 'features': features(body)}


def metadata_digest(path):
    metadata, _ = parse((ROOT / path).read_text(encoding='utf-8'))
    return sha(json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(',', ':')))


def extract_baseline(archive):
    """Create once. Repeating extraction must reproduce the identical file."""
    archive = Path(archive)
    with zipfile.ZipFile(archive) as z:
        prefix = z.namelist()[0]
        assert BASE_COMMIT in prefix, 'Archive is not the exact published 1.5.0 commit'
        def text(path):
            return z.read(prefix + path).decode('utf-8').replace('\r\n', '\n')
        assert json.loads(text('version.json'))['version'] == '1.5.0'
        names = sorted(n[len(prefix):] for n in z.namelist() if re.fullmatch(re.escape(prefix) + r'content/[^/]+/[^/]+\.md', n))
        lessons = [lesson_record(n, text(n)) for n in names]
        assert len(lessons) == len({l['id'] for l in lessons}) == 253
        images = sorted({v['text'] for l in lessons for v in l['features']['images'].values()})
        result = {'schema': 1, 'version': '1.5.0', 'commit': BASE_COMMIT,
                  'archive_sha256': sha(archive.read_bytes()), 'lessons': lessons,
                  'image_files': {p: sha(z.read(prefix + 'site/' + p)) for p in images if p.startswith('assets/')},
                  'historical_manifests': {p: sha(z.read(prefix + p)) for p in HISTORICAL}}
    if BASE.exists():
        assert read_json(BASE) == result, 'Immutable reader baseline would change'
    else:
        write_json(BASE, result)
    return result


def current_lessons():
    return [lesson_record(p.relative_to(ROOT).as_posix(), p.read_text(encoding='utf-8'))
            for p in sorted((ROOT / 'content').glob('*/*.md'))]


def diff(base):
    current = current_lessons()
    before = {row['id']: row for row in base['lessons']}
    after = {row['id']: row for row in current}
    assert len(after) == len(current), 'Duplicate current lesson ID'
    changes = []
    for lesson_id in sorted(before.keys() & after.keys()):
        old, new = before[lesson_id], after[lesson_id]
        for kind in KINDS:
            for token in sorted(old['features'][kind].keys() | new['features'][kind].keys()):
                a, b = old['features'][kind].get(token), new['features'][kind].get(token)
                old_count, new_count = a['count'] if a else 0, b['count'] if b else 0
                if old_count != new_count:
                    changes.append({'id': lesson_id, 'kind': kind, 'sha256': token,
                                    'before_count': old_count, 'after_count': new_count,
                                    'text': (a or b)['text']})
    return {'version': '1.6.0', 'baseline_commit': base['commit'],
            'missing_ids': sorted(before.keys() - after.keys()), 'added_ids': sorted(after.keys() - before.keys()),
            'quiz_changes': [k for k in sorted(before.keys() & after.keys()) if before[k]['quiz'] != after[k]['quiz']],
            'path_changes': [k for k in sorted(before.keys() & after.keys()) if before[k]['path'] != after[k]['path']],
            'feature_changes': changes,
            'source_changes': [{'id': k, 'path': before[k]['path'], 'before_sha256': before[k]['source_sha256'], 'after_sha256': after[k]['source_sha256']}
                               for k in sorted(before.keys() & after.keys()) if before[k]['source_sha256'] != after[k]['source_sha256']]}


def change_key(change):
    return (change['id'], change['kind'], change['sha256'])


def snapshot_paths():
    # Source only: generated data, historical downloads, and test outputs are excluded.
    paths = set((ROOT / 'content').rglob('*.md')) | set((ROOT / 'content').rglob('*.json'))
    paths |= set((ROOT / 'site/assets').glob('*.js')) | set((ROOT / 'site/assets').glob('*.css'))
    paths -= {ROOT / 'site/assets/data.js'}
    paths |= {ROOT / 'version.json', ROOT / 'site/index.html'}
    paths |= set((ROOT / 'site/assets/diagrams').glob('*.svg'))
    paths |= set((ROOT / 'reviews/content-audit-2026-09').glob('*.json'))
    return sorted(p.relative_to(ROOT).as_posix() for p in paths if p.is_file())


def check_changes(base, plan, report):
    assert not report['missing_ids'] and not report['added_ids'], 'Original 253 lesson IDs changed'
    assert not report['path_changes'], 'Original lesson paths changed'
    assert not report['quiz_changes'], 'Original quiz payload changed: ' + ', '.join(report['quiz_changes'])
    assert plan['version'] == '1.6.0' and plan['baseline_commit'] == BASE_COMMIT
    assert plan['baseline_sha256'] == sha(BASE.read_bytes()), 'Reader baseline digest changed'
    for path, expected in base['historical_manifests'].items():
        assert sha((ROOT / path).read_bytes()) == expected, 'Historical baseline modified: ' + path
    for path, expected in base['image_files'].items():
        assert (ROOT / 'site' / path).is_file() and sha((ROOT / 'site' / path).read_bytes()) == expected, 'Published image changed: ' + path
    # Exact per-feature dispositions are mandatory even for added formulas/code.
    approvals = plan['feature_dispositions']
    assert len({change_key(c) for c in approvals}) == len(approvals), 'Duplicate feature disposition'
    actual = {change_key(c): c for c in report['feature_changes']}
    assert {change_key(c) for c in approvals} == set(actual), 'Unreviewed or stale feature changes; run --report'
    for approved in approvals:
        change = actual[change_key(approved)]
        assert all(approved[k] == change[k] for k in ('before_count', 'after_count', 'text')), 'Feature disposition no longer matches: ' + str(change_key(change))
        assert approved.get('reason', '').strip() and approved.get('review', '').strip(), 'Feature change lacks a concrete review reason'
        for reference in approved.get('evidence_files', []):
            assert (ROOT / reference).is_file(), 'Missing review evidence: ' + reference
    assert plan.get('scope_explanation', '').strip(), 'Missing narrative scope explanation'
    assert plan.get('review_notes'), 'Missing substantive review references'
    for path in plan['review_notes']:
        assert (ROOT / path).is_file(), 'Review report missing: ' + path


def verify(require_frozen=True):
    if read_json(ROOT / 'version.json')['version'] == '1.6.1':
        from verify_patch_release import verify_patch
        return verify_patch()
    base, plan = read_json(BASE), read_json(PLAN)
    report = diff(base)
    check_changes(base, plan, report)
    if require_frozen:
        assert plan['status'] == 'reviewed', '1.6.0 review is still draft; final source snapshot has not been approved'
        expected = {row['path']: row['sha256'] for row in plan['reviewed_files']}
        assert len(expected) == len(plan['reviewed_files']), 'Duplicate reviewed source path'
        assert set(expected) == set(snapshot_paths()), 'Reviewed source inventory differs'
        for path, digest in expected.items():
            assert sha((ROOT / path).read_bytes()) == digest, 'Source changed after 1.6.0 review: ' + path
        mapping = plan['lesson_mapping']
        current = {row['id']: row for row in current_lessons()}
        assert len(mapping) == 253 and {row['id'] for row in mapping} == set(current), 'Incomplete 253-lesson revision mapping'
        original = {row['id']: row for row in base['lessons']}
        for row in mapping:
            assert row['path'] == original[row['id']]['path'] == current[row['id']]['path']
            assert row['before_sha256'] == original[row['id']]['source_sha256']
            assert row['after_sha256'] == current[row['id']]['source_sha256'], 'Lesson mapping became stale: ' + row['id']
            assert row['after_metadata_sha256'] == metadata_digest(row['path']), 'Reviewed metadata changed: ' + row['id']
    counts = {kind: sum(v['count'] for row in base['lessons'] for v in row['features'][kind].values()) for kind in KINDS}
    print('Reader revision: 253 IDs and quizzes preserved; baseline features ' + str(counts)
          + '; ' + str(len(report['feature_changes'])) + ' exact reviewed feature dispositions; immutable 1.5.0 baselines checked')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract-baseline', type=Path)
    parser.add_argument('--report', action='store_true', help='Write differences only; never approve or freeze them')
    parser.add_argument('--freeze-reviewed', action='store_true', help='After editorial approval, validate explicit dispositions and freeze current source hashes')
    args = parser.parse_args()
    if args.extract_baseline:
        extract_baseline(args.extract_baseline)
        print('Immutable 1.5.0 feature baseline extracted and verified')
    if args.report:
        report = diff(read_json(BASE))
        write_json(REPORT, report)
        print(f'Draft report: {len(report["source_changes"])} changed lessons, {len(report["feature_changes"])} feature differences; {len(report["quiz_changes"])} changed quizzes; {REPORT}')
        return
    if args.freeze_reviewed:
        assert read_json(ROOT / 'version.json')['version'] == '1.6.0', 'Historical 1.6.0 snapshot cannot be re-frozen for a patch'
        # This option never invents approvals or reasons for differing features.
        verify(require_frozen=False)
        plan = read_json(PLAN)
        plan['status'] = 'reviewed'
        plan['reviewed_files'] = [{'path': p, 'sha256': sha((ROOT / p).read_bytes())} for p in snapshot_paths()]
        original = {row['id']: row for row in read_json(BASE)['lessons']}
        plan['lesson_mapping'] = [{'id': row['id'], 'path': row['path'],
                                   'before_sha256': original[row['id']]['source_sha256'],
                                   'after_sha256': row['source_sha256'],
                                   'after_metadata_sha256': metadata_digest(row['path'])} for row in current_lessons()]
        write_json(PLAN, plan)
    if not args.extract_baseline or args.freeze_reviewed:
        verify()


if __name__ == '__main__':
    main()
