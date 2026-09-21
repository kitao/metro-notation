"""Data loss, geometry ambiguity, source mistakes and CLI boundaries."""

import contextlib
import hashlib
from html.parser import HTMLParser
from html import unescape
import io
import math
from pathlib import Path
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from metronotation.catalog import Algorithm, load_master, read_markdown
from metronotation.cli import main
from metronotation.cube import self_check, apply, solved_cube
from metronotation.notation import parse_moves, group_moves, safe_route, route_insets
from metronotation.renderer import (
    render_html,
    cube_svg,
    route_svg,
    diagram_groups,
    layer_cube,
    UNIT,
)
from scripts.check_algorithms import read_records, check_structure, up_face


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.cards, self.tokens, self.steps, self.grips = [], {}, {}, {}
        self.active = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "article":
            self.active = a["data-key"]
            self.cards.append(self.active)
            self.tokens[self.active], self.steps[self.active], self.grips[self.active] = [], [], []
        if self.active and "data-index" in a:
            self.tokens[self.active].append((int(a["data-index"]), a["data-move"]))
        if self.active and "data-step" in a:
            self.steps[self.active].append(
                (int(a["data-step"]), a["data-direction"], int(a["data-turns"]), a["data-layer"])
            )
        if self.active and "data-before" in a:
            self.grips[self.active].append(int(a["data-before"]))

    def handle_endtag(self, tag):
        if tag == "article":
            self.active = None


class Integrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_master()

    def test_all119_exact_source_tokens_through_html_and_svg(self):
        # Independent extraction from Markdown, including R3 and prime direction.
        expected = {
            r.kind + "-" + r.id: r.moves for k in ("F2L", "OLL", "PLL") for r in read_records(k)
        }
        self.assertEqual(len(expected), 119)
        for lang in ("en", "ja"):
            doc = Document(render_html(self.records, lang))
            self.assertEqual(set(doc.cards), set(expected))
            self.assertEqual(len(doc.cards), 119)
            for record in self.records:
                with self.subTest(lang=lang, case=record.key):
                    self.assertEqual(doc.tokens[record.key], list(enumerate(expected[record.key])))
                    self.assertEqual(
                        doc.steps[record.key],
                        [
                            (i, f"{m.direction[0]},{m.direction[1]}", m.count, m.layer)
                            for i, m in enumerate(record.moves)
                        ],
                    )
                    self.assertEqual(doc.grips[record.key], sorted(record.regrips))

    def test_photo_reviewed_master_spelling_is_unchanged(self):
        # Freeze the 2026-09-21 photo review, including case order and exact
        # spelling. Updating this requires another source review, not a formatter.
        reviewed = "".join(f"{r.key}\t{r.text}\n" for r in self.records)
        self.assertEqual(
            hashlib.sha256(reviewed.encode()).hexdigest(),
            "2548fef68def591bdc3ab4504de2ce43e707060617fc57bc83ef2ece369a4240",
        )

    def test_photo_reviewed_annotations_are_unchanged(self):
        # P1/P3/P4/P5/P6 review: 117 colored hints, 26 regrips and 18
        # priority marks. Guard their exact positions, not only their counts.
        reviewed = "".join(
            f"{r.key}\t{sorted(r.hints.items())}\t{sorted(r.regrips.items())}\t{r.beginner}\n"
            for r in self.records
        )
        self.assertEqual(
            hashlib.sha256(reviewed.encode()).hexdigest(),
            "62dea3a692f3a66dcc2c8d272b048fe3e0b66e46da53c586d49e3efe39da96ff",
        )

    def test_cube_conventions_and_all_stage_invariants(self):
        self_check()
        for kind in ("F2L", "OLL", "PLL"):
            for record in read_records(kind):
                with self.subTest(case=(kind, record.id)):
                    self.assertIsNone(check_structure(record))

    def test_independent_photo_top_patterns(self):
        masks = dict(
            re.findall(
                r"^\| (\d{2}) \| `([01/]+)` \|$",
                (ROOT / "algorithms/oll-patterns.md").read_text(encoding="utf-8"),
                re.M,
            )
        )
        self.assertEqual(len(masks), 57)
        for record in read_records("OLL"):
            self.assertEqual(up_face(record), masks[record.id], record.id)

    def test_photo_f2l_stickers_solve_forward(self):
        # Start with independently transcribed visible/hidden source stickers,
        # not an inverse of the algorithm under test. Gray stickers stay unknown.
        for record in self.records[:41]:
            diagram = record.recognition
            roles = {
                "B": "F" if diagram.side == 1 else "L",
                "R": "R" if diagram.side == 1 else "F",
                "W": "D",
            }
            cube = {
                position: roles[role] for position, role in diagram.colors.items() if role != "."
            }
            cube.update({(p, n): color for (p, n), color in solved_cube().items() if p == n})
            for move in record.moves:
                cube = apply(cube, move.cube_token)
            centers = {normal: color for (pos, normal), color in cube.items() if pos == normal}
            self.assertTrue(
                all(color == centers[normal] for (pos, normal), color in cube.items()), record.key
            )

    def test_legend_covers_every_used_track_style(self):
        from metronotation.renderer import render_legend

        ns = {"s": "http://www.w3.org/2000/svg"}
        legend = render_legend(1).split("<aside", 1)[0]
        root = ET.fromstring(legend)
        represented = set()
        for edge in root.findall(".//s:g[@data-move]", ns):
            move = parse_moves(edge.get("data-move"))[0]
            represented.add((move.layer, move.wide))
            self.assertEqual(move.direction, (0, -1))
        used = {(move.layer, move.wide) for r in self.records for move in r.moves}
        self.assertEqual(represented, used)

    def test_idiom_color_has_one_meaning(self):
        html = render_html(self.records)
        highlights = re.findall(r'<tspan data-(?:idiom|sequence)=[^>]+style="fill:([^"]+)"', html)
        self.assertTrue(highlights)
        self.assertEqual(set(highlights), {"#c94f00"})

    def test_known_transcription_errors_are_detected(self):
        f2l = next(r for r in read_records("F2L") if r.id == "26")
        f2l.moves[2] = "R'"
        self.assertIsNotNone(check_structure(f2l))
        rb = next(r for r in read_records("PLL") if r.id == "Rb")
        del rb.moves[8]
        self.assertIsNotNone(check_structure(rb))

    def test_state_equivalence_does_not_erase_direction(self):
        for a, b in [("U2", "U2'"), ("R3", "R'")]:
            ma, mb = parse_moves(a)[0], parse_moves(b)[0]
            self.assertEqual(apply(solved_cube(), a), apply(solved_cube(), b))
            self.assertNotEqual((ma.direction, ma.count), (mb.direction, mb.count))
            self.assertNotEqual(
                render_html([Algorithm("CUSTOM", "1", (ma,))]),
                render_html([Algorithm("CUSTOM", "1", (mb,))]),
            )

    def test_parser_and_rejection(self):
        moves = parse_moves("r U2′ R3 Rw’ l2'")
        self.assertEqual([m.text for m in moves], ["r", "U2'", "R3", "Rw'", "l2'"])
        self.assertEqual(moves[3].cube_token, "r'")
        for bad in ("", "R4", "R''", "1", "R ? U", "…", "R2x4", "(R U)", "<script>"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_moves(bad)

    def test_no_route_crossing_or_backtracking(self):
        self.assertTrue(safe_route(parse_moves("R U R' U'")))
        self.assertFalse(safe_route(parse_moves("R R'")))
        self.assertTrue(safe_route(parse_moves("U2 R U' R'")))
        # Loop-and-stem shapes (p/q) are readable from either open endpoint.
        self.assertTrue(safe_route(parse_moves("R2 U R' U'")))
        self.assertTrue(safe_route(parse_moves("U R U' R2")))
        self.assertTrue(safe_route(parse_moves("R U' R' U2")))
        self.assertFalse(safe_route(parse_moves("R U' R' U2 R U' R'")))
        self.assertFalse(safe_route(parse_moves("R R' U R U'")))
        for record in self.records:
            boundaries = tuple(record.regrips)
            groups = group_moves(record.moves, boundaries)
            self.assertEqual([m for g in groups for _, m in g], list(record.moves))
            for g in groups:
                self.assertTrue(safe_route([m for _, m in g]), record.key)
                self.assertFalse(any(i in boundaries for i, _ in g[1:]))
                self.assertTrue(len(g) == 1 or all(m.layer != "rotation" for _, m in g))

    def test_rendered_endpoint_ink_clearance(self):
        from metronotation.notation import point_segment_distance

        ns = {"s": "http://www.w3.org/2000/svg"}
        for record in self.records:
            for group in diagram_groups(record):
                root = ET.fromstring(route_svg(group))
                edges = root.findall("s:g", ns)
                origin = root.find('s:circle[@class="origin"]', ns)
                start = (float(origin.get("cx")), float(origin.get("cy")))
                final_lines = edges[-1].findall("s:line", ns)
                end = tuple(
                    sum(float(e.get(k)) for e in final_lines) / len(final_lines)
                    for k in ("x2", "y2")
                )
                for p, radius, own in (
                    (start, float(origin.get("r")), 0),
                    (end, UNIT * 0.075, len(edges) - 1),
                ):
                    gaps = []
                    for i, edge in enumerate(edges):
                        if i == own:
                            continue
                        for line in edge.findall("s:line", ns):
                            a = tuple(float(line.get(k)) for k in ("x1", "y1"))
                            b = tuple(float(line.get(k)) for k in ("x2", "y2"))
                            gaps.append(
                                point_segment_distance(p, a, b)
                                - radius
                                - float(line.get("stroke-width")) / 2
                            )
                    for circle in root.findall("s:circle", ns):
                        q = tuple(float(circle.get(k)) for k in ("cx", "cy"))
                        if math.dist(p, q) > 1e-3:
                            gaps.append(math.dist(p, q) - radius - float(circle.get("r")))
                    self.assertGreaterEqual(
                        min(gaps), 1.2 - 1e-3, (record.key, [m.text for _, m in group])
                    )
        oll25 = next(r for r in self.records if r.key == "OLL-25")
        self.assertEqual([len(g) for g in diagram_groups(oll25)], [4, 4])
        oll37 = next(r for r in self.records if r.key == "OLL-37")
        self.assertEqual([len(g) for g in diagram_groups(oll37)], [4, 4])

    def test_sune_family_keeps_source_and_phrase_boundaries(self):
        from metronotation.learning import sequence_tokens

        for key, name in (
            ("OLL-27", "Sune"),
            ("OLL-26", "Sune (mirrored)"),
            ("OLL-06", "Wide Anti-Sune"),
        ):
            record = next(r for r in self.records if r.key == key)
            marked = sequence_tokens(record)
            self.assertEqual(set(marked), set(range(7)))
            self.assertEqual(set(marked.values()), {(name, 0)})
            self.assertEqual([len(g) for g in diagram_groups(record)], [3, 4])
        ub = next(r for r in self.records if r.key == "PLL-Ub")
        self.assertFalse(sequence_tokens(ub))

    def test_reviewed_motor_phrases_and_required_geometric_splits(self):
        expected = {
            "F2L-09": [4, 3],
            "F2L-10": [4, 3],
            "F2L-23": [1, 4, 4, 3],
            "OLL-03": [1, 3, 4, 2],
            "OLL-04": [1, 3, 4, 2],
            "OLL-11": [2, 3, 4, 2],
            "OLL-12": [2, 3, 4, 2],
            "OLL-23": [2, 4, 3],
            "OLL-24": [1, 4, 4],
            "OLL-28": [4, 1, 1, 4],
            "PLL-E": [4, 4, 4, 4, 1],
            "PLL-T": [4, 4, 2, 4],
        }
        for record in self.records:
            if record.key in expected:
                self.assertEqual(
                    [len(g) for g in diagram_groups(record)], expected[record.key], record.key
                )
        # Exact photo spelling makes these reversals unavoidable. Do not merge
        # them into retracing strokes or silently replace R r' by a slice move.
        self.assertFalse(safe_route(parse_moves("R r'")))
        self.assertFalse(safe_route(parse_moves("R U R' D R2")))

    def test_typefaces_are_embedded_for_offline_use(self):
        import base64
        from metronotation.typography import stylesheet

        css = stylesheet()
        encoded = re.findall(r"data:font/ttf;base64,([A-Za-z0-9+/=]+)", css)
        self.assertEqual(len(encoded), 3)
        for blob, name in zip(encoded, ("cabin-medium", "cabin-semibold", "arimo-regular")):
            self.assertEqual(
                base64.b64decode(blob),
                (ROOT / f"src/metronotation/assets/fonts/{name}.ttf").read_bytes(),
            )
        self.assertIn("The Cabin Project Authors", css)
        self.assertIn("The Arimo Project Authors", css)
        self.assertEqual(css.count("SIL OPEN FONT LICENSE Version 1.1"), 2)
        self.assertNotRegex(css, r"url\(['\"]?https?://")

    def test_minimal_overview_and_uniform_geometry(self):
        html = render_html(self.records)
        self.assertNotRegex(html, r"<(?:input|button|select|script|marker)\b")
        self.assertNotIn("stroke-dasharray", html)
        self.assertNotIn("#f5f6f6", html)
        self.assertEqual(html.count('class="sheet-heading"'), 4)
        self.assertEqual(html.count('class="sheet-footer"'), 4)
        self.assertEqual(len(re.findall('class="case-label"', html)), 119)
        beginner_keys = {r.key for r in self.records if r.beginner}
        self.assertEqual(
            beginner_keys,
            {
                *(f"OLL-{n:02}" for n in (21, 22, 23, 24, 25, 26, 27, 43, 44, 45)),
                *(f"PLL-{n}" for n in ("Aa", "Ab", "H", "T", "Ua", "Ub", "Y", "Z")),
            },
        )
        self.assertEqual(html.count('class="beginner-mark"'), 18)
        self.assertEqual(len(set(re.findall(r'data-scale="([^"]+)"', html))), 1)
        # Each column has a fixed origin; DOM/source order reads downward.
        for sheet in re.findall(r"<section\b.*?</section>", html, re.S):
            columns = {}
            for attrs in re.findall(r"<article ([^>]+)>", sheet):
                col = int(re.search(r'data-column="(\d+)"', attrs)[1])
                row = int(re.search(r'data-row="(\d+)"', attrs)[1])
                left = re.search(r"left:([^;]+)", attrs)[1]
                span = int(re.search(r'data-span="(\d+)"', attrs)[1])
                columns.setdefault(col, []).append((row, left, span))
            origins = []
            for items in columns.values():
                expected_row = 1
                for row, _, span in items:
                    self.assertEqual(row, expected_row)
                    expected_row += span
                self.assertEqual(len({left for _, left, _ in items}), 1)
                origins.append(float(items[0][1].rstrip("%")))
            self.assertEqual(origins, sorted(set(origins)))
        captions = re.findall(r'<text class="move-caption"[^>]*>(.*?)</text>', html)
        self.assertEqual(
            unescape(re.sub(r"<[^>]+>", "", " ".join(captions))).split(),
            " ".join(r.text for r in self.records).split(),
        )
        self.assertFalse(safe_route(parse_moves("U U")))
        ns = {"s": "http://www.w3.org/2000/svg"}
        count = 0
        for record in self.records:
            for group in diagram_groups(record):
                root = ET.fromstring(route_svg(group))
                self.assertEqual(len(root.findall('s:circle[@class="origin"]', ns)), 1)
                self.assertIsNone(root.find("s:text", ns))
                self.assertIsNone(root.find("s:rect", ns))
                segments = root.findall("s:g", ns)
                for n, ((_, move), segment) in enumerate(zip(group, segments)):
                    lines = segment.findall("s:line", ns)
                    self.assertEqual(len(lines), 2 if move.wide else 1)
                    a = lines[0].attrib
                    delta = tuple(
                        float(a["x2" if d == 0 else "y2"]) - float(a["x1" if d == 0 else "y1"])
                        for d in (0, 1)
                    )
                    start_inset, end_inset = route_insets([m for _, m in group])
                    inset = start_inset * int(n == 0) + end_inset * int(n == len(group) - 1)
                    for d in (0, 1):
                        self.assertAlmostEqual(
                            delta[d], move.direction[d] * UNIT * (move.count - inset), places=4
                        )
                    self.assertEqual(
                        a["stroke"],
                        {
                            "near": "#242424",
                            "far": "#0099d6",
                            "slice": "#139136",
                            "rotation": "#e36a00",
                        }[move.layer],
                    )
                    self.assertAlmostEqual(
                        float(a["stroke-width"]),
                        UNIT * (0.04 if move.wide else (0.03 if move.layer == "slice" else 0.15)),
                    )
                    if move.wide:
                        self.assertEqual(lines[1].get("stroke"), a["stroke"])
                        self.assertAlmostEqual(float(lines[1].get("stroke-width")), UNIT * 0.04)
                        separation = (
                            sum((float(lines[1].get(k)) - float(a[k])) ** 2 for k in ("x1", "y1"))
                            ** 0.5
                        )
                        self.assertAlmostEqual(separation, UNIT * 0.11, places=4)
                    count += 1
        self.assertEqual(count, 1208)

    def test_native_sheet_bounds_and_priority_clearance(self):
        html = render_html(self.records)
        self.assertEqual(set(re.findall(r'data-scale="([^"]+)"', html)), {"1.00000000"})
        ns = {"s": "http://www.w3.org/2000/svg"}
        for sheet in re.findall(r"<section\b.*?</section>", html, re.S):
            bounds = []
            for attrs, body in re.findall(r"<article ([^>]+)>(.*?)</article>", sheet, re.S):
                key = re.search(r'data-key="([^"]+)"', attrs)[1]
                coords = {
                    k: float(v) for k, v in re.findall(r"(left|top|width|height):([\d.]+)%", attrs)
                }
                x, y, w, h = (
                    coords["left"] * 14.4,
                    coords["top"] * 10.06,
                    coords["width"] * 14.4,
                    coords["height"] * 10.06,
                )
                self.assertGreaterEqual(x, 23.99, key)
                self.assertLessEqual(x + w, 1416.01, key)
                self.assertGreaterEqual(y, 87.99, key)
                self.assertLessEqual(y + h, 982.01, key)
                for previous, ax, ay, aw, ah in bounds:
                    overlap = (
                        x < ax + aw - 0.01
                        and ax < x + w - 0.01
                        and y < ay + ah - 0.01
                        and ay < y + h - 0.01
                    )
                    if overlap:
                        self.assertEqual((previous, key), ("PLL-H", "PLL-Ja"))
                        self.assertLessEqual(ay + ah - y, 16.01)
                bounds.append((key, x, y, w, h))
                root = ET.fromstring(body)
                for child in root.findall("s:svg", ns):
                    cx, cy, cw, ch = (float(child.get(k)) for k in ("x", "y", "width", "height"))
                    self.assertGreaterEqual(min(cx, cy), 0, key)
                    self.assertLessEqual(cx + cw, w + 0.01, key)
                    self.assertLessEqual(cy + ch, h + 0.01, key)
                mark = root.find('s:svg[@class="beginner-mark"]', ns)
                if mark is not None:
                    self.assertEqual(len(mark.findall("s:circle", ns)), 1, key)
                    cube = root.find('s:svg[@class="cube-svg"]', ns)
                    self.assertGreaterEqual(
                        float(cube.get("x")) - float(mark.get("x")) - float(mark.get("width")),
                        14,
                        key,
                    )

    def test_equal_columns_and_baseline_grid(self):
        html = render_html(self.records)
        wrapped = []
        for sheet in re.findall(r"<section\b.*?</section>", html, re.S):
            pitch = float(re.search(r"--row-pitch:([\d.]+)", sheet)[1])
            first_height = float(re.search(r"--first-row:([\d.]+)", sheet)[1])
            body_top = float(re.search(r"--body-top:([\d.]+)", sheet)[1])
            row_count = int(re.search(r"--row-count:(\d+)", sheet)[1]) + 1
            body_height = first_height + (row_count - 1) * pitch
            self.assertEqual(body_top, 92)
            self.assertAlmostEqual(1006 - (body_top + body_height), 24)
            widths = set()
            column_x = {}
            for attrs, body in re.findall(r"<article ([^>]+)>(.*?)</article>", sheet, re.S):
                span = int(re.search(r'data-span="(\d+)"', attrs)[1])
                row = int(re.search(r'data-row="(\d+)"', attrs)[1])
                col = int(re.search(r'data-column="(\d+)"', attrs)[1])
                key = re.search(r'data-key="([^"]+)"', attrs)[1]
                widths.add(float(re.search(r"--cell-width:([\d.]+)", attrs)[1]))
                column_x[col] = float(re.search(r"left:([\d.]+)%", attrs)[1]) * 14.4
                top = float(re.search(r"top:([\d.]+)%", attrs)[1]) * 10.06
                self.assertAlmostEqual(
                    top, body_top + (first_height + (row - 2) * pitch if row > 1 else 0), places=5
                )
                ys = [
                    float(v)
                    for v in re.findall(
                        r'<text class="(?:case-label|move-caption)"[^>]* y="([\d.]+)"', body
                    )
                ]
                if span == 1:
                    baseline = (first_height if row == 1 else pitch) - 4
                    expected = {baseline, baseline + 16} if key == "PLL-H" else {baseline}
                    self.assertEqual(len(set(ys)), len(expected), key)
                    for actual, wanted in zip(sorted(set(ys)), sorted(expected)):
                        self.assertAlmostEqual(actual, wanted, places=3, msg=key)
                else:
                    wrapped.append(key)
            self.assertEqual(len(widths), 1)
            origins = list(column_x.values())
            for a, b in zip(origins, origins[1:]):
                self.assertAlmostEqual(b - a, next(iter(widths)) + 24, places=4)
        self.assertEqual(set(wrapped), {"OLL-41", "OLL-42"})

    def test_pictorial_key_layer_membership_and_direction(self):
        ns = {"s": "http://www.w3.org/2000/svg"}
        for symbol, color, stickers, arrows, down in (
            ("R", "#242424", 15, 1, False),
            ("L", "#0099d6", 6, 1, True),
            ("M", "#139136", 6, 1, True),
            ("r", "#242424", 21, 2, False),
            ("L'", "#0099d6", 6, 1, False),
            ("M'", "#139136", 6, 1, False),
            ("l'", "#0099d6", 12, 2, False),
            ("x", "#e36a00", 27, 3, False),
        ):
            root = ET.fromstring(layer_cube(symbol))
            faces = root.findall("s:polygon", ns)
            self.assertEqual(len(faces), 27)
            self.assertEqual(sum(p.get("fill") == color for p in faces), stickers)
            strokes = [p for p in root.findall("s:path", ns) if p.get("stroke") == "white"]
            self.assertEqual(len(strokes), arrows)
            for path in strokes:
                coords = re.findall(r"-?\d+(?:\.\d+)?", path.get("d"))
                self.assertEqual(float(coords[3]) > float(coords[1]), down)

    def test_named_idioms_and_h_perm_clearance(self):
        from metronotation.learning import IDIOMS

        html = render_html(self.records)
        matches = 0
        for record in self.records:
            body = re.search(r'data-key="' + record.key + r'">(.*?)</article>', html, re.S)[1]
            marked = {}
            for name, start, index, token in re.findall(
                r'<tspan data-idiom="([^"]+)" data-idiom-start="(\d+)" data-idiom-index="(\d+)"[^>]*>(.*?)</tspan>',
                body,
            ):
                marked.setdefault((name, int(start)), []).append((int(index), unescape(token)))
            for (name, start), items in marked.items():
                self.assertEqual([i for i, _ in items], list(range(start, start + 4)))
                self.assertEqual(IDIOMS[tuple(t for _, t in items)], name)
                matching_groups = [g for g in diagram_groups(record) if g[0][0] == start]
                self.assertEqual(len(matching_groups), 1, record.key)
                self.assertEqual(
                    [i for i, _ in matching_groups[0]], list(range(start, start + 4)), record.key
                )
                self.assertTrue(safe_route([m for _, m in matching_groups[0]]), record.key)
                captions = re.findall(r'<text class="move-caption"[^>]*>(.*?)</text>', body)
                self.assertEqual(
                    sum(f'data-idiom-start="{start}"' in c for c in captions), 1, record.key
                )
                matches += 1
        self.assertGreater(matches, 20)
        for record in self.records:
            groups = diagram_groups(record)
            self.assertEqual([m for g in groups for _, m in g], list(record.moves))
            for g in groups:
                self.assertTrue(safe_route([m for _, m in g]), record.key)
        self.assertTrue(any(len(g) > 4 for r in self.records for g in diagram_groups(r)))
        ns = {"s": "http://www.w3.org/2000/svg"}
        cards = {
            re.search(r'data-key="([^"]+)"', attrs)[1]: (attrs, ET.fromstring(body))
            for attrs, body in re.findall(r"<article ([^>]+)>(.*?)</article>", html, re.S)
        }

        def shape_vertical_extent(key):
            attrs, root = cards[key]
            top = float(re.search(r"top:([\d.]+)%", attrs)[1]) * 10.06
            boxes = [
                (float(e.get("y")), float(e.get("y")) + float(e.get("height")))
                for e in root.findall("s:svg", ns)
            ]
            boxes += [
                (float(e.get("y")) - float(e.get("font-size")), float(e.get("y")) + 3)
                for e in root.findall("s:text", ns)
            ]
            return top + min(a for a, b in boxes), top + max(b for a, b in boxes)

        self.assertGreaterEqual(
            shape_vertical_extent("PLL-Ja")[0] - shape_vertical_extent("PLL-H")[1], 12
        )

    def test_f2l_recognition_colors_and_hidden_stickers(self):
        from metronotation.renderer import f2l_display
        from metronotation.cube import starting_state

        ns = {"s": "http://www.w3.org/2000/svg"}
        expected_hidden = {
            1: 0,
            2: 0,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 2,
            8: 2,
            9: 2,
            10: 2,
            11: 1,
            12: 1,
            13: 0,
            14: 0,
            15: 1,
            16: 1,
            17: 0,
            18: 0,
            19: 1,
            20: 1,
            21: 2,
            22: 2,
            23: 1,
            24: 1,
        }
        for record in self.records[:41]:
            diagram = record.recognition
            self.assertIsNotNone(diagram)
            root = ET.fromstring(cube_svg(record))
            faces = root.findall('s:polygon[@class="face-sticker"]', ns)
            hidden = root.findall('s:polygon[@class="hidden-sticker"]', ns)
            self.assertEqual(len(faces), 27, record.key)
            self.assertEqual(len(hidden), expected_hidden.get(int(record.id), 0), record.key)
            for tab in hidden:
                points = [tuple(map(float, p.split(","))) for p in tab.get("points").split()]
                self.assertAlmostEqual(
                    math.dist(points[0], points[1]), 14, places=3, msg=record.key
                )
                self.assertAlmostEqual(
                    math.dist(points[1], points[2]), 14, places=3, msg=record.key
                )
                self.assertTrue(all(0 < x < 120 and 0 < y < 120 for x, y in points), record.key)
            self.assertTrue(
                {p.get("fill") for p in faces + hidden}
                <= {"#0866ef", "#f03225", "#ffffff", "#d4d4d4"},
                record.key,
            )
            # Independently retain the fixed photo-reviewed values while checking
            # the cube-model mask, including the edge-only left slot in case 26.
            side, mask = f2l_display(starting_state([m.cube_token for m in record.moves]))
            self.assertEqual(side, diagram.side, record.key)
            for position, color in diagram.colors.items():
                self.assertEqual(mask[position], color, (record.key, position))
            centers = [
                p
                for p in faces
                if p.get("data-position") == p.get("data-normal")
                and p.get("data-normal") != "(0, 1, 0)"
            ]
            centers.sort(key=lambda p: sum(float(v.split(",")[0]) for v in p.get("points").split()))
            self.assertEqual([p.get("data-color") for p in centers], ["B", "R"], record.key)
        self.assertEqual(self.records[25].recognition.side, -1)

    def test_learning_units_survive_visual_grouping(self):
        from metronotation.learning import learning_units, learning_breaks, idiom_tokens

        protected = 0
        for record in self.records:
            cuts = {g[0][0] for g in diagram_groups(record)}
            for start, end in learning_units(record):
                self.assertFalse(cuts.intersection(range(start + 1, end)), record.key)
                self.assertFalse(
                    learning_breaks(record).intersection(range(start + 1, end)), record.key
                )
                protected += 1
            self.assertTrue(set(record.regrips) <= cuts, record.key)
        self.assertGreater(protected, 30)
        # A whole four-move unit must not be labeled as setup + insertion.
        basic = self.records[0]
        self.assertEqual(len(diagram_groups(basic)), 1)
        self.assertEqual(set(idiom_tokens(basic)), set(range(4)))
        reverse = next(r for r in self.records if r.key == "F2L-37")
        self.assertEqual({idiom_tokens(reverse)[i][1] for i in range(4, 8)}, {4})
        # A pair of intact two-move units can form one readable square.
        square = parse_moves("R U R' U'")
        self.assertEqual(len(group_moves(square, protected=((0, 2), (2, 4)))), 1)
        with self.assertRaises(ValueError):
            group_moves(square, boundaries=(1,), protected=((0, 2),))

    def test_master_errors_fail_closed(self):
        raw = (ROOT / "algorithms/f2l.md").read_text(encoding="utf-8")
        for bad in (
            raw.replace("転記済", "要確認", 1),
            raw.replace("P3:U", "P999:U", 1),
            raw.replace("`U R U' R'`", "`U ?`", 1),
        ):
            with self.assertRaises(ValueError):
                read_markdown(bad, "F2L")

    def test_escaped_labels(self):
        record = Algorithm("CUSTOM", "<script>alert(1)</script>", parse_moves("R"))
        document = render_html([record], title="</title><script>alert(1)</script>")
        self.assertNotIn("<script>alert(1)</script>", document)

    def test_cli_protects_master_and_handles_selection(self):
        with (
            tempfile.TemporaryDirectory() as temp,
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            output = Path(temp) / "study.html"
            self.assertEqual(main(["--case", "PLL-Ub", "-o", str(output)]), 0)
            self.assertEqual(Document(output.read_text(encoding="utf-8")).cards, ["PLL-Ub"])
            self.assertEqual(main(["--case", "PLL-nonexistent", "-o", str(output)]), 2)
            self.assertEqual(main(["-o", str(output), "--pdf", str(output)]), 2)
            master = ROOT / "algorithms/f2l.md"
            original = master.read_bytes()
            self.assertEqual(main(["-o", str(master)]), 2)
            self.assertEqual(master.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
