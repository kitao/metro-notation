# Development

The published sheets are a four-page PDF and four 300 dpi PNG images.
HTML and SVG are intermediate formats for rendering and local inspection.

## Build the sheets

Use Python 3.10 or later and Poppler (`brew install poppler` on macOS;
`apt install poppler-utils` on Ubuntu).

```sh
python -m pip install -e '.[pdf,dev]'
python -m playwright install chromium
python scripts/build_sheets.py
```

The PDF is written to `output/metro-notation.pdf`, with full-size PNGs in
`output/` and README thumbnails in `output/thumbnails/`.
All images are rendered from the PDF. Local builds are excluded from Git;
the reviewed distribution files are kept in `sheets/`.

For a quick local preview of selected cases:

```sh
metro-notation --category PLL -o output/pll.html --open
metro-notation --case OLL-25 --case OLL-37 -o output/cases.html --open
```

## Source files

| Content | Location |
| --- | --- |
| Published PDF, PNGs and thumbnails | [sheets/](sheets/) |
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

## Update the distribution

**Check sheets** runs on pushes and pull requests. It builds the PDF and PNGs,
checks both the generated and published PDFs, and retains the generated files
as the `metro-notation` artifact for seven days.

Review those files, then copy them into `sheets/` and commit them with the source
change. The README links directly to the PDF download and full PNGs.
Keep tagged release attachments unchanged. Intermediate HTML is
built in a temporary directory and is not distributed.

To build the Python package, run `python -m build`. Its bundled data includes
the master, CSS, fonts and font licenses. Keep the version in
`metronotation/__init__.py` and `CHANGELOG.md` in sync.
