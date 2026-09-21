"""Fixed F2L recognition diagrams visually checked against the source closeups."""

from dataclasses import dataclass
import re

from . import ALGORITHMS


@dataclass(frozen=True)
class Recognition:
    side: int
    colors: dict


def load_f2l_diagrams():
    text = (ALGORITHMS / "f2l-patterns.md").read_text(encoding="utf-8")
    records = {}
    for id_, side_, u, f, s, hidden in re.findall(
        r"^\| (\d{2}) \| (-?1) \| `([BRW./]+)` \| `([BRW./]+)` \| `([BRW./]+)` \| `([^`]+)` \|$",
        text,
        re.M,
    ):
        side = int(side_)
        if id_ in records:
            raise ValueError(f"Duplicate F2L recognition diagram {id_}")
        colors = {}
        for values, normal, axes in (
            (u, (0, 1, 0), (0, 2)),
            (f, (0, 0, 1), (0, 1)),
            (s, (side, 0, 0), (2, 1)),
        ):
            if not re.fullmatch(r"[BRW.]{3}/[BRW.]{3}/[BRW.]{3}", values):
                raise ValueError(f"Invalid F2L recognition face {id_}")
            for i, role in enumerate(values.replace("/", "")):
                pos = list(normal)
                pos[axes[0]], pos[axes[1]] = i // 3 - 1, i % 3 - 1
                colors[tuple(pos), normal] = role
        if hidden != "-":
            for item in hidden.split():
                match = re.fullmatch(r"([LRB]):(-?1|0):([BRW])", item)
                if not match:
                    raise ValueError(f"Invalid hidden F2L sticker {id_}")
                face, tangent, role = match.groups()
                normal = {"L": (-1, 0, 0), "R": (1, 0, 0), "B": (0, 0, -1)}[face]
                if normal not in ((-side, 0, 0), (0, 0, -1)):
                    raise ValueError(f"Visible sticker marked hidden {id_}")
                pos = list(normal)
                pos[1], pos[2 if normal[0] else 0] = 1, int(tangent)
                colors[tuple(pos), normal] = role
        records[id_] = Recognition(side, colors)
    if set(records) != {f"{i:02}" for i in range(1, 42)}:
        raise ValueError("Expected 41 complete F2L recognition diagrams")
    return records
