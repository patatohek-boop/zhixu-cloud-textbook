"""Dependency-free checks for the static site's security-sensitive configuration."""
import hashlib
import json
import pathlib
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Entry(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas = {}
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert not any(k.lower().startswith('on') for k in attrs), 'Inline event handler in entry page'
        if tag == 'meta':
            self.metas[(attrs.get('http-equiv') or attrs.get('name') or '').lower()] = attrs.get('content', '')
        if tag == 'script':
            self.scripts.append(attrs.get('src', ''))


def check():
    entry = Entry()
    entry.feed((ROOT / 'site/index.html').read_text(encoding='utf-8'))
    policy = dict((part.strip().split()[0], part.strip().split()[1:])
                  for part in entry.metas.get('content-security-policy', '').split(';') if part.strip())
    for directive in ('default-src', 'connect-src', 'object-src', 'base-uri', 'form-action', 'frame-src', 'worker-src', 'script-src-attr'):
        assert policy.get(directive) == ["'none'"], f'Missing restriction: {directive}'
    assert policy.get('script-src') == ["'self'"], 'Scripts must remain local; no inline/eval permissions'
    assert entry.metas.get('referrer') == 'no-referrer', 'Unexpected referrer policy'
    for src in entry.scripts:
        assert src.startswith('assets/') and '..' not in src and ':' not in src, f'Unexpected script source: {src}'
        assert (ROOT / 'site' / src).is_file(), f'Missing script: {src}'
    assert entry.scripts.index('assets/learning-state.js') < entry.scripts.index('assets/app.js')

    workflow = (ROOT / '.github/workflows/pages.yml').read_text(encoding='utf-8')
    actions = re.findall(r'uses:\s+(\S+)', workflow)
    assert len(actions) == 5
    assert all(re.fullmatch(r'actions/[\w-]+@[a-f0-9]{40}', action) for action in actions), 'Actions must use immutable commits'
    assert 'persist-credentials: false' in workflow
    assert "github.ref == 'refs/heads/main' && github.event_name != 'pull_request'" in workflow
    assert 'pull_request_target' not in workflow and 'write-all' not in workflow

    # Metadata flows into routes, CSS colors and reference URLs outside Markdown.
    courses = 0
    for path in (ROOT / 'content').glob('*/course.json'):
        course = json.loads(path.read_text(encoding='utf-8'))
        assert re.fullmatch(r'[a-z][a-z0-9-]*', course['id']), f'Invalid course ID: {path.name}'
        assert re.fullmatch(r'#[0-9a-fA-F]{6}', course['color']), f'Invalid course color: {course["id"]}'
        for source in course['sources']:
            parsed = urlparse(source['url'])
            assert parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password, 'Reference must be a credential-free HTTPS URL'
        for filename in course['lessons']:
            assert re.fullmatch(r'[a-z0-9-]+\.md', filename), 'Lesson filename must stay in its course folder'
            text = (path.parent / filename).read_text(encoding='utf-8')
            meta = json.loads(text[8:].split('\n---\n', 1)[0])
            assert re.fullmatch(r'[a-z][a-z0-9-]*', meta['id']), 'Invalid lesson ID'
            assert isinstance(meta['minutes'], int) and 0 < meta['minutes'] < 1000
        courses += 1

    diagrams = 0
    for path in (ROOT / 'site/assets/diagrams').glob('*.svg'):
        svg = ET.fromstring(path.read_text(encoding='utf-8'))
        for element in svg.iter():
            tag = element.tag.rsplit('}', 1)[-1].lower()
            assert tag not in ('script', 'foreignobject', 'iframe', 'object', 'embed'), f'Active SVG content: {path.name}'
            for name, value in element.attrib.items():
                name = name.rsplit('}', 1)[-1].lower()
                assert not name.startswith('on'), f'SVG event handler: {path.name}'
                if name in ('href', 'src'):
                    assert value.startswith('#'), f'SVG external resource: {path.name}'
            assert not re.search(r'(?:https?:|javascript:|@import)', element.text or '', re.I), f'SVG external code/style: {path.name}'
        diagrams += 1

    # Hashes detect unexpected edits; they do not replace upstream vulnerability review.
    manifest = json.loads((ROOT / 'tools/vendor-integrity.json').read_text(encoding='utf-8'))
    actual_files = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'site/assets/vendor').rglob('*') if p.is_file()}
    assert actual_files == set(manifest), 'Vendor inventory changed; review the upstream package before updating integrity records'
    for relative, expected in manifest.items():
        data = (ROOT / relative).read_bytes()
        if pathlib.Path(relative).suffix in ('.js', '.css', '.json', '.txt'):
            data = data.replace(b'\r\n', b'\n')
        assert hashlib.sha256(data).hexdigest() == expected, f'Vendor integrity mismatch: {relative}'
    print(json.dumps({'security_configuration': 'passed', 'courses': courses, 'pinned_actions': len(actions), 'vendor_files': len(manifest), 'safe_diagrams': diagrams}))


if __name__ == '__main__':
    check()
