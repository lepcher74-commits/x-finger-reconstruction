# V5 shells — STATUS (issue #7), correction stage

Resumed from the saved result of run `38204875171`
(artifact `cad-validation-38204875171`, `v5/build_shells.py` + STEP/STL +
`shells_report.json`). The old result was **not** rebuilt from scratch; only the
defects listed in the issue were corrected.

## Fixed in this stage

| defect (previous save) | fix |
|---|---|
| `P11_blue_lower` was **3 solids** | side walls are now welded into the arc -> **1 solid** each |
| both shells **intersected P01** | socket moved distal of P01; P01 sweeps `x<=734` (P04 frame) over the 74 poses, socket starts at `x_start=744` |
| the two shells **intersected each other** | explicit side gaps `62°..118°` and `242°..298°` |
| `P11` **intersected the phantom** | the cradle curve is applied to the phalanx too -> constant radial clearance along the length |
| thickness `2V/(A_out+A_in)` **included the leg/walls** | thickness measured **on the shell walls only** as `r_out - r_in` along the radial normal, confirmed by minimum face distance |

## Result

* `P10_gray_upper`: valid, **1 solid**, wall thickness **1.5** (26.0 -> 27.5).
* `P11_blue_lower`: valid, **1 solid**, wall thickness **1.5** (26.0 -> 27.5).
* Open / mid / closed poses: **0 forbidden intersections** (only the designed
  2 P04 welds).
* All **74** poses: **0 forbidden intersections**; 148 intended P04 welds.
* Phalanx cavity free, radial clearance 2.0; parts connected to P04
  (`distance = 0`, 0.5 weld embed).

## Accepted demonstration dimensions (assumed, NOT measured)

V4 scale is conventional and uncalibrated; physical mm and wearability are not
claimed. `shell_t = 1.5` is the value requested in issue #7, applied along the
normal in V4 model units. All other numbers are assumed demo values:
`phalanx_r = 24`, clearance 2, `y_center = -420` (finger centre line),
`z_ref = 29` (P04 top), cradle `rise = 6`, sector angles 62/118/242, wall 1.6,
leg 14x16, `embed = 0.5`.

## Files

* `build_shells.py` — reproducible build + checks + preview/comparison.
* `P10_gray_upper.step|.stl`, `P11_blue_lower.step|.stl`,
  `assumed_phalanx_demo.step`, `assembly_v5_open.step`.
* `shells_report.json`, `shells_parameters.json`,
  `shells_preview_v5.png`, `shells_comparison_v5.png`, `run_stdout.txt`.

## Next step

Integrate the two shells into the existing V4 interactive HTML/GIF (both
motion directions), following P04 rigidly. Then full folding/unfolding
assembly. No PR merge.
