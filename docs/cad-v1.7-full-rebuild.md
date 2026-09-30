# CAD v1.7 — Full Rebuild

## Purpose

Rebuild the traced-profile model using corrected rigid-body and layer-stack assumptions derived from:

- patent topology;
- real X-Finger photographs/videos;
- user-provided 2D exploded/assembled profiles;
- secondary multi-view CAD renders used only for Z-stack and clevis interpretation.

## Key corrections

1. Purple fork is not rigidly merged with the long magenta drive link.
2. Green fork is not rigidly merged with the long blue rail.
3. Forked joints are represented as clevis-style paired cheeks around a central mating link.
4. The previous proximal cam/slot interpretation is demoted; current working topology favors revolute/clevis joints.
5. Physical part count is separated from kinematic rigid-body count.

## Provisional Z-stack

For preview/build preparation only:

- central mating plate thickness: 1.0 mm
- fork cheek thickness: 0.8 mm
- fork cheek centers: ±1.5 mm
- resulting central-to-cheek face clearance: 0.6 mm per side

These are DESIGN CANDIDATES, not recovered factory dimensions.

## Evidence status

- 2D outer profiles: IDENTIFIED_PROFILE from user-provided drawings.
- relative topology: CONFIRMED/IDENTIFIED from patent + multi-pose evidence.
- clevis ordering: SECONDARY_MULTI_VIEW_SUPPORTED.
- absolute thicknesses and layer spacing: DESIGN_CANDIDATE.
- hole diameter 1.8 mm: DESIGN_REFERENCE only.

## Outputs

Generated locally for the project:

- x_finger_CAD_v17_full_rebuild.scad
- x_finger_CAD_v17_full_rebuild.stl
- individual SCAD/STL components
- cad_v17_part_policy.csv
- cad_v17_clevis_stack.csv
- cad_v17_physical_zstack.csv
- cad_v17_stl_validation.csv
- cad_v17_design_audit.csv

## Next stage

CAD v1.8 should use this corrected Z-stack and independent fork rockers in a full motion/collision sweep, including screw-head and washer envelopes.
