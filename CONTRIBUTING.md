# Development

Python 3.10 or later is required. The published sheets are a four-page PDF and four 300 dpi PNG images.
HTML and SVG are intermediate formats for rendering and local inspection.

```sh
python -m pip install -e .
metro-notation --open
metro-notation --category PLL -o output/pll.html
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

## Build HTML and PDF

```sh
python -m pip install -e '.[pdf,dev]'
python -m playwright install chromium
python -m metronotation -o output/metro-notation.html --pdf output/metro-notation.pdf
python scripts/build_review.py output/metro-notation.pdf
```

PNG export and the local review gallery require Poppler (`brew install poppler` on macOS;
`apt install poppler-utils` on Ubuntu). Open `output/review.html` to compare all
four sheets. Generated files belong in `output/`; they are excluded from Git.

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
python -m http.server 8769 --directory _site
```

The README links directly to `metro-notation.pdf`. The website root redirects to
that PDF. PNG images in `images/` and 1000-pixel thumbnails in `images/thumbnails/`
are rendered from the same PDF with Poppler. Intermediate HTML is built in a
temporary directory and is not published. Run **Publish cheat sheets** in GitHub Actions
to deploy `_site/`.

To build the Python package, run `python -m build`. Its bundled data includes
the master, CSS, fonts and font licenses. Keep the version in
`metronotation/__init__.py` and `CHANGELOG.md` in sync.
