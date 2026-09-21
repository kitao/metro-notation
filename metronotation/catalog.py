"""Read the canonical Markdown without duplicating the master in code or JSON."""

from dataclasses import dataclass, field, replace
from importlib.resources import files
from pathlib import Path
import re

from .notation import Move, parse_moves
from .recognition import Recognition, load_f2l_diagrams

SOURCE = "https://store.tribox.com/products/detail.php?product_id=3973"


@dataclass(frozen=True)
class Algorithm:
    category: str
    id: str
    moves: tuple[Move, ...]
    hints: dict[int, str] = field(default_factory=dict)
    regrips: dict[int, str] = field(default_factory=dict)
    notes: str = ""
    source_lines: tuple[str, ...] = ()
    source: str = "User algorithms"
    recognition: Recognition | None = None

    @property
    def beginner(self):
        """The source sheet's young-leaf marker, not an inferred difficulty score."""
        return "若葉" in self.notes

    @property
    def key(self):
        return f"{self.category}-{self.id}"

    @property
    def text(self):
        return " ".join(move.text for move in self.moves)


def read_markdown(text, category):
    records = []
    seen = set()
    in_table = False
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.startswith("| ID | 手順"):
            in_table = True
            continue
        if not line.startswith("|"):
            in_table = False
        if not in_table:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and re.fullmatch(r":?-+:?", cells[0]):
            continue
        if len(cells) != 5:
            raise ValueError(f"{category}:{line_no}: expected five columns")
        id_, raw, colors, notes, status = cells
        if not id_:
            raise ValueError(f"{category}:{line_no}: missing case ID")
        if id_ in seen:
            raise ValueError(f"{category}: duplicate case {id_}")
        seen.add(id_)
        if status != "転記済":
            raise ValueError(f"{category} {id_}: transcription has not been confirmed")
        source_lines = tuple(re.findall(r"`([^`]+)`", raw))
        if not source_lines or re.sub(r"`[^`]+`|<br>|\s", "", raw):
            raise ValueError(f"{category} {id_}: malformed move column")
        moves = parse_moves(" ".join(source_lines))
        hints = {}
        if colors not in ("—", "未照合"):
            for item in colors.split(";"):
                match = re.fullmatch(r"\s*([PT])(\d+):(.+?)\s*", item)
                if not match:
                    raise ValueError(f"{category} {id_}: invalid finger hint {item}")
                kind, number, token = match.groups()
                index = int(number) - 1
                if not 0 <= index < len(moves) or moves[index].text != token or index in hints:
                    raise ValueError(f"{category} {id_}: finger hint does not match {item}")
                hints[index] = kind
        regrips = {}
        for hand, number in re.findall(r"(左手)?REGRIP→(\d+)", notes):
            index = int(number) - 1
            if not 0 <= index < len(moves) or index in regrips:
                raise ValueError(f"{category} {id_}: invalid regrip position")
            regrips[index] = "left" if hand else "regrip"
        records.append(
            Algorithm(category, id_, moves, hints, regrips, notes, source_lines, source=SOURCE)
        )
    if not records:
        raise ValueError(f"{category}: no algorithm rows found")
    return records


def load_master():
    result = []
    local = Path(__file__).resolve().parents[1] / "data" / "tribox-cfop-b-1.0"
    resource = local if (local / "f2l.md").is_file() else files("metronotation.reference")
    for category, expected in (
        ("F2L", {f"{i:02}" for i in range(1, 42)}),
        ("OLL", {f"{i:02}" for i in range(1, 58)}),
        ("PLL", set("Aa Ab E F Ga Gb Gc Gd H Ja Jb Na Nb Ra Rb T Ua Ub V Y Z".split())),
    ):
        records = read_markdown(
            resource.joinpath(category.lower() + ".md").read_text(encoding="utf-8"), category
        )
        if {record.id for record in records} != expected:
            raise ValueError(f"{category}: master case IDs are incomplete or unexpected")
        if category == "F2L":
            diagrams = load_f2l_diagrams()
            records = [replace(r, recognition=diagrams[r.id]) for r in records]
        result.extend(records)
    return result
