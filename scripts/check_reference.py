#!/usr/bin/env python3
"""Check the photo transcription without simplifying or replacing its moves.

Only the standard library is used. Structural cube checks detect some copying
errors, not every wrong case, AUF, finger direction, or annotation. Photo review
is always required. Uncertain rows are never evaluated as complete algorithms.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tribox-cfop-b-1.0"
import sys

sys.path.insert(0, str(ROOT))
from metronotation.cube import TOKEN, apply, solved_cube, self_check


@dataclass
class Record:
    kind: str
    id: str
    moves: list[str]
    colors: str
    notes: str
    status: str


def read_records(kind):
    records = []
    for line in (DATA / f"{kind.lower()}.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5 or cells[-1] not in ("転記済", "要確認"):
            continue
        id_, raw, colors, notes, status = cells
        moves = " ".join(re.findall(r"`([^`]+)`", raw)).split()
        records.append(Record(kind, id_, moves, colors, notes, status))
    return records


def starting_cube(record):
    cube = solved_cube()
    for move in reversed(record.moves):
        cube = apply(cube, move, inverse=True)
    return cube


def up_face(record):
    cube = starting_cube(record)
    center = cube[((0, 1, 0), (0, 1, 0))]
    return "/".join(
        "".join("1" if cube[((x, 1, z), (0, 1, 0))] == center else "0" for x in (-1, 0, 1))
        for z in (-1, 0, 1)
    )


def check_structure(record):
    cube = starting_cube(record)
    centers = {normal: color for (pos, normal), color in cube.items() if pos == normal}
    wrong = {pos for (pos, normal), color in cube.items() if color != centers[normal]}
    lower = {pos for pos in wrong if pos[1] < 1}
    if record.kind in ("OLL", "PLL"):
        if lower:
            return f"inverse state disrupts F2L: {sorted(lower)}"
        if record.kind == "PLL":
            if any(
                color != centers[(0, 1, 0)]
                for (pos, normal), color in cube.items()
                if normal == (0, 1, 0)
            ):
                return "inverse state has an unoriented U face"
    else:
        # A single unsolved F2L pair may occupy one bottom corner and one
        # middle-layer edge. The other three slots and the cross must survive.
        slots = [{(x, -1, z), (x, 0, z)} for x in (-1, 1) for z in (-1, 1)]
        if not any(lower <= slot for slot in slots):
            return f"inverse state disrupts cross or multiple slots: {sorted(lower)}"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Fail if any transcription remains uncertain",
    )
    parser.add_argument(
        "--photos", action="store_true", help="Also verify the six original photograph checksums"
    )
    args = parser.parse_args()
    self_check()
    errors = []
    if args.photos:
        source = (DATA / "README.md").read_text(encoding="utf-8")
        photographs = re.findall(r"\| P[1-6] \| \[photos/([^\]]+)\].*?`([0-9a-f]{64})`", source)
        if len(photographs) != 6:
            errors.append("Expected six original photo checksums")
        for filename, digest in photographs:
            path = DATA / "photos" / filename
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                errors.append(f"Original photograph changed or missing: {filename}")
        if not errors:
            print("Six original photographs match their recorded SHA-256 checksums.")
    pending = []
    face_rows = re.findall(
        r"^\| (\d{2}) \| `([01]{3}/[01]{3}/[01]{3})` \|$",
        (DATA / "oll-up-faces.md").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    faces = dict(face_rows)
    if len(face_rows) != 57 or set(faces) != {f"{n:02}" for n in range(1, 58)}:
        errors.append("OLL: incomplete or duplicate photo face data")
    for kind, expected in (
        ("F2L", {f"{n:02}" for n in range(1, 42)}),
        ("OLL", {f"{n:02}" for n in range(1, 58)}),
        ("PLL", set("Aa Ab E F Ga Gb Gc Gd H Ja Jb Na Nb Ra Rb T Ua Ub V Y Z".split())),
    ):
        records = read_records(kind)
        ids = [record.id for record in records]
        if set(ids) != expected or len(ids) != len(expected):
            errors.append(f"{kind}: missing, duplicate, or unexpected IDs")
        checked = 0
        for record in records:
            label = f"{kind} {record.id}"
            for hint, index, token in re.findall(r"([PT])(\d+):([^;\s]+)", record.colors):
                i = int(index) - 1
                if not (0 <= i < len(record.moves)) or record.moves[i] != token:
                    errors.append(f"{label}: {hint}{index}:{token} does not match move")
            for index in re.findall(r"REGRIP→(\d+)", record.notes):
                if not 1 <= int(index) <= len(record.moves):
                    errors.append(f"{label}: REGRIP index out of bounds")
            if record.status != "転記済":
                pending.append(label)
                continue
            if not record.moves or any(not TOKEN.fullmatch(m) for m in record.moves):
                errors.append(f"{label}: empty sequence or unrecognized token")
                continue
            error = check_structure(record)
            if error:
                errors.append(f"{label}: {error}")
            if kind == "OLL" and up_face(record) != faces.get(record.id):
                errors.append(f"{label}: reconstructed U face differs from photo")
            checked += 1
        print(f"{kind}: {len(records)} records; {checked} complete sequences checked")
    for error in errors:
        print(f"ERROR: {error}")
    print("Pending photo confirmation: " + (", ".join(pending) or "none"))
    print("Checked OLL U-face patterns against 57 photo transcriptions.")
    print("Checks do not prove side faces, finger direction, or complete photo fidelity.")
    return 1 if errors or (args.require_complete and pending) else 0


if __name__ == "__main__":
    raise SystemExit(main())
