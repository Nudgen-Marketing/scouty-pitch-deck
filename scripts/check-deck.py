"""Dependency-free structural acceptance checks for the static deck."""
from html.parser import HTMLParser
from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parents[1]
class Deck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.slides, self.references, self.meta, self.images = [], [], [], {}, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'section' and 'slide' in a.get('class', '').split():
            self.slides.append(a)
        if tag == 'meta':
            self.meta[a.get('name', a.get('property', ''))] = a.get('content')
        if tag == 'img':
            self.images.append(a)
        if 'aria-labelledby' in a:
            self.references.extend('#'+x for x in a['aria-labelledby'].split())
        for key in ('href', 'src'):
            if key in a:
                self.references.append(a[key])

text = (ROOT / 'scouty-pitch-deck.html').read_text()
for removed in ('DEMO DAY / OCTOBER 2026', 'Product source: scouty.to · 8 Oct 2026', 'No sales team needed. You approve the first email.'):
    assert removed not in text, f'Unexpected removed copy: {removed}'
d = Deck()
d.feed(text)
assert len(d.slides) == 10, 'Expected ten slides'
assert len(d.ids) == len(set(d.ids)), 'Duplicate IDs'
assert [s['id'] for s in d.slides] == [f'slide-{i}' for i in range(1, 11)]
for key in ('viewport', 'description', 'theme-color', 'og:title', 'og:type', 'og:description', 'twitter:card'):
    assert d.meta.get(key), f'Missing metadata: {key}'
for ref in d.references:
    if ref.startswith('#'):
        assert ref[1:] in d.ids, f'Broken fragment: {ref}'
    elif ref.startswith('data:'):
        assert base64.b64decode(ref.split(',', 1)[1], validate=True), 'Invalid embedded asset'
    elif not re.match(r'^(https?:|mailto:)', ref):
        assert (ROOT / ref).is_file(), f'Missing local asset: {ref}'
assert d.images and all(img.get('alt') for img in d.images)
assert all(img['src'].startswith('data:') for img in d.images), 'Deck must embed images'
assert 'mermail' not in text.lower(), 'Unexpected reference-deck content'
for required in ('prefers-reduced-motion', '@media print', 'touchstart', 'touchend', 'ArrowRight', 'Home:', 'End:', 'aria-live', 'Illustrative', 'Proposed'):
    assert required in text, f'Missing behavior or evidence label: {required}'
workflow = (ROOT / '.github/workflows/deploy-scouty-pitch-deck.yml').read_text()
assert workflow.count("github.ref == 'refs/heads/main' && github.event_name != 'pull_request'") == 2
assert 'contents: read' in workflow and 'pages: write' in workflow and 'id-token: write' in workflow
assert 'scripts/check-deck.py' in workflow and 'scripts/build-site.py' in workflow
assert 'actions/upload-artifact@' in workflow and 'actions/deploy-pages@' in workflow
print('PASS: ten slides, IDs, references, metadata, embedded assets, evidence labels and workflow guards')
