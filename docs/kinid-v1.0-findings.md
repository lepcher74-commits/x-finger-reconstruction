# KIN-ID v1.0 Findings

## Scope

KIN-ID v1.0 introduces the first geometry promoted from OBSERVED/ESTIMATED to **IDENTIFIED_GEOMETRY**.

The source is the project-supplied side CAD-render containing two mirrored views of the same distal assembly. Five repeatable landmark centers (P0...P4) were digitized independently in both views.

The labels are intentionally neutral: patent-number mapping is not yet assigned to all five points.

## Internal consistency test

The lower view was mirrored and registered to the upper view with an independent 2D similarity transform.

Result:

- similarity-registration RMS residual: **1.82 px**
- reference span P0-P1: approximately **100 px**
- residual / datum length: approximately **1.8%**

This is sufficiently consistent to promote the normalized geometry to IDENTIFIED_GEOMETRY for the CAD-render family.

## Identified normalized segment lengths

Using |P0P1| = 1:

- P0-P1 = **1.0000**
- P1-P2 = **0.3668**
- P2-P3 = **0.4290**
- P3-P4 = **0.6728**

These values are not yet millimetres.

## Important limitation

The CAD-render may represent a particular X-Finger size/configuration, not a universal master geometry.

Therefore these ratios are valid as an identified configuration geometry, not yet as production dimensions for every device size.

## Status promotion

- distal five-landmark chain: IDENTIFIED_GEOMETRY
- absolute scale: pending
- exact patent-axis mapping P0...P4: pending
- primary moving-base geometry O/A/B/C/D: still under identification
- Z offsets: still estimated

## Next step

Use these ratios to constrain CAD Prototype v0.4, then identify the moving-base primary chain from clean side photographs and assembly-video frames.
