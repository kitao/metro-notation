# Design specification

Metro Notation presents cube algorithms as memorable shapes, using the clarity
and restrained visual style of a transit map. The algorithm is authoritative;
the drawing expresses its movements and rhythm.

## Reading order

- Cases run down each column, then continue at the top of the next column.
- Within a case, routes run left to right. Each starts at a yellow station and
  ends at an ordinary station.
- Routes are primary. Move notation sits below them; case IDs and PLL names sit
  below the recognition cubes.
- A solid green dot to the left of a cube marks the source's Learn first selection.
- Each sheet carries its category title, Metro Notation version, compact legend
  and attribution. The overview contains no study controls or decorative panels.

## Movement notation

One grid interval is a quarter turn. The 2 and 3 suffixes retain two and three
intervals; primes reverse direction, including on half turns. Captions preserve
source spelling, including lowercase wide moves and R3.

| Unprimed moves | Direction | Track |
| --- | --- | --- |
| R / U / F | up / right / down-right | Charcoal `#242424` |
| L / D / B | down / left / up-left | Blue `#0099d6` |
| M / E / S | down / left / down-right | Thin green `#139136` |
| r / l / u / d / f / b | corresponding face direction | Two parallel rails |
| x / y / z | up / right / down-right | Orange `#e36a00`, separate route |

Color identifies the layer; monochrome reproduction loses this distinction.
Intermediate white stations count quarter turns. The double track represents
moving two layers; the thin track represents the middle layer.

## Geometry and layout

Values below are native SVG units. Every case uses the same scale. Stroke
thickness is measured perpendicular to the track, including diagonal segments.

| Element | Specification |
| --- | --- |
| Frame | 1440 × 1006; blue-gray `#9eb4c2`, width 0.8 |
| Paper | A3 landscape; 6 mm outside the frame on all four sides |
| Content inset | 24 horizontally and below the last ordinary case box |
| Title | 28; baseline 44; `Cube Algorithms: <category>` |
| Subtitle | 11; baseline 66; letter spacing 1.6; `METRO NOTATION <version>` |
| Body top | 92; first visible route begins around 98 |
| Columns | four × 330 for F2L/OLL; three × 448 for PLL |
| Column gutter | 24 |
| Row pitch | Equal within each page; distribute spare height between rows |
| Cube–route gap | 24 |
| Quarter-turn step | 24 |
| Single track | 3.6 |
| Wide track | two 0.96 rails with a 1.68 clear channel |
| Middle track | 0.72 |
| Start station | outer radius 3.24; yellow inner radius 2.28 |
| Ordinary station | outer radius 1.8; white inner radius 1.08 |
| Endpoint opening | at least 1.20 between visible ink outlines |
| Learn first dot | radius 3.24; `#38b000`; at least 14 clear units before the cube |
| Footer | 10.5; below the frame, aligned right |

Distribute the four-page PDF and PNG images rendered from it at 300 dpi.
Keep reviewed files in `sheets/`; README thumbnails link to the full PNGs.
HTML/SVG is the rendering source; its local preview
keeps the same columns, margins and legend as the PDF.

Long cases wrap between complete routes at the same scale. OLL 41 and 42 use two
rows, with the cube centered beside the sequence. H-perm's routes and captions sit
16 units below its case label, with at least 12 units of clearance above Ja.

Titles use Cabin Medium / SemiBold. Captions and labels use Arimo Regular.
Embed the fonts in HTML and PDF to retain their metrics. Title color is
`#203b75`, subtitle `#a43a32`, captions `#4e5d65`, footer `#68777d`.
Familiar move units use one orange text color, `#c94f00`.

## Route grouping

- Preserve all source regrips as route boundaries. Ra's initial U remains separate.
- Keep four-move triggers intact, including their caption spacing. Recognize them
  before shorter insertions inside them; R U' R' U must not become 3+1.
- Adjacent complete units can share one shape. Use an en-space between the units
  in its caption. There is no fixed four-move limit.
- Sune and Anti-Sune keep their seven-move identity across 3+4 reading shapes.
  OLL 25 and 37 use 4+4.
- Allow loops and p/q/の shapes when an inset endpoint leaves a clear opening.
  Calculate that opening from the actual station radius and nearby line geometry.
- Split interior intersections, retracing, and repeated collinear moves of the
  same style. U U must remain distinguishable from U2.
- Give whole-cube rotations their own route.

The [grouping table](rhythm-review.md) records all 119 cases. Additional graphical
breaks organize reading; only the original regrip annotations specify a grip change.

## Legend and recognition cubes

The legend sits beside the title. Its first slot stacks Start above Learn first,
without equals signs. Six equal-width slots follow, pairing a track with a cube:
R, L', M', r, l', x. All examples point upward. Slots are 124 wide, with 17 units
of visible space on each side of the equals sign.

F2L uses the fixed photo masks in blue, red, white and gray, with blue/red visible
side centers. A continuous charcoal body fills the sticker gaps. Hidden tiles
are 14 × 14 rotated squares aligned to the cube edge, with a 2.5 perpendicular
gap and a 1.3 charcoal outline. OLL top masks also come from the photographs;
OLL sides and PLL diagrams are computed from the algorithms.

## Attribution

Place this outside the frame, at the lower right:

`© 2020–2026 Takashi Kitao (github.com/kitao/metro-notation) | Algorithm source: tribox CFOP Sheet B-1.0`

Use HTTPS for the project link and the official tribox product page for the source.
Source records belong with the [algorithm data](../data/tribox-cfop-b-1.0/README.md).

## Visual review

Review all four sheets together, each full page, and enlarged difficult cases.
Check the balance above the title and below the last row; header/body separation;
column origins and row rhythm; cube/route spacing; footer clearance; endpoint
openings; line weights; and blue/charcoal distinction at reduced size.
See [CONTRIBUTING.md](../CONTRIBUTING.md) for build and check commands.

Design reference: [ZEROPERZERO interview](https://dailyportalz.jp/kiji/170530199751).
