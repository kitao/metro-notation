#!/usr/bin/env python3
"""Create a four-page vector gallery from the actual PDF (requires Poppler)."""

import argparse
import hashlib
from html import escape
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from metronotation import __version__


def build_gallery(pdf, output_name="review.html"):
    pdf = Path(pdf).resolve()
    pages = (
        ("F2L", "f2l.svg"),
        ("OLL 01–30", "oll-01-30.svg"),
        ("OLL 31–57", "oll-31-57.svg"),
        ("PLL", "pll.svg"),
    )
    figures = []
    fingerprint = hashlib.sha256(pdf.read_bytes()).hexdigest()[:12]
    for index, (label, filename) in enumerate(pages, 1):
        svg = pdf.parent / filename
        subprocess.run(
            ["pdftocairo", "-f", str(index), "-l", str(index), "-svg", str(pdf), str(svg)],
            check=True,
        )
        url = f"{svg.name}?v={fingerprint}"
        figures.append(
            f'<figure><figcaption>{label}</figcaption><a href="{url}">'
            f'<img src="{url}" alt="{label} cheat sheet"></a></figure>'
        )
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cube Algorithms — Metro Notation VERSION</title><style>
*{box-sizing:border-box}body{margin:0;padding:20px;background:#eef1f3;color:#344754;font:14px system-ui}
header{display:flex;gap:24px;align-items:baseline;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap}
h1{font-size:18px;font-weight:500;margin:0}a{color:inherit}nav{display:flex;gap:20px}
main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
figure{margin:0}figcaption{margin-bottom:8px}img{display:block;width:100%;height:auto;background:white}
@media(max-width:900px){body{padding:12px}main{grid-template-columns:1fr;gap:24px}header{gap:12px}}
</style></head><body><header><h1>Cube Algorithms · Metro Notation VERSION</h1><nav>
<a href="metro-notation.html">HTML</a><a href="PDF_NAME">PDF</a>
<a href="https://github.com/kitao/metro-notation">GitHub</a></nav></header><main>"""
    html = html.replace("VERSION", escape(__version__)).replace(
        "PDF_NAME", escape(pdf.name, quote=True)
    )
    path = pdf.parent / output_name
    path.write_text(html + "".join(figures) + "</main></body></html>", encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    print(build_gallery(args.pdf))


if __name__ == "__main__":
    main()
