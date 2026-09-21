"""Recognize learning units and preserve source-specific reading phrases.

This module defines reading aids, not verified fingertrick instructions.
"""

from .catalog import SOURCE

IDIOMS = {
    ("R", "U", "R'", "U'"): "Sexy move",
    ("R'", "F", "R", "F'"): "Sledgehammer",
    ("L'", "U'", "L", "U"): "Sexy move (mirrored)",
    ("L", "F'", "L'", "F"): "Sledgehammer (mirrored)",
    ("U", "R", "U'", "R'"): "Sexy move (inverse)",
    ("U'", "L'", "U", "L"): "Sexy move (inverse mirrored)",
    ("R", "U'", "R'", "U"): "Reverse sexy move",
    ("L'", "U", "L", "U'"): "Reverse sexy move (mirrored)",
    ("F", "R'", "F'", "R"): "Hedgehammer",
    ("F'", "L", "F", "L'"): "Hedgehammer (mirrored)",
    ("R", "U", "R'", "F'"): "J trigger",
    ("L'", "U'", "L", "F"): "J trigger (mirrored)",
    ("R", "U", "R'", "U"): "Half Sune",
    ("L'", "U'", "L", "U'"): "Half Sune (mirrored)",
    ("R'", "U'", "R", "U'"): "Half Anti-Sune",
    ("L", "U", "L'", "U"): "Half Anti-Sune (mirrored)",
}


F2L_INSERTIONS = {("R", "U", "R'"), ("R", "U'", "R'"), ("L'", "U", "L"), ("L'", "U'", "L")}


FOUR_MOVE_UNITS = {
    ("R", "U", "R'", "U'"),
    ("R", "U'", "R'", "U"),
    ("U", "R", "U'", "R'"),
    ("U'", "R", "U", "R'"),
    ("L'", "U'", "L", "U"),
    ("L'", "U", "L", "U'"),
    ("U'", "L'", "U", "L"),
    ("U", "L'", "U'", "L"),
}


READING_PHRASES = {
    "F2L-05": ("U2 R U R'", "U2 R U' R'"),
    "F2L-34": ("U R' D'", "R U' R'", "D R"),
    "F2L-38": ("R U' R'", "U' R U R'", "U2 R U' R'"),
    "F2L-40": ("r U' r'", "U2 r U r'", "R U R'"),
    "F2L-41": ("R U' R'", "r U' r'", "U2 r U r'"),
    "OLL-02": ("R' F' r U2'", "L' U2 l U2'", "R' F R"),
    "OLL-14": ("R' F R", "U R' F' R", "F U' F'"),
    "OLL-15": ("r' U' M'", "U' R U", "r' U r"),
    "OLL-18": ("r U' r'", "F U F U'", "R U R' U'", "F'"),
    "OLL-21": ("R U R' U", "R U' R' U", "R U2' R'"),
    "OLL-22": ("R U2' R2'", "U' R2 U' R2'", "U2' R"),
    "OLL-25": ("F R' F' r", "U R U' r'"),
    "OLL-34": ("U' R U R2'", "U' R' F R", "U R U' F'"),
    "OLL-35": ("R U2' R2'", "F R F'", "R U2' R'"),
    "OLL-36": ("R U R2'", "F' U' F", "U R2 U2' R'"),
    "OLL-38": ("R U R' U", "R U' R' U'", "R' F R F'"),
    "OLL-52": ("R' F' U' F", "U' R U R'", "U R"),
    "OLL-55": ("R' F R", "U R U'", "R2' F' R2", "U' R' U", "R U R'"),
    "PLL-Aa": ("l' U R' D2", "R U' R' D2", "R l"),
    "PLL-F": ("R' U' F'", "R U R' U'", "R' F R2", "U' R'", "U' R U R'", "U R"),
    "PLL-Ga": ("R2 U R' U", "R' U' R U'", "R2 U'", "D R' U R D'"),
    "PLL-Gb": ("R' U' R U", "D' R2 U R' U", "R U' R U'", "R2' D"),
    "PLL-Gd": ("R U R' U'", "D R2 U'", "R U' R' U", "R' U R2 D'"),
    "PLL-Ra": ("U", "R U' R' U'", "R U R D", "R' U' R D'", "R' U2 R'"),
    "PLL-Rb": ("R' U2 R' D'", "R U' R' D R", "U R U' R'", "U' R"),
    "PLL-Ua": ("R U R' U", "R' U' R2 U'", "R' U R' U R"),
    "PLL-V": ("R'", "U R U' R'", "f' U'", "R U2 R'", "U' R U' R'", "f R"),
}


SEQUENCES = {
    "R U R' U R U2 R'": "Sune",
    "R U2 R' U' R U' R'": "Anti-Sune",
    "L' U' L U' L' U2 L": "Sune (mirrored)",
    "L' U2 L U L' U L": "Anti-Sune (mirrored)",
    "r U R' U R U2 r'": "Wide Sune",
    "r U2 R' U' R U' r'": "Wide Anti-Sune",
    "l' U' L U' L' U2 l": "Wide Sune (mirrored)",
    "l' U2 L U L' U l": "Wide Anti-Sune (mirrored)",
}


def sequence_tokens(record):
    # A half-turn's printed prime is retained; matching only identifies the
    # sequence family and never changes its direction or source spelling.
    tokens = tuple(m.face + "2" if m.count == 2 else m.text for m in record.moves)
    marked = {}
    start = 0
    while start + 7 <= len(tokens):
        name = SEQUENCES.get(" ".join(tokens[start : start + 7]))
        if name and not any(i in record.regrips for i in range(start + 1, start + 7)):
            marked.update({i: (name, start) for i in range(start, start + 7)})
            start += 7
        else:
            start += 1
    return marked


def reading_breaks(record):
    result = set()
    phrases = READING_PHRASES.get(record.key) if record.source == SOURCE else None
    if phrases:
        if " ".join(phrases).split() != [m.text for m in record.moves]:
            raise ValueError(f"{record.key}: reading phrases differ from source")
        cursor = 0
        for phrase in phrases:
            result.add(cursor)
            cursor += len(phrase.split())
    for start in {start for _, start in sequence_tokens(record).values()}:
        result.update((start, start + 3, start + 7))
    return result


def learning_units(record):
    """Whole four-move units take precedence over embedded F2L insertions."""
    tokens = tuple(m.text for m in record.moves)
    occupied = set(idiom_tokens(record))
    boundaries = {*record.regrips}
    spans = []
    patterns = [(4, FOUR_MOVE_UNITS)]
    if record.category == "F2L":
        patterns.append((3, F2L_INSERTIONS))
    for size, candidates in patterns:
        for start in range(len(tokens) - size + 1):
            end = start + size
            if (
                tokens[start:end] in candidates
                and not any(i in occupied for i in range(start, end))
                and not any(i in boundaries for i in range(start + 1, end))
            ):
                spans.append((start, end))
                occupied.update(range(start, end))
    return tuple(sorted(spans))


def learning_breaks(record):
    """Caption spacing marks known units, not inferred pauses or photo wraps."""
    spans = learning_units(record)
    spans += tuple(
        (start, start + 4)
        for start in sorted({start for _, start in idiom_tokens(record).values()})
    )
    return {edge for span in spans for edge in span}


def idiom_tokens(record):
    """Exact contiguous tokens only; preserve source spelling and regrip breaks."""
    tokens = tuple(m.text for m in record.moves)
    boundaries = {*record.regrips, *reading_breaks(record)}
    marked = {}
    start = 0
    while start < len(tokens):
        pattern = tokens[start : start + 4]
        name = IDIOMS.get(pattern)
        if record.category == "F2L" and name and name.startswith("Half "):
            name = None
        if name and not any(i in boundaries for i in range(start + 1, start + 4)):
            for i in range(start, start + 4):
                marked[i] = (name, start)
            start += 4
        else:
            start += 1
    return marked
