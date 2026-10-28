"""Package only public presentation files; works locally and in Actions."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir()
shutil.copyfile(ROOT / 'scouty-pitch-deck.html', SITE / 'index.html')
for name in ('scouty-pitch-deck.html', 'scouty-pitch-deck-vi.html'):
    shutil.copyfile(ROOT / name, SITE / name)
shutil.copytree(ROOT / 'assets', SITE / 'assets')
(SITE / '.nojekyll').touch()
print('Packaged English index.html, both language decks, assets/ and .nojekyll')
