"""Verify enrichment assets are shipped byte-for-byte in the offline Android bundle."""
import hashlib, pathlib, re, subprocess, sys
root=pathlib.Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'tools/bundle_android.py')],check=True)
site=root/'site'; target=root/'android/app/build/generated/textbookAssets/www'
required=['assets/knowledge-map.js','assets/learning-experience.css','assets/foundation-labs.js','assets/concept-stories.js','assets/concept-stories.css','assets/figure-viewer.js','assets/data.js','assets/app.js','assets/cfd-labs.js','assets/content-stats.json']
required += [p.relative_to(site).as_posix() for p in (site/'assets/diagrams').glob('*.svg')]
for name in required:
    assert (target/name).is_file(),name
    assert hashlib.sha256((site/name).read_bytes()).digest()==hashlib.sha256((target/name).read_bytes()).digest(),name
entry=(target/'index.html').read_text()
for name in required[:6]: assert name in entry,name
assert 'assets/android-adapter.js' in entry
for link in re.findall(r'(?:src|href)="([^"#]+)"',entry):
    assert not link.startswith(('http://','https://','//')),link
print(f'Offline bundle: {len(required)} reader assets match source; no remote entry assets')
