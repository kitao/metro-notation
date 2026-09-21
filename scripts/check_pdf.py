#!/usr/bin/env python3
"""Check full-master PDF labels and exact move order, with titles, notation keys and attribution.

Optional dependency: pypdf. This content check complements rendered-page review;
it does not establish the geometry or readability of the drawing by itself.
"""

import argparse
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from metronotation import __version__
from metronotation.catalog import load_master


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        from pypdf import PdfReader
    except ImportError:
        parser.error("PDF auditing requires the optional pypdf package")
    records = load_master()
    batches = [records[:41], records[41:71], records[71:98], records[98:]]
    for path in args.pdfs:
        reader = PdfReader(path)
        if len(reader.pages) != 4:
            raise ValueError(f"{path}: expected four pages")
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
                descriptor = (
                    descendants[0].get_object().get("/FontDescriptor") if descendants else None
                )
                if not descriptor or "/FontFile2" not in descriptor.get_object():
                    raise ValueError(f"{path}: page {index}: unexpected unembedded font {name}")
                embedded.add(name)
            if embedded != {"Cabin-Medium", "Cabin-SemiBold", "Arimo-Regular"}:
                raise ValueError(f"{path}: page {index}: substituted fonts {embedded}")
            frames = []
            footer_y = []

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
                raise ValueError(
                    f"{path}: page {index}: copyright is not in the bottom outer margin"
                )
            if reader.get_fields() or any(
                a.get_object().get("/Subtype") != "/Link" for a in page.get("/Annots", [])
            ):
                raise ValueError(f"{path}: unexpected interactive fields or annotations")
        print(
            f"{path}: 4 A3 pages; 119 case labels; 1208 exact moves; 6 mm frame margins; footer outside frame; embedded typefaces; no form fields"
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f"PDF audit failed: {exc}", file=sys.stderr)
        sys.exit(1)
