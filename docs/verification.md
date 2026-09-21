# Verification record — Metro Notation 1.0

Checked locally on 2026-09-21 with Python 3.12. This record separates verified
properties from work that remains; it does not claim universal cuber approval.

## Master and cube states

- 119 cases: 41 F2L, 57 OLL and 21 PLL; 1,208 exact move tokens and 26 regrips.
- Six original photographs are guarded by SHA-256 checksums. The reviewed master
  spelling has a separate regression hash. `R3`, lowercase wide moves and primed
  half turns survive unchanged in SVG captions and extracted PDF text.
- All 41 independently transcribed F2L recognition diagrams solve forward under
  their source algorithms: every known sticker reaches its solved face. Unknown
  stickers are excluded rather than inferred from the algorithm being tested.
- All 119 inverse states satisfy their stage invariants. All 57 independently
  transcribed OLL upper-face masks match. Negative tests detect known F2L 26 and
  PLL Rb transcription errors.
- Source regrips are mandatory group boundaries. Named learning units and curated
  reading phrases are checked against the unchanged master. The generated
  [119-case rhythm review](rhythm-review.md) records the resulting divisions.

These checks complement photo comparison. Inverse-then-forward simulation alone
would not prove transcription accuracy and is not treated as that proof here.

## Drawing and layout

The automated suite contains 23 tests. It checks actual SVG geometry, rather than
only drawing metadata, for all 1,208 moves: directions, quarter-turn counts,
colors, line widths and double-rail separation. It also checks:

- A single yellow start and no goal marker per route; a 1.20-unit minimum visible
  endpoint-to-edge gap that accounts for circle size and diagonal edges.
- Equal columns and row rhythm, consistent route scale, case bounds, clipping,
  long-case wrapping and clearance below H perm.
- All 41 fixed F2L masks, 24 equal diamond markers and source recognition colors.
- The compact legend's six physical layer mappings, including opposite-side wide
  moves; all mappings point upward. Start and Learn first share the first slot.
- One orange caption color for familiar move units; a solid green Learn first dot.

All four PDF sheets are rendered for visual review. Numeric checks do not replace
inspection of alignment, optical balance, small-size clarity and whitespace.
The design values and rationale live in [design-policy.md](design-policy.md).

## Output and packaging

The PDF audit checks four A3 landscape pages, all 119 labels and 1,208 exact move
tokens, every title/version/key/credit, 6 mm frame margins on every edge, and a
footer outside the lower frame. Only link annotations are allowed; no forms or
progress checkboxes are inserted. Routes remain vector artwork.

HTML generation uses the Python standard library. PDF conversion uses optional
Playwright/Chromium; gallery previews use Poppler. The wheel includes its Markdown
master and CSS. A clean installation is exercised outside the source checkout.
The retired text-format reader and duplicate legacy algorithm files are removed.
CI checks Linux and Windows on Python 3.10 and 3.14; consult the repository's
Actions results for the status of a particular commit.

For repeatable commands, see [maintaining.md](maintaining.md). Publishing the
website does not constitute a release or close the remaining verification gaps.

## Remaining limits

Finger hints remain provisional photo transcriptions. Detailed hand illustrations,
regrip directions and every OLL/PLL source sticker or permutation arrow have not
all been independently digitized. Reconstructed OLL/PLL states are valid examples,
not exact copies of all source artwork. F2L recognition uses the fixed photo masks.

Cube-state checks cannot prove universally optimal finger mechanics. Full physical
execution of every grouping, physical print proofs, color-vision user testing and
memorization studies remain incomplete. Color conveys layer information, so
monochrome reproduction is not equivalent. No claim of tribox endorsement is made.
