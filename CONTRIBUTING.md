# Development

The published sheets are a four-page PDF and four 300 dpi PNG images.
HTML and SVG are intermediate formats for rendering and local inspection.

## Build the sheets

Use Python 3.10 or later and Poppler (`brew install poppler` on macOS;
`apt install poppler-utils` on Ubuntu).

```sh
python -m pip install -e '.[pdf,dev]'
python -m playwright install chromium
python scripts/build_site.py --output output
```

The PDF is written to `output/metro-notation.pdf`, with full-size PNGs in
`output/images/` and README thumbnails in `output/images/thumbnails/`.
All images are rendered from the PDF. Generated files are excluded from Git.

For a quick local preview of selected cases:

```sh
metro-notation --category PLL -o output/pll.html --open
metro-notation --case OLL-25 --case OLL-37 -o output/cases.html --open
```

## Source files

| Content | Location |
| --- | --- |
| Algorithms and photographs | [data/tribox-cfop-b-1.0](data/tribox-cfop-b-1.0/README.md) |
| Parsing and cube simulation | `metronotation/catalog.py`, `cube.py` |
| Move groups and route geometry | `metronotation/learning.py`, `notation.py` |
| Drawing, layout and typography | `metronotation/renderer.py`, `typography.py`, `assets/` |
| Design specification | [docs/design-policy.md](docs/design-policy.md) |
| Algorithm groups | [docs/rhythm-review.md](docs/rhythm-review.md) |

The Markdown master is the single source of algorithm text. Preserve its spelling,
move order and regrip positions when changing the presentation. Algorithm
corrections require source comparison before updating the regression hash.

## Check a change

```sh
ruff check metronotation scripts tests
ruff format --check metronotation scripts tests
python scripts/check_reference.py --require-complete --photos
python -m unittest discover -s tests -v
python scripts/update_rhythm_review.py --check
python scripts/check_pdf.py output/metro-notation.pdf
```

After changing grouping rules, run `python scripts/update_rhythm_review.py` and
review its diff. These checks cover source tokens, cube states, diagram geometry
and PDF content.

Inspect all four sheets at full-page and reading sizes. Check column alignment,
row spacing, color distinction, endpoint openings and text bounds. Include
T / H / Aa, OLL 14 / 25 / 37 / 41 / 42 and F2L 7 / 8 / 26 / 37 in close-ups.
Repeat the visual check on the deployed PDF after publishing.

## Publish

```sh
python scripts/build_site.py
python scripts/check_pdf.py _site/metro-notation.pdf
```

Run **Publish cheat sheets** in GitHub Actions to build, check and deploy `_site/`.
The README links directly to the PDF and PNGs; the website root redirects to the
PDF. Intermediate HTML is built in a temporary directory and is not published.

To build the Python package, run `python -m build`. Its bundled data includes
the master, CSS, fonts and font licenses. Keep the version in
`metronotation/__init__.py` and `CHANGELOG.md` in sync.
