#!/usr/bin/env python3
"""Build the static Pages directory locally; never uploads or deploys anything."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from metronotation.catalog import load_master
from metronotation.pdf import export_pdf
from metronotation.renderer import render_html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    output = args.output.resolve()
    # Keep publication output away from source directories and private photos.
    if (
        output == ROOT
        or ROOT in output.parents
        and output.parts[len(ROOT.parts)]
        in {"data", "metronotation", "docs", "tests", "scripts", ".git", ".github"}
    ):
        parser.error("Choose a separate generated-output directory")
    output.mkdir(parents=True, exist_ok=True)
    records = load_master()
    html = output / "metro-notation.html"
    document = render_html(records)
    html.write_text(document, encoding="utf-8")
    (output / "index.html").write_text(document, encoding="utf-8")
    for filename, batch in (
        ("f2l.html", [r for r in records if r.category == "F2L"]),
        ("oll-01-30.html", [r for r in records if r.category == "OLL" and int(r.id) <= 30]),
        ("oll-31-57.html", [r for r in records if r.category == "OLL" and int(r.id) > 30]),
        ("pll.html", [r for r in records if r.category == "PLL"]),
    ):
        (output / filename).write_text(render_html(batch), encoding="utf-8")
    export_pdf(html, output / "metro-notation.pdf")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Site: {output} (algorithm sheets and PDF)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
