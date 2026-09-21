# Maintaining and publishing Metro Notation

## Generate the cheat sheets

Python 3.10 or later is required. HTML generation has no runtime dependencies.

```sh
python -m pip install -e .
metro-notation --open
metro-notation --category PLL -o pll.html
```

HTML works offline. To print from a browser, select A3 landscape, enable
background graphics and disable browser headers and footers. For automatic PDF
export, install the optional tools shown under “Change and verify” below.

## Repository layout

```text
metronotation/                  Python implementation and bundled CSS
  assets/                      CSS and licensed, embedded typefaces
data/tribox-cfop-b-1.0/         Canonical Markdown data and source photographs
  photos/
docs/                          Design, notation, verification and maintenance
scripts/                       Build and verification commands
tests/                         Source, cube-state and rendering regression tests
.github/workflows/             CI and manual website publication
```

Python modules and scripts use `snake_case`; documentation and data use
`kebab-case`. Each master file is named for its CFOP category. Source photographs
have descriptive names and stable IDs in the source README. The Python package
bundles the canonical data directly; there is no second editable copy.

Generated directories are ignored by Git: `output/` for local sheets, `_site/`
for the website, and `build/` / `dist/` for Python packaging. They are reproducible
outputs, not input data. Keep temporary audits and screenshots outside the repo.

## Sources of truth

| Concern | Location |
| --- | --- |
| Exact moves, regrips, provisional finger hints | `data/tribox-cfop-b-1.0/{f2l,oll,pll}.md` |
| Original photographs and checksums | `data/tribox-cfop-b-1.0/photos/` and its parent README |
| Independent recognition data | `f2l-diagrams.md`, `oll-up-faces.md` beside the master |
| Parsing / source validation | `metronotation/catalog.py` |
| Cube state and move conventions | `metronotation/cube.py` |
| Lossless notation / geometric grouping | `metronotation/notation.py` |
| Idioms and source-specific reading phrases | `metronotation/learning.py` |
| SVG, legend, layout and print geometry | `metronotation/renderer.py` |
| Screen / print presentation | `metronotation/assets/style.css` |
| Offline typography and licenses | `metronotation/typography.py`, `assets/fonts/` |
| Visual contract and rationale | [design-policy.md](design-policy.md) |
| Current checks and limitations | [verification.md](verification.md) |

The root README contains English first, then Japanese. Keep both sections in sync.
Do not reintroduce the retired text parser, PNG renderer or duplicate algorithm
sources. HTML generation uses the Python standard library. Only PDF printing uses
Playwright / Chromium; the publication gallery uses Poppler's vector conversion.
The optional `dev` extra provides packaging and PDF-audit tools.

## Change and verify

1. Read the design policy and notation contract before modifying the drawing.
2. Keep the master unchanged for visual work. Its reviewed spelling is guarded
   by a SHA-256 regression assertion. Never update that assertion just to make a
   failing test pass. A deliberate algorithm change requires photo review and
   an explicit new source/version decision.
3. Keep source regrips mandatory. Reading phrases duplicate text only to validate
   their boundaries against the master, never to substitute different moves.
4. Update the rhythm table after a grouping change:

```sh
ruff check metronotation scripts tests
ruff format --check metronotation scripts tests
python scripts/update_rhythm_review.py
python scripts/check_reference.py --require-complete --photos
python -m unittest discover -s tests -v
python scripts/update_rhythm_review.py --check
```

5. Generate and audit the actual deliverables:

```sh
python -m pip install -e '.[pdf,dev]'
python -m playwright install chromium
python -m metronotation -o output/metro-notation.html --pdf output/metro-notation.pdf
python scripts/check_pdf.py output/metro-notation.pdf
python scripts/build_review.py output/metro-notation.pdf
```

Install Poppler for `pdftocairo`, `pdftoppm` and `pdfinfo` (`brew install poppler`
on macOS or the `poppler-utils` package on Ubuntu).

6. Render all four PDF pages and inspect them, not only a changed example:

```sh
pdftoppm -scale-to 1800 -png output/metro-notation.pdf /tmp/metro-review
```

Review the four-sheet gallery, each complete sheet, and enlarged T / H / Aa,
OLL 14 / 25 / 37 / 41 / 42 and F2L 7 / 8 / 26 / 37. These exercise diagonal
openings, double rails, thin middle lines, long wraps and hidden stickers.
Check actual text bounds, not only SVG viewports. Inspect both HTML and PDF;
font substitution and rasterization can reveal defects numeric tests miss.
Check title-to-frame and last-row-to-frame spacing together, plus header/body
separation, column origins, row rhythm and footer clearance on both sides.

7. Check packaging from outside the checkout:

```sh
python -m build
python -m venv /tmp/metro-package-check
/tmp/metro-package-check/bin/python -m pip install dist/metro_notation-1.0-py3-none-any.whl
cd /tmp
/tmp/metro-package-check/bin/python -m metronotation --check
/tmp/metro-package-check/bin/python -m metronotation -o metro-installed.html
```

On Windows use the environment's `Scripts/python.exe`. The installed package
must contain its Markdown master, CSS, fonts and licenses and generate all 119 cases without
accessing this checkout. CI exercises Python 3.10 and 3.14 on Linux and Windows.
A local run does not establish that those hosted CI jobs have passed.

## GitHub Pages

```sh
python scripts/build_site.py
python scripts/check_pdf.py _site/metro-notation.pdf
python -m http.server 8769 --directory _site
```

The generated `_site/` contains `index.html`, the self-contained HTML,
`metro-notation.pdf`, `f2l.svg`, `oll-01-30.svg`, `oll-31-57.svg`, `pll.svg`
and `.nojekyll`. It contains no source photographs.
Gallery links are relative so repository-subpath hosting works.
The build does not upload or publish anything.

Website:

- Web: https://kitao.github.io/metro-notation/
- PDF: https://kitao.github.io/metro-notation/metro-notation.pdf

When publication is authorized, set the repository's Pages source to
**GitHub Actions**, then run **Publish cheat sheets**. The workflow is manual;
it builds, runs source/unit/rhythm checks, audits the PDF, uploads only `_site/`
and deploys through the `github-pages` environment. It does not publish on every
push. See [GitHub's Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

After deployment, verify the live index, linked HTML, all four SVG pages and PDF.
Website publication and an official versioned release are separate operations.
Create release tags only when an official release is approved.
