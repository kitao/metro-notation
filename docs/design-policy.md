# Design policy — Metro Notation 1.0

This is the visual contract for future changes. The goal is a useful cube cheat
sheet with the calm structure of a classic transit map: something worth keeping
on a desk or a wall. Memorability, correct execution and beauty must support each
other. Attractive geometry never justifies changing an algorithm.

## Priority and hierarchy

1. Preserve the exact photo master and source regrips.
2. Make the case and the route readable at the intended physical size.
3. Keep familiar move units intact; use memorable shapes without inventing pauses.
4. Align repeated elements and balance the complete page.
5. Keep decoration subordinate to meaning.

The sheet is an overview, not a learning dashboard. No checkboxes, progress
controls, badges, goal symbols, filled panels or explanatory paragraphs.
Route diagrams are primary; move captions sit below them, and case IDs / PLL
names sit below cubes. Routes read left to right. Cases read down a column, then
continue at the top of the next column.

Every page has `Cube Algorithms: <category>` above `METRO NOTATION 1.0`.
The subtitle comes from the software version. Keep the category in the title,
not isolated at the opposite edge. The compact pictorial key sits to its right.

## Measured geometry

Values are native SVG units unless stated otherwise. Do not scale individual
cases to make them fit. Horizontal, vertical and diagonal strokes share the same
perpendicular thickness; diagonal steps encode an axis and may be longer.

| Element | Value / rule | Reason |
| --- | --- | --- |
| Frame | 1440 × 1006 | Shared composition coordinates |
| Paper | A3 landscape; 6 mm outside the frame on every side | Consistent physical margins |
| Horizontal content inset | 24 | Align title, columns and frame |
| Main title | 28; baseline 44 | Visible hierarchy without dominating |
| Subtitle | 11; baseline 66; letter spacing 1.6 | Compact identity and version |
| Body top | 92; first visible route begins about 98 | Distinct separation below the header |
| Last ordinary case box | ends at 982 | 24-unit lower inset, optically near the title's upper inset |
| Columns | four × 330 for F2L/OLL; three × 448 for PLL | Stable left origins |
| Column gutters | 24 | Separate algorithms without shrinking them |
| Row rhythm | equal pitch within each page; distribute spare height between rows | Avoid a large unused lower margin |
| Cube–route gap | 24 | Separate recognition from execution |
| Quarter-turn step | 24 | Same movement scale everywhere |
| Single track | 3.6 | Same thickness in every direction |
| Wide track | two 0.96 rails, 1.68 clear channel | Two layers, not a decorative hollow line |
| Middle track | 0.72 | Deliberately thin: the middle layer |
| Start | outer radius 3.24, yellow inner radius 2.28 | Identify direction without arrowheads |
| Ordinary station | outer radius 1.8, white inner radius 1.08 | Quarter-turn count and endpoints |
| Endpoint opening | at least 1.20 between visible ink outlines | Consistent gaps despite radii / angles |
| Learn first | solid green circle, radius 3.24, left of cube | Same size as Start; no star / shield / double ring |
| Priority gutter | at least 14 clear units before the cube | Avoid clipping and crowding |
| Footer | 10.5; outside frame, lower right | Attribution does not distort body spacing |

The first row omits unused height above its tallest route. Long cases wrap only
between existing routes, without shrinking. Currently OLL 41 and 42 use two rows;
the cube is centered beside the combined sequence. H-perm's routes and captions
sit 16 units lower than its case label, occupying empty space rather than
protruding upward. Verify at least 12 units of clearance above Ja.

Screen and print use the same native drawing geometry. Narrow screens retain
whole cases in one column; wide screens retain the page's column order. The
four-page gallery uses vector previews from the actual PDF, not resampled PNGs.

## Color and typography

| Meaning | Color |
| --- | --- |
| Near layers: R / U / F | charcoal `#242424` |
| Opposite layers: L / D / B | bright blue `#0099d6` |
| Middle layers: M / E / S | green `#139136` |
| Whole-cube rotation | orange `#e36a00` |
| Familiar unit in move captions | orange `#c94f00`, one color for all idioms |
| Learn first | vivid green `#38b000` |
| Ordinary captions | slate `#4e5d65` |
| Title / subtitle | navy `#203b75` / brick `#a43a32` |
| Frame | blue-gray `#9eb4c2`, width 0.8 |

No unexplained color categories. Track color means a layer; orange **text** means
a familiar unit, not the photo's finger-hint colors. Color remains necessary for
reading opposite layers: do not claim monochrome or color-vision accessibility
without separate validation. Inspect black / blue at reduced size, not just as
large swatches. Keep the two actual narrow rails and the thin middle track.

Titles use Gill Sans, Trebuchet MS and sans-serif fallbacks; captions use Arial,
Helvetica and sans-serif fallbacks. Font availability can change appearance.
Check actual PDF text bounds after a font or platform change. Do not assume
character counts equal proportional text widths. Never simplify lowercase `l`,
`R3` or primes for typographic convenience.

## Legend and recognition diagrams

The first slot stacks Start above Learn first without equals signs. Then show
six physical mappings: near one layer, opposite one layer, middle, near two
layers, opposite two layers, whole cube. Every example runs upward, including
its cube arrows: R, L', M', r, l', x. Equal signs have the same visible gap on
both sides. Black and blue double rails must **both** appear; users must not have
to infer an undocumented combination. Keep the key on every sheet, beside the
title, and distinct from algorithm rows. Screen and print slots are both 124 wide.

F2L uses the 41 fixed photo-reviewed blue/red/white/gray masks. No extra yellow,
orange or green face colors. The two visible side centers read blue then red.
Hidden-side tiles are 14 × 14 rotated squares aligned with the relevant cube
edge, with a 2.5 perpendicular gap and a 1.3 charcoal outline matching face tiles.
A continuous charcoal body fills sticker gaps; no white pinholes at corners.

OLL top patterns have independent photo data. OLL side stickers and PLL diagrams
are reconstructed examples, not complete copies of the photo artwork. Original
PLL permutation arrows and detailed grip directions are not yet transcribed.
Do not describe them as photo-identical or conceal that review boundary.

## Rhythm and movement

A yellow origin begins each route. The ordinary terminal station ends it.
Closed loops, p/q and の shapes are allowed when insetting an endpoint creates
a clear opening. Measure **ink-to-ink** distance using actual circle radii,
track thickness and the neighboring geometry, including diagonal edges.
Do not use one fixed center offset. Interior intersections or retracing require
another route. Quarter-turn stations remain on the original grid.

Source regrips are mandatory route breaks, even if joining looks attractive.
In particular, Ra's initial U stays separate. Whole-cube rotations get their own
route. OLL 25 and 37 read as 4+4. There is no arbitrary four-move route cap.

Four-move named triggers and protected basic insertions stay intact. Recognize
a whole four-move unit before an embedded three-move insertion; do not turn
R U' R' U into 3+1. Adjacent complete units can share one shape. When they do,
use a modest en-space in the caption. A graphical break is not a regrip command.
Sune / Anti-Sune retain their seven-move identity across 3+4 reading shapes.
See [all 119 groupings](rhythm-review.md); changes must preserve source spelling.

## Attribution and distribution

Footer order is author, project URL in parentheses, then the algorithm source:

`© 2020–2026 Takashi Kitao (github.com/kitao/metro-notation) | Algorithm source: tribox CFOP Sheet B-1.0`

The visible URL may omit the scheme; its link must use HTTPS. Link tribox to the
official B-1.0 product. Do not imply tribox endorsement. Full selection/production
credits and the software license belong in the bilingual README, not a MIT badge.

## Change review

After a change, check the **entire four-page composition**, not only the changed
case. Check native size, reduced full-page view, and enlarged problem shapes.
Look for unused bands, drifting columns, unequal gutters, text clipping, false
contacts, inconsistent line weight, weak black/blue distinction, and source drift.
A passing test is evidence for its assertion, not aesthetic or ergonomic approval.
Use [the maintenance checks](maintaining.md) and record limitations honestly.

Reference: [ZEROPERZERO interview](https://dailyportalz.jp/kiji/170530199751).
The relevant principle is to let the subject's structure create its visual
identity. Do not rotate or bend cube routes merely to decorate the page.
