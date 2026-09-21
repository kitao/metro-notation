#!/usr/bin/env python3
"""Keep the published 119-case reading table synchronized with actual output."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from metronotation.catalog import load_master
from metronotation.learning import READING_PHRASES, idiom_tokens, sequence_tokens
from metronotation.renderer import diagram_groups


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "docs/rhythm-review.md"
    old = path.read_text(encoding="utf-8")
    preface = old.split("| ケース |", 1)[0]
    rows = [
        "| ケース | 路線の区切り | 検出した定番手順 | 個別に区切りを指定 |",
        "|---|---|---|---|",
    ]
    for record in load_master():
        groups = " ／ ".join(
            "`" + " ".join(m.text for _, m in g) + "`" for g in diagram_groups(record)
        )
        names = dict.fromkeys(
            name for name, _ in [*idiom_tokens(record).values(), *sequence_tokens(record).values()]
        )
        curated = "あり" if record.key in READING_PHRASES else "—"
        rows.append(f"| {record.key} | {groups} | {', '.join(names) or '—'} | {curated} |")
    new = preface + "\n".join(rows) + "\n"
    if args.check:
        if old != new:
            print(
                "Rhythm review is stale: run python scripts/update_rhythm_review.py",
                file=sys.stderr,
            )
            return 1
    else:
        path.write_text(new, encoding="utf-8")
    print("Rhythm review: 119 cases match the renderer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
