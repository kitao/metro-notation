#!/usr/bin/env python3
"""Build the four-page PDF, 300 dpi PNGs and README thumbnails."""

import argparse
from pathlib import Path
import sys
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from metronotation.catalog import load_master
from metronotation.pdf import export_pdf
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
        in {"data", "metronotation", "docs", "tests", "scripts", ".git", ".github"}
    ):
        parser.error("Choose a separate generated-output directory")
    output.mkdir(parents=True, exist_ok=True)
    records = load_master()
    with TemporaryDirectory(prefix="metro-notation-") as temporary:
        html = Path(temporary) / "metro-notation.html"
        html.write_text(render_html(records), encoding="utf-8")
        export_pdf(html, output / "metro-notation.pdf")
    thumbnails = output / "thumbnails"
    thumbnails.mkdir(parents=True, exist_ok=True)
    for page, name in enumerate(("f2l", "oll-01-30", "oll-31-57", "pll"), 1):
        for destination, resolution in (
            (output / name, ["-r", "300"]),
            (thumbnails / name, ["-scale-to", "1000"]),
        ):
            subprocess.run(
                [
                    "pdftoppm",
                    "-f",
                    str(page),
                    "-l",
                    str(page),
                    *resolution,
                    "-png",
                    "-singlefile",
                    str(output / "metro-notation.pdf"),
                    str(destination),
                ],
                check=True,
            )
    print(f"Sheets: {output} (PDF, four PNGs and thumbnails)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
