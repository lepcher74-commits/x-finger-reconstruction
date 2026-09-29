# CAD v1.1 — Dual Distal Candidate + Fastener Envelope

## Z-stack revision

The layer stack was widened to preserve room for a 0.3 mm washer allowance plus approximately 0.30 mm residual face clearance:

- upper outer rail center: +3.5 mm
- upper drive center: +1.9 mm
- pivot block center: 0 mm
- lower drive center: -1.9 mm
- lower outer rail center: -3.5 mm

Nominal plate thicknesses:
- drives: 1.0 mm
- outer rails: 1.0 mm
- pivot block: 1.6 mm

The computed residual clearance is approximately 0.30 mm at the tightest adjacent interface.

## Fastener envelope used

These are prototype design envelopes, not asserted factory dimensions:

- M1.4 shaft envelope: 1.4 mm nominal thread diameter
- clearance hole: 1.8 mm design reference
- screw head envelope: 3.0 mm diameter × 1.2 mm height
- washer envelope: 3.2 mm diameter × 0.3 mm thickness

## CAD structure

The OpenSCAD model now contains switchable distal variants:

- distal_H1
- distal_H3
- assembly_H1
- assembly_H3

This allows the same primary-stage model and Z-stack to be tested with both surviving distal hypotheses.

## Release status

CAD v1.1 is still a functional-candidate research model, not a build-validated or clinical device.
