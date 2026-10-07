"""Verify independent release metadata and exact offline payload against this checkout."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import zipfile

p = argparse.ArgumentParser()
p.add_argument('--apk', required=True)
p.add_argument('--metadata', required=True)
p.add_argument('--permissions', required=True)
a = p.parse_args()
root = pathlib.Path(__file__).resolve().parents[1]
metadata = pathlib.Path(a.metadata).read_text(encoding='utf-8')
permissions = pathlib.Path(a.permissions).read_text(encoding='utf-8')
assert "name='app.zhixu.textbook.independent' versionCode='10' versionName='1.6.1'" in metadata
assert "application-label:'知序·独立版'" in metadata
assert 'application-debuggable' not in metadata
assert 'uses-permission' not in permissions
subprocess.run([sys.executable, str(root / 'tools/bundle_android.py')], check=True, capture_output=True)
bundle = root / 'android/app/build/generated/textbookAssets/www'
expected = {p.relative_to(bundle).as_posix(): p.read_bytes() for p in bundle.rglob('*') if p.is_file() and p.name != '.nojekyll'}
with zipfile.ZipFile(a.apk) as z:
    actual = {n.removeprefix('assets/www/'): z.read(n) for n in z.namelist() if n.startswith('assets/www/') and not n.endswith('/')}
assert actual.keys() == expected.keys(), 'APK runtime asset inventory differs from source'
assert len(actual) == 155, f'Unexpected 1.6.1 runtime asset count: {len(actual)}'
for name, data in actual.items():
    assert data == expected[name], f'APK resource differs: {name}'
print(json.dumps({'sha256': hashlib.sha256(pathlib.Path(a.apk).read_bytes()).hexdigest(),
                  'applicationId': 'app.zhixu.textbook.independent', 'label': '知序·独立版',
                  'versionName': '1.6.1', 'versionCode': 10, 'debuggable': False,
                  'requested_permissions': 0, 'exact_runtime_assets': len(actual)}, ensure_ascii=False))
