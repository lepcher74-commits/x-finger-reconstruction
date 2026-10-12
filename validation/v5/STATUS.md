# V5 shells — STATUS (issue #7)

Resumed from the saved result of run `38213100529`
(artifact `cad-validation-38213100529`, restored and SHA256-verified by the
supervisor). The old result was **not** rebuilt from scratch; it was saved to the
branch first, then the two remaining software defects were corrected.

## Thickness contradiction — resolved (this stage)

The old `shells_report.json` had `estimated = 1.5` (from `r_out - r_in`) but
`normal_face_distance = 1.06398` for `P10_gray_upper`, while `STATUS` called the
thickness *confirmed*. That was a **reporting defect, not a geometry defect**:

* The shell is lofted from **25 overlapping slices**; the cradle lift gives each
  slice a slightly different axis (z shifts by up to ~0.44 per step).
* The old `normal_face_distance` was the minimum over **all** inner/outer face
  pairs, i.e. it could pair the **inner face of one slice with the outer face of
  a neighbouring, cradle-shifted slice** — a *wrong pair*. The minimum is
  `1.5 - Δaxis = 1.06398`, nowhere near a real wall.
* Measured **directly along the wall normal** (ray march into the material to the
  first boundary, thousands of samples):

| part | nominal `r_out-r_in` | measured min | measured max | same-wall (`face_dist_coaxial`) | wrong pair (`face_dist_cross_slice`) |
|---|---|---|---|---|---|
| P10_gray_upper | 1.5 | **1.5** | 55.6 (in the leg zone) | **1.5** | 1.06398 |
| P11_blue_lower | 1.5 | **1.5** | 1.88 (side-wall skirt) | **1.5** | 1.5 |

Zones (P10): x `742.5..770.2` (leg merged) min 1.5 max 55.6; x `770.2..825.5`
min 1.5 max 1.5. The **only** effect of the slice junctions is *added* material,
never thinning below 1.5. So no geometry fix was needed; the measurement and its
wording were fixed. `r_out - r_in` is now labelled *nominal construction value*,
not a measurement.

## Clearance — reflected honestly

* Nominal **radial** clearance on the circular walls is **2.0** (`r_in - r_phalanx`).
* The **absolute minimum solid distance** to the assumed phantom is smaller:
  **0.1667** (P10) and **0.5749** (P11). The report now stores the closest-point
  locations:
  * P10: shell `(760.0,-413.0,79.26)` — the back leg / proximal cap region.
  * P11: shell `(819.58,-442.68,51.71)` — the side-wall skirt near the free end.
* These are **axial/skirt** gaps, not the wall radius. The phantom is an assumed
  demo body; the values are reported, not hidden.

## Unchanged, verified results

* `P10_gray_upper` / `P11_blue_lower`: valid, **1 solid** each.
* Open / mid / closed and **all 74 poses: 0 forbidden intersections**; 148
  intended P04 welds (the designed 0.5 weld). Old V4 parts, axes and kinematics
  untouched; V4 scale still conventional.

## Accepted demonstration dimensions (assumed, NOT measured)

`phalanx_r = 24`, clearance 2, `y_center = -420`, `z_ref = 29`, cradle
`rise = 6`, sectors 62/118/242, wall 1.6, leg 14x16, `embed = 0.5`,
`shell_t = 1.5` (the issue #7 value).

## Files

* `build_shells.py` — reproducible build + normal-ray thickness audit + checks +
  preview/comparison.
* `P10_gray_upper.step|.stl`, `P11_blue_lower.step|.stl`,
  `assumed_phalanx_demo.step`, `assembly_v5_open.step`,
  `assembly_v5_folded.step`.
* `shells_report.json`, `shells_parameters.json`, `shells_preview_v5.png`,
  `shells_comparison_v5.png`.
* `make_viewer_v5.py` — integrates P10/P11 into the full V4 viewer:
  `assembly_viewer_v5.html`, `assembly_motion_v5.gif`,
  `assembly_v5_preview.png`, `viewer_data_v5.json`.

## Integration into the full V4 viewer (done)

`make_viewer_v5.py` reuses the frozen V4 `viewer_data.json` (9 parts + 8 axes,
74-frame motion) and appends P10/P11 rigidly parented to **P04**, without
touching any V4 file. It produces:

* `assembly_viewer_v5.html` — standalone (no internet), all full housings,
  74-step slider and automatic **fold + unfold** (ping-pong), section toggle and
  per-part visibility. The new shells are listed as “Верхняя оболочка P10
  (серая)” and “Нижняя оболочка P11 (синяя)”.
* `assembly_motion_v5.gif` — 3D animation of the full V4 assembly with the
  shells, both directions.
* `assembly_v5_open.step` / `assembly_v5_folded.step` — full assembly
  (19 solids: 9 V4 parts + 8 axes + P10 + P11).
* `viewer_data_v5.json`, `assembly_v5_preview.png`.

## Next step

Item closed on the requested points. Optional follow-ups only: a fit/tolerance
study to replace the assumed demo dimensions, and physical-mm calibration. No PR
merge.
