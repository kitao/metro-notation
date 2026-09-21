#!/usr/bin/env python3
"""Build the four-page PDF and four 300 dpi PNGs."""

import argparse
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from metronotation.catalog import load_master
from metronotation.pdf import export_pdf, export_pngs
from metronotation.renderer import render_html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    output = args.output.resolve()
    # Keep generated sheets away from source directories and reference photos.
    if (
        output == ROOT
        or ROOT in output.parents
        and output.parts[len(ROOT.parts)]
        in {"algorithms", "src", "docs", "tests", "scripts", ".git", ".github"}
    ):
        parser.error("Choose a separate generated-output directory")
    output.mkdir(parents=True, exist_ok=True)
    records = load_master()
    with TemporaryDirectory(prefix="metro-notation-") as temporary:
        html = Path(temporary) / "metro-notation.html"
        html.write_text(render_html(records), encoding="utf-8")
        export_pdf(html, output / "metro-notation.pdf")
    export_pngs(output / "metro-notation.pdf", output)
    print(f"Sheets: {output} (PDF and four PNGs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
