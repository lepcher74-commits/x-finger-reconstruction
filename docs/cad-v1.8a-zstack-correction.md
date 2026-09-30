# CAD v1.8a — Local Z-stack Correction

## Problem

CAD v1.8 found the same collision in 15 poses:

main phalanx <-> orange S-link

Both parts were modeled as 1.0 mm plates centered on the same plane.

## Minimum offset search

A local Z-search was performed while retaining:
- 1.0 mm phalanx thickness;
- 1.0 mm orange S-link thickness;
- 0.30 mm washer allowance;
- required residual face clearance >= 0.30 mm.

The minimum center offset satisfying the target was:

orange S-link center Z = +1.60 mm

This creates:
- raw face gap = 0.60 mm;
- residual clearance after 0.30 mm washer allowance = 0.30 mm.

## Status

DESIGN_CANDIDATE

The +1.60 mm side is not claimed to be the original production side/order. It is the minimum engineering offset that clears the currently diagnosed conflict.

## Consequence

With this local Z separation, the collision family diagnosed in v1.8 is removed in all 36 sampled poses.

The next task is to validate the chosen side/order against the best real-photo and patent evidence before freezing the build BOM.
