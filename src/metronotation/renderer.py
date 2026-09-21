"""Minimal reference sheets, faithful to the original metro-map visual language."""

from html import escape
import math

from . import __version__
from .typography import stylesheet
from .catalog import SOURCE
from .learning import idiom_tokens, learning_breaks, learning_units, reading_breaks, sequence_tokens
from .cube import starting_state
from .notation import group_moves, trace, parse_moves, route_insets, START_RADIUS, STATION_RADIUS

COLORS = {"near": "#242424", "far": "#0099d6", "slice": "#139136", "rotation": "#e36a00"}
FACE_COLORS = {
    "U": "#ffe500",
    "D": "#ffffff",
    "F": "#0866ef",
    "R": "#f03225",
    "B": "#00a841",
    "L": "#ffa400",
}
UNIT = 24
PAD = 6
TRACK = UNIT * 0.15
RAIL_GAP = UNIT * 0.07
ORIGIN_RADIUS = UNIT * START_RADIUS
PRIORITY_COLOR = "#38b000"
PAGE_INSET = 24
BODY_TOP = 92
BOTTOM_INSET = 24
BODY_HEIGHT = 870


IDIOM_COLOR = "#c94f00"


# Arimo advances in em (compatible with Arial); proportional widths avoid gratuitous line wrapping.
MOVE_ADVANCE = dict(
    zip(
        "RLUDFBMESrludfbxyz23' w",
        (
            0.722,
            0.556,
            0.722,
            0.722,
            0.611,
            0.667,
            0.833,
            0.667,
            0.667,
            0.333,
            0.222,
            0.556,
            0.556,
            0.278,
            0.556,
            0.5,
            0.5,
            0.5,
            0.556,
            0.556,
            0.191,
            0.278,
            0.722,
        ),
    )
)


def svg_open(width, height, title, cls=""):
    return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" role="img" aria-label="{escape(title, quote=True)}">'


def route_size(group, caption_breaks=()):
    points = trace([move for _, move in group])
    xs, ys = zip(*points)
    extra_gaps = sum(i in caption_breaks for i, _ in group[1:])
    caption_width = (
        sum(MOVE_ADVANCE[c] for c in " ".join(m.text for _, m in group)) * 10.5
        + 4
        + extra_gaps * (0.5 - 0.278) * 10.5
    )
    return max(caption_width, max(1, max(xs) - min(xs)) * UNIT + 2 * PAD), max(
        1, max(ys) - min(ys)
    ) * UNIT + 2 * PAD


def route_svg(group, caption_breaks=()):
    """Solid tracks, small white stations and one yellow origin. No decorations.

    A closed path has a small gap at its origin, as in the original renderer.
    Data attributes preserve the exact spelling and step number without ink.
    """
    points = trace([move for _, move in group])
    xs, ys = zip(*points)
    width, height = route_size(group, caption_breaks)
    ox = (width - (max(xs) - min(xs)) * UNIT) / 2 - min(xs) * UNIT
    oy = (height - (max(ys) - min(ys)) * UNIT) / 2 - min(ys) * UNIT

    def point(x, y):
        return x * UNIT + ox, y * UNIT + oy

    parts = [svg_open(width, height, "Metro route", "route-svg")]
    dots = {}
    x = y = 0
    start_inset, end_inset = route_insets([move for _, move in group])
    origin = None
    for n, (index, move) in enumerate(group):
        dx, dy = move.direction
        a = point(x, y)
        x, y = x + dx * move.count, y + dy * move.count
        b = point(x, y)
        if n == 0:
            a = a[0] + dx * UNIT * start_inset, a[1] + dy * UNIT * start_inset
        if n == len(group) - 1:
            b = b[0] - dx * UNIT * end_inset, b[1] - dy * UNIT * end_inset
        color = COLORS[move.layer]
        if origin is None:
            origin = a, color
        attrs = f'x1="{a[0]:.6f}" y1="{a[1]:.6f}" x2="{b[0]:.6f}" y2="{b[1]:.6f}"'
        width_ = UNIT * 0.03 if move.layer == "slice" else TRACK
        parts.append(
            f'<g data-index="{index}" data-move="{escape(move.text, quote=True)}" data-step="{index}" data-direction="{dx},{dy}" data-turns="{move.count}" data-layer="{move.layer}">'
        )
        if move.wide:
            # Draw two actual rails. A white overpaint can erase both thin rails
            # when PDF rasterizers snap the strokes to low-resolution pixels.
            rail = (TRACK - RAIL_GAP) / 2
            offset = (TRACK + RAIL_GAP) / 4
            nx, ny = -dy / math.hypot(dx, dy), dx / math.hypot(dx, dy)
            for sign in (-1, 1):
                ax, ay = a[0] + sign * nx * offset, a[1] + sign * ny * offset
                bx, by = b[0] + sign * nx * offset, b[1] + sign * ny * offset
                parts.append(
                    f'<line x1="{ax:.6f}" y1="{ay:.6f}" x2="{bx:.6f}" y2="{by:.6f}" stroke="{color}" stroke-width="{rail:g}" stroke-linecap="butt"/>'
                )
        else:
            parts.append(
                f'<line {attrs} stroke="{color}" stroke-width="{width_:g}" stroke-linecap="butt"/>'
            )
        parts.append("</g>")

        def station(p):
            dots[p] = color

        station(a)
        station(b)
        # Quarter-turn stations are evenly spaced even when a loop end is inset.
        raw_a = point(x - dx * move.count, y - dy * move.count)
        for q in range(1, move.count):
            station((raw_a[0] + dx * UNIT * q, raw_a[1] + dy * UNIT * q))
    for (cx, cy), color in dots.items():
        parts.append(
            f'<circle cx="{cx:.6f}" cy="{cy:.6f}" r="{UNIT * STATION_RADIUS:g}" fill="{color}"/>'
        )
        parts.append(f'<circle cx="{cx:.6f}" cy="{cy:.6f}" r="{UNIT * 0.045:g}" fill="white"/>')
    (sx, sy), color = origin
    parts.append(
        f'<circle class="origin" cx="{sx:.6f}" cy="{sy:.6f}" r="{ORIGIN_RADIUS:g}" fill="{color}"/>'
    )
    parts.append(f'<circle cx="{sx:.6f}" cy="{sy:.6f}" r="{UNIT * 0.095:g}" fill="#ffd700"/>')
    return "".join(parts) + "</svg>"


def cube_svg(record):
    cube = starting_state([move.cube_token for move in record.moves])
    center = cube[((0, 1, 0), (0, 1, 0))]
    if record.category == "F2L":
        return isometric_cube(cube, record.key, record.recognition)
    positions = (
        [((x, 1, -1), (0, 0, -1)) for x in (-1, 0, 1)]
        + [((1, 1, z), (1, 0, 0)) for z in (-1, 0, 1)]
        + [((x, 1, 1), (0, 0, 1)) for x in (1, 0, -1)]
        + [((-1, 1, z), (-1, 0, 0)) for z in (1, 0, -1)]
        + [((x, 1, z), (0, 1, 0)) for z in (-1, 0, 1) for x in (-1, 0, 1)]
    )
    colors = []
    # Normalize labels to the current centers after any whole-cube rotation.
    centers = {color: normal for (pos, normal), color in cube.items() if pos == normal}
    normal_face = {
        (1, 0, 0): "R",
        (-1, 0, 0): "L",
        (0, 1, 0): "U",
        (0, -1, 0): "D",
        (0, 0, 1): "F",
        (0, 0, -1): "B",
    }
    for position in positions:
        color = cube[position]
        fill = (
            ("#ffe500" if color == center else "#d4d4d4")
            if record.category == "OLL"
            else ("white" if position[1] == (0, 1, 0) else FACE_COLORS[normal_face[centers[color]]])
        )
        colors.append(
            ("#58656b" if fill == "#ffe500" else ("#d4d4d4" if fill == "white" else fill), fill)
        )
    return top_cube(colors, record.key)


def top_cube(colors, title):
    parts = [svg_open(104, 104, title + " setup", "cube-svg")]
    for i, (stroke, fill) in enumerate(colors):
        if i < 3:
            x, y, w, h = 18 + i * 23, 5, 20, 8
        elif i < 6:
            x, y, w, h = 91, 18 + (i - 3) * 23, 8, 20
        elif i < 9:
            x, y, w, h = 18 + (8 - i) * 23, 91, 20, 8
        elif i < 12:
            x, y, w, h = 5, 18 + (11 - i) * 23, 8, 20
        else:
            x, y, w, h = 18 + (i - 12) % 3 * 23, 18 + (i - 12) // 3 * 23, 20, 20
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="0" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>'
        )
    return "".join(parts) + "</svg>"


def f2l_display(cube):
    """Photo-style recognition mask, separate from physical cube face colors."""
    centers = {normal: color for (pos, normal), color in cube.items() if pos == normal}
    slots = [
        side
        for side in (-1, 1)
        if any(
            color != centers[normal]
            for (pos, normal), color in cube.items()
            if pos[0] == side and pos[2] == 1 and pos[1] in (-1, 0)
        )
    ]
    if len(slots) != 1:
        raise ValueError("F2L diagram needs exactly one unfinished front slot")
    side = slots[0]
    front, flank, down = (centers[n] for n in ((0, 0, 1), (side, 0, 0), (0, -1, 0)))
    roles = {front: "B" if side == 1 else "R", flank: "R" if side == 1 else "B", down: "W"}
    target = {front, flank}
    pieces = {}
    for (pos, normal), color in cube.items():
        pieces.setdefault(pos, set()).add(color)
    mask = {}
    for (pos, normal), color in cube.items():
        active = pieces[pos] in (target, target | {down})
        slot = pos[0] == side and pos[2] == 1 and pos[1] in (-1, 0)
        show = active or (pos[1] < 1 and not slot and normal[1] == 0)
        mask[pos, normal] = roles.get(color, ".") if show else "."
    return side, mask


def isometric_cube(cube, title, recognition=None):
    side, mask = (recognition.side, recognition.colors) if recognition else f2l_display(cube)
    palette = {"B": "#0866ef", "R": "#f03225", "W": "#ffffff", ".": "#d4d4d4"}

    def project(p):
        x, y, z = p
        return (
            60 + x * (28 if side == 1 else 18) - side * z * (18 if side == 1 else 28),
            64 + x * (8 if side == 1 else -12) + z * (12 if side == 1 else 8) - y * 28,
        )

    parts = [svg_open(120, 120, title + " recognition diagram", "cube-svg")]
    # Hidden U-layer side stickers are laid just outside the top-face silhouette.
    for normal in ((-side, 0, 0), (0, 0, -1)):
        fixed = 0 if normal[0] else 2
        tangent = 2 if fixed == 0 else 0
        for col in (-1, 0, 1):
            pos = list(normal)
            pos[1], pos[tangent] = 1, col
            role = mask.get((tuple(pos), normal), ".")
            if role == ".":
                continue
            # A tile-sized square follows the corresponding cube edge. Keep
            # its shape and clearance identical on both hidden faces.
            point = [0, 1, 0]
            point[fixed] = normal[fixed]
            point[tangent] = col / 1.5
            edge = project(point)
            point[tangent] += 1
            end = project(point)
            dx, dy = end[0] - edge[0], end[1] - edge[1]
            length = math.hypot(dx, dy)
            tx, ty = dx / length, dy / length
            nx, ny = -ty, tx
            center = project((0, 1, 0))
            if nx * (edge[0] - center[0]) + ny * (edge[1] - center[1]) < 0:
                nx, ny = -nx, -ny
            corners = [
                (edge[0] + tx * a + nx * b, edge[1] + ty * a + ny * b)
                for a, b in ((-7, 2.5), (7, 2.5), (7, 16.5), (-7, 16.5))
            ]
            coords = " ".join(f"{x:g},{y:g}" for x, y in corners)
            parts.append(
                f'<polygon class="hidden-sticker" data-position="{tuple(pos)}" data-normal="{normal}" data-color="{role}" points="{coords}" fill="{palette[role]}" stroke="#303638" stroke-width="1.3" stroke-linejoin="round"/>'
            )
    # One continuous body under all stickers prevents white pinholes where
    # the separately outlined tile corners meet.
    outline = [
        project(p)
        for p in (
            (-side, 1, -1),
            (side, 1, -1),
            (side, -1, -1),
            (side, -1, 1),
            (-side, -1, 1),
            (-side, 1, 1),
        )
    ]
    coords = " ".join(f"{x:g},{y:g}" for x, y in outline)
    parts.append(f'<polygon class="cube-body" points="{coords}" fill="#303638"/>')
    for normal, axes in (((0, 1, 0), (0, 2)), ((0, 0, 1), (0, 1)), ((side, 0, 0), (2, 1))):
        fixed = next(i for i, v in enumerate(normal) if v)
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                pos = list(normal)
                pos[axes[0]], pos[axes[1]] = row, col
                corners = []
                for a, b in ((-0.46, -0.46), (0.46, -0.46), (0.46, 0.46), (-0.46, 0.46)):
                    point = [v / 1.5 for v in pos]
                    point[fixed] = normal[fixed]
                    point[axes[0]] = (row + a) / 1.5
                    point[axes[1]] = (col + b) / 1.5
                    corners.append(project(point))
                role = mask.get((tuple(pos), normal), ".")
                coords = " ".join(f"{x:g},{y:g}" for x, y in corners)
                parts.append(
                    f'<polygon class="face-sticker" data-position="{tuple(pos)}" data-normal="{normal}" data-color="{role}" points="{coords}" fill="{palette[role]}" stroke="#303638" stroke-width="1.3" stroke-linejoin="round"/>'
                )
    return "".join(parts) + "</svg>"


def diagram_groups(record):
    # Source regrips are mandatory route breaks, even for joinable loop/stem
    # shapes. Named triggers stay intact only when they contain no regrip.
    starts = sorted({start for _, start in idiom_tokens(record).values()})
    groups = []
    cursor = 0
    boundaries = (*record.regrips, *reading_breaks(record))
    protected = learning_units(record)
    room = 356 if record.category == "PLL" else 238
    height_limit = {"F2L": 64, "OLL": 94, "PLL": 112}.get(record.category, 92)

    def extent(ms):
        return route_size(tuple(enumerate(ms)))

    def fits(ms):
        width, height = extent(ms)
        return width <= room and height <= height_limit

    for start in [*starts, len(record.moves)]:
        if cursor < start:
            for group in group_moves(
                record.moves[cursor:start],
                [i - cursor for i in boundaries if cursor < i < start],
                max_moves=start - cursor,
                measure=lambda ms: extent(ms)[0],
                fits=fits,
                protected=[
                    (a - cursor, b - cursor) for a, b in protected if cursor <= a and b <= start
                ],
            ):
                groups.append(tuple((i + cursor, move) for i, move in group))
        if start < len(record.moves):
            groups.append(tuple((i, record.moves[i]) for i in range(start, start + 4)))
            cursor = start + 4
    return tuple(groups)


def case_route_size(record, group):
    return route_size(group, learning_breaks(record))


def case_size(record):
    groups = diagram_groups(record)
    sizes = [case_route_size(record, group) for group in groups]
    return 92 + sum(w for w, h in sizes) + 8 * (len(sizes) - 1), max(
        42, *(h for w, h in sizes)
    ) + 18


def place_svg(svg, x, y, width, height):
    return svg.replace(
        "<svg ", f'<svg x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" ', 1
    )


def case_lines(record, width, pitch):
    """Wrap only between intact route groups; keep every diagram at native size."""
    groups = diagram_groups(record)
    room = width - 92
    best = {len(groups): (0, 0, ())}
    for start in range(len(groups) - 1, -1, -1):
        options = []
        used = 0
        for end in range(start + 1, len(groups) + 1):
            used += case_route_size(record, groups[end - 1])[0] + (8 if end > start + 1 else 0)
            if used > room + 0.001:
                break
            height = max(42, *(route_size(g)[1] for g in groups[start:end]))
            span = math.ceil((height + 16) / pitch)
            tail_span, tail_cost, tail = best[end]
            options.append(
                (
                    span + tail_span,
                    (room - used) ** 2 + tail_cost,
                    ((groups[start:end], span), *tail),
                )
            )
        if not options:
            raise ValueError(f"{record.key}: a route exceeds column width")
        best[start] = min(options, key=lambda x: x[:2])
    return best[0][2]


def render_case(record, cell_width, cell_height, scale, x, y, pitch, top_trim=0):
    key = escape(record.key, quote=True)
    lines = case_lines(record, cell_width, pitch)
    idioms = idiom_tokens(record)
    sequences = sequence_tokens(record)
    caption_breaks = learning_breaks(record)
    parts = [svg_open(cell_width, cell_height, record.key, "case-map")]
    first_baseline = lines[0][1] * pitch - 4 - top_trim
    baselines = [first_baseline]
    for groups, _ in lines[1:]:
        # Continuation stays closer to its own line than to the next case.
        baselines.append(baselines[-1] + max(42, *(route_size(g)[1] for g in groups)) + 28)
    first_center = baselines[0] - 12 - max(42, *(route_size(g)[1] for g in lines[0][0])) / 2
    last_center = baselines[-1] - 12 - max(42, *(route_size(g)[1] for g in lines[-1][0])) / 2
    label_y = first_baseline if len(lines) == 1 else (first_center + last_center) / 2 + 33
    cube_bottom = label_y - 12
    parts.append(place_svg(cube_svg(record), 26, cube_bottom - 42, 42, 42))
    if record.beginner:
        parts.append(
            f'<svg class="beginner-mark" x="2" y="{cube_bottom - 26:g}" width="10" height="10" viewBox="0 0 10 10" role="img" aria-label="Learn first: source priority">'
            f'<circle cx="5" cy="5" r="{ORIGIN_RADIUS:g}" fill="{PRIORITY_COLOR}"/>'
            "</svg>"
        )
    label = record.id if record.category == "PLL" else f"{record.category} {record.id}"
    parts.append(
        f'<text class="case-label" x="47" y="{label_y:g}" font-size="10.5" text-anchor="middle">{escape(label)}</text>'
    )
    for (groups, span), caption_y in zip(lines, baselines):
        caption_y += 16 if record.key == "PLL-H" else 0
        route_x = 92
        for group in groups:
            width, height = route_size(group, caption_breaks)
            first = group[0][0]
            if first in record.regrips:
                parts.append(f'<g data-before="{first}" data-regrip="{record.regrips[first]}"></g>')
            words = []
            for index, move in group:
                word = escape(move.text)
                if index in idioms:
                    name, start = idioms[index]
                    word = f'<tspan data-idiom="{name}" data-idiom-start="{start}" data-idiom-index="{index}" style="fill:{IDIOM_COLOR}">{word}</tspan>'
                elif index in sequences:
                    name, start = sequences[index]
                    word = f'<tspan data-sequence="{name}" data-sequence-start="{start}" data-sequence-index="{index}" style="fill:{IDIOM_COLOR}">{word}</tspan>'
                if index != first:
                    gap = (
                        f'<tspan data-unit-start="{index}">\u2002</tspan>'
                        if index in caption_breaks
                        else " "
                    )
                    word = gap + word
                words.append(word)
            caption = "".join(words)
            parts.append(
                f'<text class="move-caption" x="{route_x + width / 2:g}" y="{caption_y:g}" font-size="10.5" text-anchor="middle">{caption}</text>'
            )
            parts.append(
                place_svg(
                    route_svg(group, caption_breaks=caption_breaks),
                    route_x,
                    caption_y - 12 - height,
                    width,
                    height,
                )
            )
            route_x += width + 8
    parts.append("</svg>")
    return f'<article class="case" style="--cell-width:{cell_width:g}px;--cell-height:{cell_height:g}px;left:{x / 1440 * 100:.8f}%;top:{y / 1006 * 100:.8f}%;width:{cell_width / 1440 * 100:.8f}%;height:{cell_height / 1006 * 100:.8f}%" data-key="{key}">{"".join(parts)}</article>'


def layer_cube(symbol):
    """Show actual layer membership and front-sticker motion, without move text."""
    move = parse_moves(symbol)[0]
    selected = {"R": {1}, "L": {-1}, "M": {0}, "r": {0, 1}, "l": {-1, 0}, "x": {-1, 0, 1}}[
        move.face
    ]
    upward = move.direction == (0, -1)
    color = COLORS[move.layer]

    def project(x, y, z):
        return 60 + (x - z) * 24, 64 + (x + z) * 12 - y * 28

    parts = [svg_open(120, 120, "Moving layers and direction", "layer-cube")]
    for normal, axes, base in (
        ((0, 1, 0), (0, 2), "#f1f1f1"),
        ((0, 0, 1), (0, 1), "#dedede"),
        ((1, 0, 0), (2, 1), "#c6c6c6"),
    ):
        fixed = next(i for i, v in enumerate(normal) if v)
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                pos = list(normal)
                pos[axes[0]], pos[axes[1]] = col, row
                corners = []
                for da, db in ((-0.47, -0.47), (0.47, -0.47), (0.47, 0.47), (-0.47, 0.47)):
                    point = [v / 1.5 for v in pos]
                    point[fixed] = normal[fixed]
                    point[axes[0]], point[axes[1]] = (col + da) / 1.5, (row + db) / 1.5
                    corners.append(project(*point))
                active = pos[0] in selected
                coords = " ".join(f"{x:g},{y:g}" for x, y in corners)
                parts.append(
                    f'<polygon points="{coords}" fill="{color if active else base}" stroke="{"#eee" if active else "#aaa"}" stroke-width=".8"/>'
                )
    for col in sorted(selected):
        x1, y1 = project(col / 1.5, -0.62 if upward else 0.62, 1.025)
        x2, y2 = project(col / 1.5, 0.62 if upward else -0.62, 1.025)
        direction = -1 if upward else 1
        parts.append(
            f'<path d="M{x1:g} {y1:g} L{x2:g} {y2 - direction * 4:g}" stroke="white" stroke-width="5"/>'
        )
        parts.append(
            f'<path d="M{x2:g} {y2:g} L{x2 - 5:g} {y2 - direction * 8:g} L{x2 + 5:g} {y2 - direction * 8:g} Z" fill="white"/>'
        )
    return "".join(parts) + "</svg>"


def render_legend(scale):
    """A label pair precedes six physical mappings with equal visible gaps."""

    def equals(cx, cy):
        return "".join(
            f'<line x1="{cx - 3 * scale:g}" y1="{cy + dy * scale:g}" x2="{cx + 3 * scale:g}" y2="{cy + dy * scale:g}" stroke="#68777d" stroke-width="{0.8 * scale:g}"/>'
            for dy in (-1.5, 1.5)
        )

    def label_pair(priority=False):
        cy = 46 if priority else 18
        if priority:
            symbol = (
                f'<circle cx="18" cy="{cy}" r="{ORIGIN_RADIUS * scale:g}" fill="{PRIORITY_COLOR}"/>'
            )
            edge, label = 18 + ORIGIN_RADIUS * scale, "Learn first"
        else:
            symbol = (
                f'<circle cx="18" cy="{cy}" r="{ORIGIN_RADIUS * scale:g}" fill="{COLORS["near"]}"/>'
                f'<circle cx="18" cy="{cy}" r="{UNIT * 0.095 * scale:g}" fill="#ffd700"/>'
            )
            edge, label = 18 + ORIGIN_RADIUS * scale, "Start"
        cls = "priority-key" if priority else ""
        return (
            symbol
            + f'<text class="{cls}" x="{edge + 14 * scale:g}" y="{cy + 4}" font-size="11">{label}</text>'
        )

    items = [label_pair() + label_pair(True)]
    for symbol in ("R", "L'", "M'", "r", "l'", "x"):
        group = ((-1, parse_moves(symbol)[0]),)
        width, height = route_size(group)
        equal_x = (width / 2 + ORIGIN_RADIUS + 17) * scale
        cube_x = equal_x + (17 - 12.08 * 52 / 120) * scale
        items.append(
            place_svg(route_svg(group), 0, 32 - height * scale / 2, width * scale, height * scale)
            + equals(equal_x, 32)
            + place_svg(
                layer_cube(symbol), cube_x, 32 - 64 * 52 / 120 * scale, 52 * scale, 52 * scale
            )
        )
    parts = [svg_open(1440, 100, "How to read the diagrams", "notation-key")]
    for i, item in enumerate(items):
        parts.append(
            f'<svg x="{552 + i * 124}" y="14" width="124" height="64" viewBox="0 0 124 64">{item}</svg>'
        )
    return "".join(parts) + "</svg>"


def page_identity(category, batch):
    label = category if category != "OLL" else f"OLL {batch[0].id}–{batch[-1].id}"
    frame = (
        svg_open(1440, 1006, "Sheet frame", "sheet-frame")
        + '<rect x=".4" y=".4" width="1439.2" height="1005.2" fill="none" stroke="#9eb4c2" stroke-width=".8"/></svg>'
    )
    heading = (
        frame
        + svg_open(1440, 96, "Cube Algorithms — Metro Notation", "sheet-heading")
        + f'<text class="sheet-title" x="24" y="44">Cube Algorithms: {escape(label)}</text>'
        + f'<text class="notation-signature" x="24" y="66">METRO NOTATION {escape(__version__)}</text></svg>'
    )
    footer = (
        svg_open(1440, 24, "Attribution", "sheet-footer")
        + '<text x="1440" y="16" font-size="10.5" text-anchor="end">© 2020–2026 Takashi Kitao ('
        + '<a href="https://github.com/kitao/metro-notation">github.com/kitao/metro-notation</a>) | Algorithm source: <a href="https://store.tribox.com/products/detail.php?product_id=3973">tribox CFOP Sheet B-1.0</a></text></svg>'
    )
    return heading, footer


def column_layout(records):
    """Equal columns and a fixed baseline grid, reading down then right."""
    category = records[0].category
    pitch = {"F2L": 80, "OLL": 110, "PLL": 128}.get(category, 108)
    count = min(3 if category == "PLL" else 4, len(records))
    gap = 24
    width = (1440 - 2 * PAGE_INSET - gap * (count - 1)) / count
    capacity = math.ceil(BODY_HEIGHT / pitch)
    spans = [sum(span for _, span in case_lines(r, width, pitch)) for r in records]
    candidates = []

    def partition(start, remaining, columns, loads):
        if not remaining:
            if start == len(records):
                first_height = max(
                    max(42, *(route_size(g)[1] for g in case_lines(c[0], width, pitch)[0][0])) + 16
                    for c in columns
                )
                if (max(loads) - 1) * pitch + first_height <= BODY_HEIGHT:
                    score = (
                        max(loads) - min(loads),
                        sum(n * n for n in loads),
                        tuple(-n for n in loads),
                    )
                    candidates.append((score, columns, loads, first_height))
            return
        used = 0
        for end in range(start + 1, len(records) - remaining + 2):
            used += spans[end - 1]
            if used > capacity:
                break
            partition(end, remaining - 1, columns + [records[start:end]], loads + [used])

    partition(0, count, [], [])
    if not candidates:
        return None
    _, columns, loads, first_height = min(candidates, key=lambda item: item[0])
    # Anchor the list below the header and distribute remaining height across
    # the row rhythm. The lower frame inset then matches the title's top inset.
    if max(loads) > 1:
        pitch = (1006 - BODY_TOP - BOTTOM_INSET - first_height) / (max(loads) - 1)
    return columns, width, pitch, max(loads), gap, first_height


def render_html(records, lang="en", title=None):
    if lang not in ("en", "ja"):
        raise ValueError("Supported languages: en, ja")
    if not records or len({r.key for r in records}) != len(records):
        raise ValueError("A document needs unique, non-empty case IDs")
    title = title or f"Cube Algorithms — Metro Notation {__version__}"
    scale = 1.0
    sheets = []
    for category in dict.fromkeys(r.category for r in records):
        cases = [r for r in records if r.category == category]
        limit = 21 if category == "PLL" else (30 if category == "OLL" else 44)
        offset, number = 0, 1
        while offset < len(cases):
            count = min(limit, len(cases) - offset)
            while count:
                batch = cases[offset : offset + count]
                layout = column_layout(batch)
                if layout is not None:
                    columns, width, pitch, row_count, column_gap, first_height = layout
                    break
                count -= 1
            if not count:
                raise ValueError("An algorithm exceeds the sheet at native size")
            cards = []
            body_top = BODY_TOP
            for col_index, column in enumerate(columns):
                x = PAGE_INSET + col_index * (width + column_gap)
                row_index = 0
                for r in column:
                    span = sum(n for _, n in case_lines(r, width, pitch))
                    top_trim = pitch - first_height if row_index == 0 else 0
                    height = span * pitch - top_trim + (16 if r.key == "PLL-H" else 0)
                    y = body_top + (first_height + (row_index - 1) * pitch if row_index else 0)
                    card = render_case(r, width, height, scale, x, y, pitch, top_trim)
                    card = card.replace(
                        'style="',
                        f'style="--column:{col_index + 1};--row:{row_index + 2};--span:{span};',
                        1,
                    )
                    card = card.replace(
                        'class="case"',
                        f'class="case" data-column="{col_index + 1}" data-row="{row_index + 1}" data-span="{span}"',
                        1,
                    )
                    cards.append(card)
                    row_index += span
            heading, footer = page_identity(category, batch)
            sheet_key = escape(f"{category}-{number}", quote=True)
            column_css = " ".join(f"{width:g}px" for _ in columns)
            sheets.append(
                f'<section class="sheet" style="--body-top:{body_top:g}px;--columns:{column_css};--column-gap:{column_gap:g}px;--row-pitch:{pitch}px;--first-row:{first_height}px;--row-count:{row_count - 1};--footer-row:{row_count + 2}" id="{sheet_key}" aria-label="{sheet_key}" data-columns="{len(columns)}" data-scale="{scale:.8f}" data-cases="{len(batch)}"><div class="sheet-content">{heading}{render_legend(scale)}{"".join(cards)}{footer}</div></section>'
            )
            offset += count
            number += 1
    css = stylesheet()
    source = SOURCE if all(r.source == SOURCE for r in records) else "User algorithms"
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="source" content="{escape(source, quote=True)}"><title>{escape(title)}</title><style>{css}</style></head>
<body><main>{"".join(sheets)}</main></body></html>'''
