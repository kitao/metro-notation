"""Check the PDF and PNGs in one or more sheet directories.

Directories must contain the same drawing, independent of PDF metadata.
Requires pypdf and Poppler. This complements, rather than replaces, visual review.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from metronotation import __version__
from metronotation.catalog import load_master
from metronotation.pdf import IMAGE_PATHS, export_pngs


def check_images(directory, reference=None):
    """Check every supplied image against its PDF and the first checked drawing."""
    with TemporaryDirectory(prefix="metro-sheet-check-") as temporary:
        rendered = Path(temporary)
        export_pngs(directory / "metro-notation.pdf", rendered)
        current = {}
        for relative in IMAGE_PATHS:
            current[relative] = (rendered / relative).read_bytes()
            if (directory / relative).read_bytes() != current[relative]:
                raise ValueError(f"{directory / relative}: image does not match its PDF")
            if reference is not None and reference[relative] != current[relative]:
                raise ValueError(
                    f"{directory / relative}: drawing differs from the first directory"
                )
    return current


def frame_and_footer(page):
    """Page coordinates of the 1440 × 1006 frame corners and of the copyright baseline."""
    frames, footer_y = [], []

    def transform(x, y, cm):
        return cm[0] * x + cm[2] * y + cm[4], cm[1] * x + cm[3] * y + cm[5]

    def geometry(op, operands, cm, tm):
        if (
            op == b"re"
            and len(operands) == 4
            and abs(float(operands[2]) - 1439.2) < 0.01
            and abs(float(operands[3]) - 1005.2) < 0.01
        ):
            frames.append([transform(x, y, cm) for x, y in ((0, 0), (1440, 1006))])

    def text_position(text, cm, tm, font, size):
        if "©" in text:
            footer_y.append(transform(tm[4], tm[5], cm)[1])

    page.extract_text(visitor_operand_before=geometry, visitor_text=text_position)
    return frames, footer_y


# The footer's links, written out here so that a changed target in the renderer is caught.
LINKS = [
    "https://github.com/kitao/metro-notation",
    "https://store.tribox.com/products/detail.php?product_id=3973",
]


def page_batches(records):
    """The cases on each of the four pages, in reading order."""
    return [records[:41], records[41:71], records[71:98], records[98:]]


def check_pdf(reader, batches, path="metro-notation.pdf"):
    """Check every page's text, size, fonts, frame margins, footer and link targets.

    Forms and annotations other than links are refused as well.
    """
    if len(reader.pages) != len(batches):
        raise ValueError(f"{path}: expected {len(batches)} pages")
    for index, (page, batch) in enumerate(zip(reader.pages, batches), 1):
        category = batch[0].category
        title = category if category != "OLL" else f"OLL {batch[0].id}–{batch[-1].id}"
        expected = (
            "Cube Algorithms: "
            + title
            + f" METRO NOTATION {__version__} Start Learn first "
            + " ".join(
                (r.id if r.category == "PLL" else f"{r.category} {r.id}") + " " + r.text
                for r in batch
            )
        )
        expected += " © 2020–2026 Takashi Kitao (github.com/kitao/metro-notation) | Algorithm source: tribox CFOP Sheet B-1.0"
        actual = " ".join(page.extract_text().split())
        # PDF extractors may infer spaces between letter-spaced subtitle glyphs.
        # Normalize this exact heading only; preserve every algorithm token.
        subtitle = f"METRO NOTATION {__version__}"
        subtitle_pattern = r"\s*".join(re.escape(c) for c in subtitle if not c.isspace())
        actual = re.sub(subtitle_pattern + r"(?= Start)", subtitle, actual, count=1)
        if actual != expected:
            raise ValueError(f"{path}: page {index}: label or move order mismatch")
        if (
            abs(float(page.mediabox.width) - 1190.55) > 2
            or abs(float(page.mediabox.height) - 841.89) > 2
        ):
            raise ValueError(f"{path}: page {index}: not A3 landscape")
        embedded = set()
        for resource in page["/Resources"]["/Font"].values():
            font = resource.get_object()
            name = str(font["/BaseFont"]).split("+")[-1]
            descendants = font.get("/DescendantFonts", [])
            descriptor = descendants[0].get_object().get("/FontDescriptor") if descendants else None
            if not descriptor or "/FontFile2" not in descriptor.get_object():
                raise ValueError(f"{path}: page {index}: unexpected unembedded font {name}")
            embedded.add(name)
        if embedded != {"Cabin-Medium", "Cabin-SemiBold", "Arimo-Regular"}:
            raise ValueError(f"{path}: page {index}: substituted fonts {embedded}")
        frames, footer_y = frame_and_footer(page)
        if len(frames) != 1:
            raise ValueError(f"{path}: page {index}: expected one page frame")
        (x1, y1), (x2, y2) = frames[0]
        margins = [
            min(x1, x2),
            float(page.mediabox.width) - max(x1, x2),
            min(y1, y2),
            float(page.mediabox.height) - max(y1, y2),
        ]
        millimeters = [v * 25.4 / 72 for v in margins]
        if any(abs(v - 6) > 0.15 for v in millimeters):
            raise ValueError(f"{path}: page {index}: unequal frame margins {millimeters}")
        if len(footer_y) != 1 or not 0 < footer_y[0] < min(y1, y2):
            raise ValueError(f"{path}: page {index}: copyright is not in the bottom outer margin")
        annotations = [a.get_object() for a in page.get("/Annots", [])]
        if any(a.get("/Subtype") != "/Link" for a in annotations):
            raise ValueError(f"{path}: page {index}: unexpected annotations")
        if sorted(a.get("/A", {}).get("/URI") for a in annotations) != sorted(LINKS):
            raise ValueError(f"{path}: page {index}: unexpected link targets")
    if reader.get_fields():
        raise ValueError(f"{path}: unexpected form fields")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directories",
        nargs="+",
        type=Path,
        help="Directories with the PDF and PNGs; all must match the first",
    )
    args = parser.parse_args()
    try:
        from pypdf import PdfReader
    except ImportError:
        parser.error("PDF checks need pypdf: python -m pip install --group dev")
    records = load_master()
    batches = page_batches(records)
    reference = None
    for directory in args.directories:
        path = directory / "metro-notation.pdf"
        check_pdf(PdfReader(path), batches, path)
        reference = check_images(directory, reference)
        print(
            f"{path}: 4 A3 pages; {len(records)} case labels; "
            f"{sum(len(r.moves) for r in records)} exact moves; 6 mm frame margins; "
            "footer outside frame; embedded typefaces; no form fields"
        )
        print(f"{directory}: four 300 dpi PNGs match the PDF")
    if len(args.directories) > 1:
        print("All directories contain the same rendered sheets.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Sheet check failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
