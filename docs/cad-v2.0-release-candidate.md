# CAD v2.0 — Prototype Release Candidate

Status: build-oriented research prototype candidate.

## Scope

CAD v2.0 freezes one reproducible configuration from the current reconstruction work:

- traced user-supplied 2D profiles;
- corrected rigid-body interpretation;
- paired-cheek clevis construction;
- distal S-link Z correction from CAD v1.8a;
- candidate M1.4 fastener map from CAD v1.9a;
- local-origin STL parts for manufacturing review;
- assembled STL for visual verification.

## Frozen prototype parameters

- Working metric calibration: 0.1 mm/px — SCALE_BOUND, not factory proof.
- Pivot hole diameter: 1.8 mm — DESIGN_CANDIDATE.
- Thread family: M1.4 — CONFIRMED_FAMILY.
- Main plate thickness: 1.0 mm — DESIGN_CANDIDATE.
- Carrier thickness: 1.6 mm — DESIGN_CANDIDATE.
- Clevis cheek thickness: 0.8 mm — DESIGN_CANDIDATE.
- Clevis cheek centers: ±1.5 mm — DESIGN_CANDIDATE.
- Orange S-link center Z: +1.6 mm — DESIGN_CANDIDATE.
- Outer support center Z: ±3.2 mm — DESIGN_CANDIDATE.
- Minimum moving clearance: 0.30 mm — BUILD_RULE.
- Minimum screw reserve: 0.50 mm — BUILD_RULE.

## Physical part set

The RC exports ten physical pieces:

1. upper_drive
2. lower_main_rail
3. purple_fork_L
4. purple_fork_R
5. green_fork_L
6. green_fork_R
7. central_carrier
8. orange_S_link
9. tip_rocker
10. proximal_support

Fork cheeks are separate physical plates but each paired set represents one kinematic clevis body.

## Validation basis

- All individual RC STL meshes are watertight.
- Assembly STL is watertight.
- Motion/hardware validation basis: CAD v1.8 / v1.8a.
- Distal S-link is offset in Z to remove the collision family found near extension.
- Hardware mapping remains prototype-oriented unless directly source-confirmed.

## Important limitation

This repository contains a reverse-engineering / research reconstruction.
CAD v2.0 is not a clinically validated medical-device release and is not suitable for human use without professional engineering, fitting, fatigue testing, pinch-point analysis, material validation and safety review.
