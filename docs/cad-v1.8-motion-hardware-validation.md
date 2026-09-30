# CAD v1.8 — Full Motion + Hardware Collision Sweep

## Scope

CAD v1.8 validates the current reconstructed primary + distal linkage through the working range with conservative hardware envelopes.

This stage distinguishes:
- topology/geometric relations already identified;
- SCALE_BOUND metric geometry;
- DESIGN_CANDIDATE hardware/Z-stack assumptions.

## Working sweep

Primary input range:

-35 deg .. 0 deg

36 poses were checked at 1 degree increments.

The distal four-bar was constrained to the mathematically valid KIN/CAD v1.6 branch by the current design-candidate mapping:

distal_input = -29 deg + 0.8 * primary_input

This mapping is not claimed as the original X-Finger transmission law; it is a closure-valid engineering coupling for validation.

## Closure result

All 36 sampled poses achieved simultaneous primary and distal loop closure.

## Hardware envelopes

Design-candidate envelopes used in the sweep:

- shaft nominal: 1.4 mm
- clearance hole reference: 1.8 mm
- screw-head envelope: 3.0 mm diameter x 1.2 mm
- washer envelope: 3.2 mm diameter x 0.30 mm
- nut envelope: 3.2 mm diameter x 1.2 mm

These are prototype envelopes, not asserted original factory dimensions.

## Collision result

The conservative sweep found one repeated collision family only:

phalanx <-> orange S-link

It occurs in 15 near-extension poses, approximately -14 deg .. 0 deg.

No other plate-plate or hardware-link collision family was detected by the current conservative proxy.

This is therefore a localized Z-stack issue rather than a global kinematic failure.

## Interpretation

The v1.8 result supports the corrected independent-fork body model introduced in CAD v1.7.

It also shows that the orange S-link should not remain coplanar with the main phalanx in the current build candidate.
