# Changelog

## KIN-ID v0.9 / CAD Prototype v0.3

- Sampled promotional-video motion sequence at 150, 152, 154 and 155 s.
- Added preliminary manual centerline/pivot-chain picks.
- Added normalized motion-envelope analysis.
- Introduced an OBSERVED / LOW confidence class for occluded motion-frame measurements.
- Prevented low-confidence motion picks from overriding master CAD dimensions.
- Defined the acceptance gate for future O/A/B/C/D multi-pose identification.

## KIN-ID v0.7 / CAD Prototype v0.3

- Added multi-frame Procrustes-based linkage identification scaffold.
- Added explicit moving-base primary model to the fitting code.
- Added assembly-video observation register.
- Confirmed M1.4×5L proximal fastener instruction, 4L small-size note, and M1.4×2L distal fastener instruction.
- Added first metric seed table with confidence status per parameter.
- Added parametric OpenSCAD physical seed model with upper/lower Z-separated perforated branches.
- Marked all uncalibrated plate geometry as ESTIMATED.

## KIN-ID v0.6 / CAD Prototype v0.2

- Corrected the ground/input topology.
- Separated Matrix 1 from moving Bracket 2.
- Reclassified the old normalized linkage solution as non-manufacturing solver data.
- Added evidence from project-supplied assembly and motion videos.
- Added matched-hole-index constraint for upper/lower adjustable branches.
- Added documented M1.4×5L assembly fastener marking.
- Established CONFIRMED / IDENTIFIED / ESTIMATED parameter classes.
