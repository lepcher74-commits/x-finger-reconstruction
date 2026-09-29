# CAD v1.3 — User-profile reconstruction

## New source material

The project owner supplied two side-view drawings:
- an exploded layout of eight bending-mechanism components;
- the same profiles in assembled position.

These drawings materially improve the CAD reconstruction because they expose complete 2D silhouettes, holes, forks and a curved internal slot that were previously represented only by capsule-like placeholder links.

## Recovered components

1. tip_plate
2. pivot_plate
3. fork_purple
4. link_orange
5. fork_green
6. long_link_magenta
7. cam_orange
8. long_rail_blue

## Reconstruction method

- The outer profile of each component was recovered from the exploded drawing.
- Circular features were associated with the appropriate component.
- The cam internal curved slot was recovered as a separate inner contour.
- The exploded profiles were registered back onto the assembled drawing with rigid 2D transforms.
- Metric conversion currently uses 0.1 mm/pixel, derived from a 1.8 mm preview pivot-hole reference and a median image hole radius of about 9 px.

The metric conversion remains SCALE_BOUND; it is not claimed to be an original factory dimension.

## Status changes

- 2D component silhouettes: IDENTIFIED_PROFILE
- relative assembled placement in the supplied drawing: IDENTIFIED_2D_REGISTRATION
- hole-center pattern: IDENTIFIED_2D / manually curated
- absolute millimetre scale: SCALE_BOUND
- Z-stack assignment: ESTIMATED / build-layout candidate

## CAD output

CAD v1.3 replaces the former capsule-only geometry with the traced user-supplied profiles. Individual STL and SCAD files are generated for each component, plus a combined traced assembly.

The current Z assignment is provisional and is used only to create a collision-separable 3D representation. Final layer ordering still requires validation against physical side/oblique views.
