"""Lossless move parsing and deterministic, collision-free route grouping."""

from dataclasses import dataclass
from functools import lru_cache
import math
import re

START_RADIUS = 0.135
STATION_RADIUS = 0.075
ENDPOINT_GAP = 0.05

PATTERN = re.compile(r"([RLUDFB]w|[RLUDFBMESrludfbxyz])([23]?)(\'?)")
BASE_DIRECTION = {
    "R": (0, -1),
    "L": (0, 1),
    "M": (0, 1),
    "U": (1, 0),
    "D": (-1, 0),
    "E": (-1, 0),
    "F": (1, 1),
    "B": (-1, -1),
    "S": (1, 1),
    "x": (0, -1),
    "y": (1, 0),
    "z": (1, 1),
}


@dataclass(frozen=True)
class Move:
    text: str
    face: str
    count: int
    prime: bool

    @property
    def wide(self):
        return self.face in "rludfb" or self.face.endswith("w")

    @property
    def base(self):
        return self.face[0].upper() if self.wide else self.face

    @property
    def direction(self):
        x, y = BASE_DIRECTION[self.base]
        return (-x, -y) if self.prime else (x, y)

    @property
    def layer(self):
        if self.base in "xyz":
            return "rotation"
        if self.base in "MES":
            return "slice"
        return "far" if self.base in "LDB" else "near"

    @property
    def cube_token(self):
        face = self.face[0].lower() if self.face.endswith("w") else self.face
        return face + (str(self.count) if self.count != 1 else "") + ("'" if self.prime else "")


def parse_moves(text):
    """Accept compact and spaced notation; normalize prime glyphs only."""
    text = text.replace("′", "'").replace("’", "'")
    result = []
    offset = 0
    while offset < len(text):
        if text[offset].isspace():
            offset += 1
            continue
        match = PATTERN.match(text, offset)
        if match is None:
            raise ValueError(
                f"Unrecognized move at character {offset + 1}: {text[offset : offset + 12]!r}"
            )
        face, count, prime = match.groups()
        result.append(Move(match[0], face, int(count or 1), bool(prime)))
        offset = match.end()
    if not result:
        raise ValueError("An algorithm must contain at least one move")
    return tuple(result)


def segments_intersect(a, b, c, d):
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    def between(p, q, r):
        return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(
            p[1], q[1]
        )

    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    return (
        (o1 * o2 < 0 and o3 * o4 < 0)
        or (o1 == 0 and between(a, b, c))
        or (o2 == 0 and between(a, b, d))
        or (o3 == 0 and between(c, d, a))
        or (o4 == 0 and between(c, d, b))
    )


def trace(moves):
    points = [(0, 0)]
    for move in moves:
        dx, dy = move.direction
        for _ in range(move.count):
            x, y = points[-1]
            points.append((x + dx, y + dy))
    return points


def point_segment_distance(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def endpoint_clearances(moves, insets):
    """Visible ink-to-ink clearance, in quarter-turn units."""
    points = trace(moves)
    first, last = moves[0].direction, moves[-1].direction
    start = tuple(points[0][d] + first[d] * insets[0] for d in (0, 1))
    end = tuple(points[-1][d] - last[d] * insets[1] for d in (0, 1))
    drawn = [start, *points[1:-1], end]
    widths = [(0.03 if m.layer == "slice" else 0.15) for m in moves for _ in range(m.count)]
    result = []
    for n, (p, radius) in enumerate(((start, START_RADIUS), (end, STATION_RADIUS))):
        own = 0 if n == 0 else len(widths) - 1
        gaps = [math.dist(start, end) - START_RADIUS - STATION_RADIUS]
        gaps.extend(math.dist(p, q) - radius - STATION_RADIUS for q in points[1:-1])
        gaps.extend(
            point_segment_distance(p, a, b) - radius - width / 2
            for i, (a, b, width) in enumerate(zip(drawn, drawn[1:], widths))
            if i != own
        )
        result.append(min(gaps))
    return tuple(result)


def route_insets(moves):
    return _route_insets(tuple(moves))


@lru_cache(maxsize=8192)
def _route_insets(moves):
    """Inset each endpoint by its radius and the actual neighboring geometry."""
    points = trace(moves)
    insets = [0.0, 0.0]
    if points[-1] == points[0]:
        a = moves[0].direction
        b = tuple(-v for v in moves[-1].direction)
        al, bl = math.hypot(*a), math.hypot(*b)
        opening = math.dist(tuple(v / al for v in a), tuple(v / bl for v in b))
        if opening:
            distance = (START_RADIUS + STATION_RADIUS + ENDPOINT_GAP) / opening
            insets = [min(0.48, distance / al), min(0.48, distance / bl)]
    for _ in range(4):
        changed = False
        for n in (0, 1):
            if endpoint_clearances(moves, insets)[n] >= ENDPOINT_GAP - 1e-8:
                continue
            low = insets[n]
            high = low
            trial = insets.copy()
            while high < 0.48:
                high = min(0.48, high + 0.02)
                trial = insets.copy()
                trial[n] = high
                if endpoint_clearances(moves, trial)[n] >= ENDPOINT_GAP:
                    break
                low = high
            for _ in range(18):
                mid = (low + high) / 2
                trial[n] = mid
                if endpoint_clearances(moves, trial)[n] >= ENDPOINT_GAP:
                    high = mid
                else:
                    low = mid
            if high > insets[n] + 1e-8:
                changed = True
                insets[n] = high
        if not changed:
            break
    return tuple(insets)


def safe_route(moves):
    # Without arrowheads, same-style collinear tokens must remain separate maps.
    # Otherwise U U and U2 would become indistinguishable.
    for a, b in zip(moves, moves[1:]):
        if a.direction == b.direction and a.layer == b.layer and a.wide == b.wide:
            return False
    points = trace(moves)
    segments = list(zip(points, points[1:]))
    # Endpoint contacts are readable with a small opening; interior crossings
    # and retracing must still be split.
    start_inset, end_inset = route_insets(moves)
    if min(endpoint_clearances(moves, (start_inset, end_inset))) < ENDPOINT_GAP - 1e-7:
        return False
    if start_inset:
        a, b = segments[0]
        segments[0] = ((a[0] + (b[0] - a[0]) * start_inset, a[1] + (b[1] - a[1]) * start_inset), b)
    if end_inset:
        a, b = segments[-1]
        segments[-1] = (a, (b[0] + (a[0] - b[0]) * end_inset, b[1] + (a[1] - b[1]) * end_inset))
    for i, (a, b) in enumerate(segments):
        for j in range(i):
            c, d = segments[j]
            if j == i - 1:
                if b == points[j]:
                    return False
                continue
            if segments_intersect(a, b, c, d):
                return False
    return True


def group_moves(moves, boundaries=(), max_moves=None, measure=None, fits=None, protected=()):
    """Minimize safe reading groups, then isolated moves. Never alter a move.

    Dynamic programming considers later geometry, unlike greedy splitting.
    These groups are not claims about ergonomic finger-trigger boundaries.
    """
    if max_moves is None:
        max_moves = max(1, len(moves))
    if max_moves < 1:
        raise ValueError("max_moves must be positive")
    boundaries = set(boundaries)
    # A learning unit can share a route with neighboring units, but a route
    # boundary must never fall inside it. Spans are half-open token indices.
    forbidden = {i for start, end in protected for i in range(start + 1, end)}
    if boundaries & forbidden:
        raise ValueError("A learning unit crosses an explicit boundary")
    size = len(moves)
    best = {size: ((0, 0, 0), ())}
    for start in range(size - 1, -1, -1):
        if start in forbidden:
            continue
        options = []
        for end in range(start + 1, min(size, start + max_moves) + 1):
            if end not in best:
                continue
            candidate = moves[start:end]
            if any(i in boundaries for i in range(start + 1, end)):
                break
            if len(candidate) > 1 and any(m.layer == "rotation" for m in candidate):
                break
            if not safe_route(candidate):
                continue
            if fits is not None and not fits(candidate):
                continue
            suffix_cost, suffix = best[end]
            cost = (
                1 + suffix_cost[0],
                int(end - start == 1) + suffix_cost[1],
                # Ignore floating-point noise when widths are visually identical.
                # Python versions use different summation algorithms; tied routes
                # must keep the same deterministic longer-first choice everywhere.
                round((measure(candidate) if measure else 0) + suffix_cost[2], 6),
            )
            group = tuple((i, moves[i]) for i in range(start, end))
            options.append((cost, -len(candidate), (group, *suffix)))
        if options:
            cost, _, groups = min(options, key=lambda option: option[:2])
            best[start] = cost, groups
    if 0 not in best:
        raise ValueError("Learning units cannot fit without splitting or obscuring the route")
    return best[0][1]
