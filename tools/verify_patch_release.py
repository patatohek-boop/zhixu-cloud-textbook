"""Verify the exact 1.6.1 errata against the immutable 1.6.0 source snapshot.

A patch permits only the nine declared source/metadata files. It does not
re-freeze unrelated text or replace the earlier review and preservation records.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    'content/fluid-mechanics/fluid-mechanics-03.md',
    'content/fluid-mechanics/fluid-mechanics-40.md',
    'content/machine-learning/machine-learning-11.md',
    'content/machine-learning/machine-learning-39.md',
    'site/assets/cfd-labs.js',
    'reviews/content-audit-2026-09/fluid-mechanics.json',
    'reviews/content-audit-2026-09/machine-learning.json',
    'version.json',
    'site/index.html',
}
BASELINE_SHA = '0774a1aa9d90cdcf95e6f61cd78952675ee8f69cf572e81ff942d23147da3503'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_patch():
    from verify_reader_revision import snapshot_paths, metadata_digest
    prior_path = ROOT / 'reviews/reader-revision-1.6.0.json'
    assert sha(prior_path.read_bytes()) == BASELINE_SHA, 'Historical 1.6.0 review changed'
    prior = json.loads(prior_path.read_text(encoding='utf-8'))
    patch = json.loads((ROOT / 'reviews/errata-1.6.1.json').read_text(encoding='utf-8'))
    assert patch['version'] == '1.6.1' and patch['baseline_version'] == '1.6.0'
    assert patch['baseline_commit'] == '376813bdf1600f8f086e3647339b523c7fdf357e'
    assert patch['baseline_manifest_sha256'] == BASELINE_SHA
    assert patch['status'] == 'reviewed', 'Exact errata source review is not complete'
    amendments = {r['path']: r for r in patch['files']}
    assert len(amendments) == len(patch['files']) and set(amendments) == ALLOWED
    expected = {r['path']: r['sha256'] for r in prior['reviewed_files']}
    assert len(expected) == len(prior['reviewed_files'])
    assert set(expected) == set(snapshot_paths()), 'Source inventory changed beyond errata'
    for path, digest in expected.items():
        if path in amendments:
            row = amendments[path]
            assert row['before_sha256'] == digest and row['after_sha256'] != digest
            assert row['reason'].strip()
            digest = row['after_sha256']
        assert sha((ROOT / path).read_bytes()) == digest, 'Unreviewed patch change: ' + path
    # In particular, no quiz, lesson ID, prerequisite, or other lesson metadata changes.
    assert len(prior['lesson_mapping']) == 253
    for row in prior['lesson_mapping']:
        assert metadata_digest(row['path']) == row['after_metadata_sha256'], row['id']
    base_path = ROOT / 'reviews/reader-baseline-1.5.0.json'
    assert sha(base_path.read_bytes()) == prior['baseline_sha256']
    base = json.loads(base_path.read_text(encoding='utf-8'))
    for path, digest in base['historical_manifests'].items():
        assert sha((ROOT / path).read_bytes()) == digest, 'Historical baseline changed: ' + path
    print(f'1.6.1 errata: {len(ALLOWED)} exact amended files; all other {len(expected)-len(ALLOWED)} frozen files and 253 lesson metadata records unchanged')
    return patch


if __name__ == '__main__':
    verify_patch()
