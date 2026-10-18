"""Generate portable HTML/SVG and optional PDF overview sheets."""

import argparse
import sys
import webbrowser
from pathlib import Path

from . import ALGORITHMS, ROOT, __version__
from .catalog import load_master
from .renderer import render_html


def check_destination(path):
    """Refuse to replace master data or a reviewed sheet, however the path is spelled."""
    # samefile compares the files themselves, so symlinks and case variants cannot slip through.
    if path.exists() and any(
        path.samefile(source)
        for directory in (ALGORITHMS, ROOT / "sheets")
        for source in directory.rglob("*")
        if source.is_file()
    ):
        raise ValueError(f"{path}: output must not replace master data or a reviewed sheet")


def same_file(a, b):
    """Whether two paths resolve to one path or already are one file."""
    return a.resolve() == b.resolve() or (a.exists() and b.exists() and a.samefile(b))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output/metro-notation.html"),
        metavar="HTML",
        help="HTML file (default: %(default)s)",
    )
    parser.add_argument("--pdf", type=Path, help="Also print the generated HTML to PDF")
    parser.add_argument(
        "--category", action="append", choices=("F2L", "OLL", "PLL"), help="Category; repeatable"
    )
    parser.add_argument(
        "--case",
        action="append",
        dest="cases",
        metavar="CASE",
        help="Exact case key, e.g. PLL-Ub or OLL-49; repeatable",
    )
    parser.add_argument("--open", action="store_true", help="Open the HTML after generation")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)
    try:
        records = load_master()
        if args.category:
            records = [r for r in records if r.category in args.category]
        if args.cases:
            missing = set(args.cases) - {r.key for r in records}
            if missing:
                raise ValueError("Unknown or filtered-out cases: " + ", ".join(sorted(missing)))
            records = [r for r in records if r.key in args.cases]
        if not records:
            raise ValueError("No cases match the selection")
        for path in (args.output, args.pdf):
            if path:
                check_destination(path)
        # Refused before anything is written.
        if args.pdf and same_file(args.pdf, args.output):
            raise ValueError("HTML and PDF output paths must differ")
        output = args.output.resolve()
        document = render_html(records)
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
        print(f"{parser.prog}: {exc}", file=sys.stderr)
        return 2
