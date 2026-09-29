# KIN-ID v1.6 / CAD v1.0 — Integrated functional-candidate

## Scope

This stage integrates the identified primary linkage with the identified distal geometry into one parameterized assembly and performs a full motion sweep.

## Geometry status

Primary stage:
- AB = 5.0 mm — SCALE_BOUND
- AC = 48.108 mm — IDENTIFIED_RATIO + SCALE_BOUND
- BD = 52.232 mm — IDENTIFIED_RATIO + SCALE_BOUND
- CD = 10.679 mm — IDENTIFIED_RATIO + SCALE_BOUND

Distal chain (scaled through the same CAD render used for the primary stage):
- P0-P1 = 26.921 mm
- P1-P2 = 10.095 mm
- P2-P3 = 12.064 mm
- P3-P4 = 17.797 mm

The distal length ratios are identified, but the absolute millimetre scale still inherits the v1.4 metric-scale uncertainty.

## Motion sweep

The integrated assembly was swept across input angles from -35° to +20°.

No candidate planar self-overlap was detected in the checked non-adjacent segments across the 56 sampled poses.

Important limitation: the distal motion law used for the sweep is still an **ESTIMATED engineering coupling law** derived from observed synchronized curl; it has not yet been uniquely identified from tracked pivot trajectories.

Therefore this release is a **functional-candidate STL**, not a validated functional prosthesis.

## STL output

Separate parts are exported for:
- input bracket
- upper drive
- lower drive
- pivot block
- main phalanx
- distal link 01
- distal link 12
- distal link 23
- fingertip
- assembly preview

All exported STL meshes passed watertightness validation.

## Next engineering checks before a build-oriented release

1. Replace estimated distal motion law with a directly identified linkage closure.
2. Confirm the absolute metric scale from a physical reference or factory dimension.
3. Confirm real M1.4 head/washer/spacer envelopes and bearing clearances.
4. Perform 3D collision checking using complete fastener geometry.
5. Freeze print/manufacturing tolerances and material assumptions.

This repository is an engineering reconstruction and is not a clinically validated medical-device design.
