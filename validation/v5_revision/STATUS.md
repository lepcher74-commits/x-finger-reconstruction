# V5 revision — STATUS (issue #7, branch `opencode/issue7-20261012171902`)

Short stage resumed after the cancelled run `38237339734` (no artifact of its
own). The checkpoint was restored with
`gh run download 38237339734 -n cad-validation-38237339734 -D validation`
(artifact `11742905642`, SHA256 `0b5e5db0…64f3b` supplied by the supervisor).
Old V5 is **NOT accepted** and was not rebuilt; it is kept as `validation/v5/`.

## Blocker (exact) — reference drawings cannot be read visually

The model driving this run has **no image input**: `Read` on
`references/v5/socket_views.png` / `socket_photo.png` returns
`ERROR: Cannot read image (this model does not support image input)`.

* The files were recovered from `opencode/issue5-20261010095002`, are **base64
  text**, and were decoded to real PNGs
  (`579×582` and `543×510`, copied to `references/`). So the files are
  available and valid — the *reader* cannot see them.
* Consequence: the four **labelled** views cannot be identified and **no
  dimension is read from the picture**. `socket_photo.png` is in fact a
  **greyscale** image (no green/blue pixels), i.e. a render, not a colour
  drawing — also not readable here.

What was done instead (objective, not guessed): `measure_references.py` measures
only **pixel colour extents** (green=P04, blue=shell) per geometric view cell;
results in `reference_measurements.json` and `proportions_table.json`. These are
pixel facts, not calibrated dimensions.

## Orientation correction (from the issue text + the frozen V4 frame, NOT from the image)

The V4 hinges turn about **+Z** and the whole mechanism moves in **XY**
(`motion.json`: every frame is `{angle, translation:[x,y]}`). Therefore, in the
frame of P04:

| direction | axis | meaning |
|---|---|---|
| finger proximal→distal | **X** | socket length |
| dorsal/ventral | **Y** | **top / bottom** ← where the shells must go |
| lateral | **Z** | the **sides** ← where old V5 wrongly put them |

P04_green CAD bbox: `x[659.44,791.73] y[-510.21,-395.57] z[-29.04,29.04]`
(132.29 × 114.64 × 58.08), centre `y=-452.89, z=0`.

Old V5 shells sat at `z 28.5…89.5` (i.e. about **+Z = the side**). The revision
(`build_shells_rev.py`) rebuilds them as a **cap on P04's distal face
(x=791.73)**:

* grey upper shell about **+Y** (`θ 24…156°`), blue lower shell about **−Y**
  (`θ 204…336°`), the two **side gaps left open at ±Z**;
* grey stem (`x 791.2…802`) welded to P04's distal-top corner (0.5 embed);
* blue side walls linking the lower shell's ±Z edges to P04's side faces;
* longitudinal cradle lift `+6` at the free end;
* P04, all V4 parts, axes and kinematics are **untouched**.

`shell_t = 1.5` is the issue value in **V4 model units**; it is *not* a
calibrated physical millimetre and wearability is not claimed. All other values
are assumed demonstration values (listed in `shells_revision_report.json`).

## Files produced (this stage)

* `build_shells_rev.py` — corrected parametric CAD + render.
* `P10_gray_upper.step|.stl`, `P11_blue_lower.step|.stl` — valid, **1 solid**
  each.
* `four_views_p04_registered.png` — four orthographic panels (front/top/side/
  back) in **global assembly coordinates, equal aspect, one scale per panel,
  no independent scaling of the shells**.
* `measure_references.py`, `proportions_table.py`,
  `reference_measurements.json`, `proportions_table.json`.
* `socket_views_views_detected.png`, `socket_photo_views_detected.png` — view
  cells drawn for a human reviewer.
* `references/socket_views.png`, `references/socket_photo.png` — decoded.

## Facts (rest pose, frame 0)

| part | solids | valid | bbox (x / y / z) |
|---|---|---|---|
| P10_gray_upper | 1 | true | 790.2…873.8 / −442.3…−396.1 / −25.1…25.1 |
| P11_blue_lower | 1 | true | 790.2…873.8 / −490.0…−457.5 / −29.5…29.5 |

* P10×P11 intersection = **0**; P10/P11 vs each of P01…P09 = **0** at the rest
  pose (bboxes touch P06/P07 but the solids do not intersect).
* Do **not** confuse these with P08_gray / P02_blue (unchanged).

## Residual defects / open items

1. **Reference-compliance is NOT proven** — the model cannot read the drawing,
   so the corrected placement is justified by the V4 frame and the issue text
   only. A human must look at `four_views_p04_registered.png` against
   `references/socket_views.png`.
2. Reference view ↔ direction mapping unknown; reference ratios in
   `proportions_table.json` are therefore not asserted against a named view.
3. Wall thickness along the normal (min/max + zones) not re-measured in this
   stage; the free cavity of the phantom not yet verified.
4. Collisions checked only at the rest pose; the 74-pose sweep, full
   STEP/STL/HTML/GIF integration and the full mechanism build remain.

## Next step

Human (or image-capable model) verifies `four_views_p04_registered.png` vs
`references/socket_views.png`; if the grey/blue split and the ±Z gaps match,
proceed to normal-thickness audit, free-cavity check, 74-pose collisions, then
integrate P10/P11 into the full V4 HTML/GIF and export the full assembly
STEP/STL. Separate branch, no merge; PR to be opened by the supervisor.
