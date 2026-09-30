"""Copy the verified static textbook into APK assets with a small Android-only adapter."""
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
site = ROOT / 'site'
target = ROOT / 'android/app/build/generated/textbookAssets/www'
target.mkdir(parents=True, exist_ok=True)
expected = {p.relative_to(site) for p in site.rglob('*') if p.is_file()}
expected.add(pathlib.Path('assets/android-adapter.js'))
for path in target.rglob('*'):
    if path.is_file() and path.relative_to(target) not in expected:
        path.unlink()
for relative in expected:
    if str(relative).replace('\\', '/') == 'assets/android-adapter.js':
        source = ROOT / 'android/web/android-adapter.js'
    else:
        source = site / relative
    dest = target / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
entry = target / 'index.html'
html = entry.read_text(encoding='utf-8')
reader_script = re.search(r'<script defer src="assets/app\.js(?:\?v=[a-f0-9]+)?"></script>', html)
assert reader_script, 'Reader script missing'
html = html.replace(reader_script.group(0), '<script defer src="assets/android-adapter.js"></script>' + reader_script.group(0))
entry.write_text(html, encoding='utf-8', newline='\n')
print('Bundled', len(expected), 'offline textbook files into Android assets.')
