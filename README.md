# Scouty — Demo-day pitch deck

English, ten-slide presentation for [Scouty](https://scouty.to/), a B2B prospecting and personal outreach product for founders and small teams.

## Contents

| File / folder | Purpose |
| --- | --- |
| `scouty-pitch-deck.html` | Standalone interactive deck with embedded brand assets |
| `assets/` | Official Scouty logo and mark |
| `DESIGN-SYSTEM-SCOUTY.md` | Brand and presentation conventions |
| `docs/speaker-notes.md` | Five-minute script |
| `docs/evidence.md` | Sources, claim boundaries and missing evidence |
| `scripts/` | Dependency-free validation and static-site packaging |
| `.github/workflows/` | Preview and GitHub Pages deployment |

Open the HTML directly, or run `python3 -m http.server 8000` and visit `http://localhost:8000/scouty-pitch-deck.html`.
Use arrow keys, Page Up/Down, Home/End, horizontal swipe or the on-screen buttons. Vertical scrolling works on mobile. Slide anchors support direct links.
Print with background graphics enabled and headers/footers disabled to produce ten landscape pages. The deck works offline using embedded images and system fonts.

## Validation and packaging

```sh
python3 scripts/check-deck.py
python3 scripts/build-site.py
```

The `site/` artifact contains only the deck at `index.html` and `scouty-pitch-deck.html`, shared assets and `.nojekyll`. Generated outputs are ignored.

## GitHub Actions / Pages

Relevant pull requests to `main`, pushes to `main` and manual runs validate and upload the downloadable `scouty-pitch-deck` artifact. Only `main` pushes or manual runs from `main` deploy to Pages; pull requests never deploy.

Before the first deployment, set repository **Settings → Pages → Build and deployment → Source → GitHub Actions**. The workflow needs the `github-pages` environment to allow deployment from `main`; review any repository-specific environment rules. No custom domain or secret is required. The default project URL is `https://nudgen-marketing.github.io/scouty-pitch-deck/`; it is an expected address, not a claim of live deployment.

The workflow grants read-only contents permission by default and Pages/id-token write permissions only to the deploy job. Local delivery does not enable Pages, push commits or initiate deployment.

## Evidence

This is an evidence-led product pitch, not a traction report. Illustrative outreach is labelled; pricing and GTM are proposed experiments. See `docs/evidence.md` before adding private metrics, team claims or fundraising details.

Optional browser acceptance checks: with Playwright available on `NODE_PATH` (or locally installed), run `node scripts/check-browser.cjs`. Set `CHROME_PATH` to an existing Chrome executable if Playwright's browser is unavailable. This checks all slides at three viewport sizes, controls, boundaries and simulated swipe events, then generates a cover preview and PDF in `output/`. The verified local PDF contains ten landscape pages. No browser dependency is required by the structural CI checks.
