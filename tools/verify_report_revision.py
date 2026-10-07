"""Independent counterexamples for the four 1.5.0 priority corrections.

This arithmetic check complements (and does not replace) content review.
"""
import json, math, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]

def lesson(course, number):
    return (ROOT / 'content' / course / f'{course}-{number:02}.md').read_text(encoding='utf-8')

# Approaching a candidate from below alone does not make it an upper bound.
S, u = {0, 1, 2}, 1
assert all(any(u-e < s <= u for s in S) for e in (1e-8, .1, 1, 100))
assert not all(s <= u for s in S)
assert max(S) == 2

# Experiment-disjoint partitions still leak specimens when experiments repeat.
experiments = {'A1': 'A', 'A2': 'A', 'B1': 'B', 'B2': 'B'}
train, test = {'A1', 'B1'}, {'A2', 'B2'}
assert not train & test
assert {experiments[e] for e in train} & {experiments[e] for e in test}
partitions = [{'A1','A2'}, {'B1','B2'}]
assert not ({experiments[e] for e in partitions[0]} & {experiments[e] for e in partitions[1]})

# Row-scaling and the equivalent MSE weight must agree.
residual, scale = [1., 1.], [.5, 2.]
weighted = sum((s*e)**2 for s,e in zip(scale,residual))/len(residual)
assert weighted == 2.125
assert weighted == sum(s*s*e*e for s,e in zip(scale,residual))/len(residual)
assert sum(s*e*e for s,e in zip(scale,residual))/len(residual) == 1.25

# Incompressible-liquid isenthalpic throttling: cp*dT + v*dp = 0.
rho, cp, delta_p = 1000., 4200., -1e6
delta_T = -delta_p/(rho*cp)
assert math.isclose(delta_T, 5/21)
assert math.isclose(cp*delta_T + delta_p/rho, 0., abs_tol=1e-9)

# Compile-time publication contract: stable identity and 30 clear entry guides.
version = json.loads((ROOT/'version.json').read_text(encoding='utf-8'))
assert version['version'] in ('1.5.0', '1.6.0', '1.6.1'), 'No publication contract for this version'
all_lessons = [p for p in (ROOT/'content').glob('*/*.md')]
assert len(all_lessons) == 253
all_guides = sum([json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'content').glob('learning-guides-*.json')], [])
assert len(all_guides) == 30 and len({g['id'] for g in all_guides}) == 30
assert {'calculus-02','calculus-04','linear-algebra-05','linear-algebra-06'} <= {g['id'] for g in all_guides}
assert sum(len(json.loads(p.read_text(encoding='utf-8'))) for p in (ROOT/'content').glob('mastery-exercises-*.json')) == 78
if version['version'] == '1.5.0':
    assert '本科核心续学' in (ROOT/'site/assets/knowledge-map.js').read_text(encoding='utf-8')
else:
    assert 'window.TextbookNav.tree(courses,state)' in (ROOT/'site/assets/app.js').read_text(encoding='utf-8')
    assert 'relation-select' in (ROOT/'site/assets/textbook-navigation.js').read_text(encoding='utf-8')
print('Report revision: four independent counterexamples, stable 253 IDs, 30 entry guides and original 78 mastery tasks passed')

# Reviewed publication sources are frozen by exact content hashes; generated data
# is then rebuilt and compared separately by the offline/browser release checks.
if version['version'] in ('1.6.0', '1.6.1'):
    from verify_reader_revision import verify
    verify()
else:
    manifest_path = ROOT/'reviews/report-revision-2026-10-03.json'
    assert manifest_path.is_file(), 'Reviewed-source manifest is required for this release'
    if manifest_path.exists():
        import hashlib
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        assert manifest['version']=='1.5.0'
        assert len({row['path'] for row in manifest['files']})==len(manifest['files'])
        for row in manifest['files']:
            source=ROOT/row['path']
            assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'], 'Reviewed source changed: '+row['path']
        print(f"Reviewed revision sources: {len(manifest['files'])} exact files match their reviewed digests")
