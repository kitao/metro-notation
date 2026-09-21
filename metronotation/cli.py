"""Generate portable HTML/SVG and optional PDF overview sheets."""

import argparse
from pathlib import Path
import sys
import webbrowser

from . import __version__
from .catalog import load_master
from .renderer import render_html


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", type=Path, default=Path("output/metro-notation.html"))
    parser.add_argument("--pdf", type=Path, help="Also print the same HTML to PDF (optional extra)")
    parser.add_argument("--lang", choices=("en", "ja"), default="en")
    parser.add_argument("--category", action="append", choices=("F2L", "OLL", "PLL"))
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        help="Exact case key, e.g. PLL-Ub or OLL-49; repeatable",
    )
    parser.add_argument("--open", action="store_true", help="Open the HTML after generation")
    parser.add_argument(
        "--check", action="store_true", help="Parse the master without producing output"
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)
    try:
        records = load_master()
        if len({r.key for r in records}) != len(records):
            raise ValueError("Duplicate case keys across inputs")
        if args.category:
            records = [r for r in records if r.category in args.category]
        if args.cases:
            missing = set(args.cases) - {r.key for r in records}
            if missing:
                raise ValueError("Unknown or filtered-out cases: " + ", ".join(sorted(missing)))
            records = [r for r in records if r.key in args.cases]
        if not records:
            raise ValueError("No cases match the selection")
        if args.check:
            print(f"{len(records)} cases parsed; master move spelling preserved.")
            return 0
        output = args.output.resolve()
        # Protect both the repository master and installed package resources.
        package = Path(__file__).resolve().parent
        masters = (package.parent / "data" / "tribox-cfop-b-1.0", package / "reference")
        sources = {p.resolve() for master in masters for p in master.glob("*.md")}
        destinations = [output] + ([args.pdf.resolve()] if args.pdf else [])
        if any(path in sources for path in destinations):
            raise ValueError("Output must not overwrite an input or master file")
        if len(set(destinations)) != len(destinations):
            raise ValueError("HTML and PDF output paths must differ")
        document = render_html(records, args.lang)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(document, encoding="utf-8")
        print(f"HTML: {output} ({len(records)} cases)")
        if args.pdf:
            from .pdf import export_pdf

            print(f"PDF: {export_pdf(output, args.pdf)}")
        if args.open:
            webbrowser.open(output.as_uri())
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"metro-notation: {exc}", file=sys.stderr)
        return 2
