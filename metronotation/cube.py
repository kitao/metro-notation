"""Integer 54-sticker cube model; display direction is preserved in notation."""

import re

TOKEN = re.compile(r"([RLUDFBMESrludfbxyz])([23]?)(\'?)\Z")
FACE_NORMALS = {
    "R": (1, 0, 0),
    "L": (-1, 0, 0),
    "U": (0, 1, 0),
    "D": (0, -1, 0),
    "F": (0, 0, 1),
    "B": (0, 0, -1),
}
# axis, selected layers, clockwise quarter turn around the positive axis
MOVES = {
    "R": (0, (1,), -1),
    "L": (0, (-1,), 1),
    "U": (1, (1,), -1),
    "D": (1, (-1,), 1),
    "F": (2, (1,), -1),
    "B": (2, (-1,), 1),
    "M": (0, (0,), 1),
    "E": (1, (0,), 1),
    "S": (2, (0,), -1),
    "x": (0, (-1, 0, 1), -1),
    "y": (1, (-1, 0, 1), -1),
    "z": (2, (-1, 0, 1), -1),
}
for face in "RLUDFB":
    axis, layers, direction = MOVES[face]
    MOVES[face.lower()] = axis, (0, *layers), direction


def rotate(vector, axis, turns):
    x, y, z = vector
    for _ in range(turns % 4):
        if axis == 0:
            y, z = -z, y
        elif axis == 1:
            x, z = z, -x
        else:
            x, y = -y, x
    return x, y, z


def solved_cube():
    cube = {}
    for color, normal in FACE_NORMALS.items():
        axis = next(i for i, n in enumerate(normal) if n)
        for a in range(-1, 2):
            for b in range(-1, 2):
                pos = list(normal)
                other_axes = [i for i in range(3) if i != axis]
                pos[other_axes[0]], pos[other_axes[1]] = a, b
                cube[tuple(pos), normal] = color
    return cube


def apply(cube, token, inverse=False):
    match = TOKEN.fullmatch(token)
    if match is None:
        raise ValueError(f"Invalid move: {token!r}")
    face, count, prime = match.groups()
    axis, layers, direction = MOVES[face]
    turns = direction * int(count or 1) * (-1 if prime else 1)
    turns *= -1 if inverse else 1
    result = {}
    for (pos, normal), color in cube.items():
        if pos[axis] in layers:
            pos = rotate(pos, axis, turns)
            normal = rotate(normal, axis, turns)
        result[pos, normal] = color
    return result


def run_moves(moves):
    cube = solved_cube()
    for move in moves.split():
        cube = apply(cube, move)
    return cube


def self_check():
    original = solved_cube()
    assert len(original) == 54
    for face in MOVES:
        assert run_moves(" ".join([face] * 4)) == original
        assert run_moves(f"{face} {face}'") == original
        assert run_moves(f"{face}2") == run_moves(f"{face}2'")
        assert run_moves(f"{face}3") == run_moves(f"{face}'")
    for left, right in (
        ("r", "R M'"),
        ("l", "L M"),
        ("u", "U E'"),
        ("d", "D E"),
        ("f", "F S"),
        ("b", "B S'"),
        ("x", "R M' L'"),
        ("y", "U E' D'"),
        ("z", "F S B'"),
    ):
        assert run_moves(left) == run_moves(right), (left, right)
    # R sends the UF-side sticker at URF to the back side of URB.
    r = run_moves("R")
    assert r[((1, 1, -1), (0, 0, -1))] == "U"
    assert r[((1, 1, -1), (0, 1, 0))] == "F"


def starting_state(tokens):
    cube = solved_cube()
    for token in reversed(tokens):
        cube = apply(cube, token, inverse=True)
    return cube
