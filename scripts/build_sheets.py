"""Build the four-page PDF, four 300 dpi PNGs in output/."""

import argparse
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from metronotation.catalog import load_master
from metronotation.pdf import IMAGE_PATHS, export_pdf, export_pngs
from metronotation.renderer import render_html


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    output = ROOT / "output"
    # A symlinked output directory could point at the reviewed sheets/.
    if output.is_symlink():
        raise SystemExit(f"{output} must be a directory, not a symlink")
    output.mkdir(exist_ok=True)
    records = load_master()
    # Build beside the destination, then move each finished file into place. Replacing the
    # directory entry never writes through an existing symlink or hard link.
    with TemporaryDirectory(prefix=".build-", dir=output) as temporary:
        temporary = Path(temporary)
        html = temporary / "metro-notation.html"
        html.write_text(render_html(records), encoding="utf-8")
        export_pdf(html, temporary / "metro-notation.pdf")
        export_pngs(temporary / "metro-notation.pdf", temporary)
        for path in (Path("metro-notation.pdf"), *IMAGE_PATHS):
            os.replace(temporary / path, output / path)
    print(f"Sheets: {output} (PDF and four PNGs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
