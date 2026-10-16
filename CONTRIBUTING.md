# Development

The published sheets are a four-page PDF and four 300 dpi PNG images.
HTML and SVG are intermediate formats for rendering and local inspection.

## Build the sheets

Use Python 3.10 or later, pip 25.1 or later, and Poppler (`brew install poppler` on macOS;
`apt install poppler-utils` on Ubuntu).

```sh
python -m pip install --group dev
python -m playwright install chromium
python scripts/build_sheets.py
```

The PDF and four PNGs are written to `output/`. Each PNG is rendered from the PDF.
Local builds are excluded from Git; reviewed files are kept in `sheets/`.

For a quick local preview of selected cases:

```sh
python src/metronotation --category PLL -o output/pll.html --open
python src/metronotation --case OLL-25 --case OLL-37 -o output/cases.html --open
```

## Source files

| Content | Location |
| --- | --- |
| Published PDF and PNGs | [sheets/](sheets/) |
| Canonical algorithms and source photographs | [algorithms/](algorithms/README.md) |
| Parsing, cube simulation and rendering | [src/metronotation/](src/metronotation/) |
| Build and validation commands | [scripts/](scripts/) |
| Design and grouping specifications | [docs/design.md](docs/design.md), [docs/grouping.md](docs/grouping.md) |
| Regression tests | [tests/](tests/) |

The Markdown master is the single source of algorithm text. Preserve its spelling,
move order and regrip positions when changing the presentation. Algorithm
corrections require source comparison before updating the regression hash.

## Check a change

```sh
ruff check src scripts tests
ruff format --check src scripts tests
python scripts/check_algorithms.py --require-complete --photos
python -m unittest discover -s tests -v
python scripts/update_grouping.py --check
python scripts/check_sheets.py output
```

After changing grouping rules, run `python scripts/update_grouping.py` and
review its diff. These checks cover source tokens, cube states, diagram geometry
and PDF content. The sheet check renders the PDF and compares all four PNGs.

Inspect all four sheets at full-page and reading sizes. Check column alignment,
row spacing, color distinction, endpoint openings and text bounds. Include
T / H / Aa, OLL 14 / 25 / 37 / 41 / 42 and F2L 7 / 8 / 26 / 37 in close-ups.
Repeat the visual check on the published PDF.

## Update the distribution

**Check sheets** runs on pushes and pull requests. It builds the PDF and PNGs,
checks that generated and published drawings match, and retains the generated
files as the `metro-notation` artifact for seven days.

Use this artifact for distribution: local font shaping can differ from the
workflow's output. After a visual change, the comparison with `sheets/` will fail;
review the artifact, copy its five files into `sheets/`, and commit them.
The README displays the full PNGs at a reduced size; GitHub supplies
the links to its image viewer, with repository navigation available.
Keep tagged release attachments unchanged. Intermediate HTML is
built in a temporary directory and is not distributed.

Keep the version in `src/metronotation/__init__.py` and `CHANGELOG.md` in sync.

## Website

The website is served at `https://kitao.dev/metro-notation/` using Cloudflare
Workers Static Assets. It uses the README as its page content and copies the
five reviewed files from `sheets/` unchanged. Page layout lives in `web/`;
`dist/` is generated and excluded from Git.

The page uses kitao.dev's shared Noto Sans JP stylesheet at
`/assets/fonts/noto-sans-jp.css` for English and Japanese. These fonts belong to
the `kitao-dev` Worker and are not included in this project's public build.

Use Node.js 24 or later:

```sh
npm ci
npm test
npm run preview
```

Open `http://127.0.0.1:4175/metro-notation/`. The preview uses the Cloudflare
runtime, including its redirects, headers, and 404 behavior. The four PNGs
provide an overview; opening an image does not provide a separate zoom viewer.
Keep the `kitao-dev` repository alongside this one for local preview. Its
`assets/fonts/` is copied into the preview build so fonts load from the same
origin. The normal build and deployment omit that local copy.

After reviewing the page and explicitly approving publication, run locally:

```sh
npm run deploy
```

Deployment runs the website checks and build first. Authentication uses existing
OAuth credentials protected by the OS keychain and stops if that storage is
unavailable; API token/key environment variables are rejected. Do not use
plaintext credential files. GitHub Actions checks and builds the website without
deploying it or storing Cloudflare credentials.

The suffix wildcard in `kitao.dev/metro-notation*` also matches query strings on
the slashless URL, as in the Keynote setup. Static Assets redirects these to
`/metro-notation/` while preserving the query string. This avoids a separate
zone redirect rule. Files are published only inside the `metro-notation/`
directory; other paths have no matching assets and return 404.

After publication, check the page and all five sheet links, compare the public
files with `sheets/`, and verify the trailing-slash redirect and unknown-path 404s.
Verify that the existing Pyxel, Playload, and Keynote pages still work.
