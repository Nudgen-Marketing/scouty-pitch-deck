"""Package only public presentation files; works locally and in Actions."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir()
for name in ('index.html', 'scouty-pitch-deck.html'):
    shutil.copyfile(ROOT / 'scouty-pitch-deck.html', SITE / name)
shutil.copytree(ROOT / 'assets', SITE / 'assets')
(SITE / '.nojekyll').touch()
print('Packaged index.html, scouty-pitch-deck.html, assets/ and .nojekyll')
