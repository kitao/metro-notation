# Metro notation — reading contract

The sheet places the metro diagrams first and standard move symbols beneath them.
The cube has a case number or PLL perm name beneath it. Read a case's routes from left
to right. Each route begins at its yellow station; its ordinary last station is
its end. There is no goal symbol. A closed route has a small opening at the origin. Loop-and-stem shapes (like p, q or の) remain one route when a small inset at the start or end removes the contact. Interior crossings and retraced lines still require a split; move counts and intermediate stations stay unchanged.

One grid interval represents a quarter turn; 2 and 3 retain two and three intervals.
Intermediate white stations mark those intervals. A prime reverses the direction,
including for half turns. Source spelling is preserved in the Markdown master, printed below each route
and retained in SVG metadata. A compact key pairs each line style with a cube showing the moving layer and its direction.

| Unprimed moves | Direction | Style |
| --- | --- | --- |
| R / U / F | up / right / down-right | Black |
| L / D / B | down / left / up-left | Bright blue |
| M / E / S | down / left / down-right | Thin green middle layer |
| r l u d f b (or Rw etc.) | Corresponding face direction | Two narrow parallel rails, original line proportions |
| x / y / z | up / right / down-right | Orange, separate route |

These are schematic rotation directions, not assertions about finger mechanics.
Colors distinguish layers; monochrome printing loses that information.

## Group boundaries

Routes have no fixed move-count cap. Named triggers remain intact. Other groups minimize route count and then single-move fragments, within the available column width and row height. Crossings, backtracking and touching an earlier segment
force a break; returning to the origin at the very end is allowed. Successive
same-style collinear tokens also force a break, so U U does not look like U2.
Source regrips are retained. A rotation has its own route.
These are visual groups, not verified ergonomic trigger groups.

The master preserves printed line breaks, provisional finger hints, regrip positions
and conditional notes separately. They are not badges or instructions on the sheet.
No unconfirmed finger motion or regrip direction is invented.

## Cube setups

A 54-sticker model applies the inverse of each exact algorithm. Centers normalize
colors after whole-cube rotations. F2L shows its active front slot from the appropriate
side, highlighting the target pair while masking irrelevant upper pieces. OLL shows
yellow orientation, PLL surrounding top-layer colors. The bottom of a top view is
its front edge. These are valid inverse-algorithm examples, not copies of all printed
source stickers or permutation arrows.

See [design policy](design-policy.md) and [verification](verification.md).

The left-hand priority green dot follows the source young-leaf selection: 10 OLL and 8 PLL cases; none are inferred for F2L. “Learn first” defines its meaning. Each sheet includes its own notation key, title, project URL and attribution on a white background.

F2L master diagrams use fixed photo-reviewed blue/red/white/gray recognition data,
including hidden-side sticker tiles. They are not ordinary six-color cube views.
Orange move text identifies recurring units, including R/U triggers,
Sledgehammer/Hedgehammer, J triggers and Sune families.
Four-move triggers stay in one route and caption; seven-move Sune families
retain their identity across 3+4 reading shapes. This text color is separate
from the layer colors on metro tracks. See [the full rhythm review](rhythm-review.md).

Basic F2L insertions are protected learning units even when their captions are not highlighted. Adjacent intact units can share a single route; graphical breaks do not imply regrips. Source-specified regrips remain authoritative.
