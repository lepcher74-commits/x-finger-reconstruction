# CAD v1.3 Build Status

The supplied 2D drawings allow the project to move from abstract linkage bars toward actual part silhouettes.

## Current confidence classes

| Feature | Status |
|---|---|
| eight component outer profiles | IDENTIFIED_PROFILE |
| cam curved internal slot | IDENTIFIED_PROFILE |
| major pivot-hole centers | IDENTIFIED_2D |
| exploded-to-assembled transforms | IDENTIFIED_2D_REGISTRATION |
| primary linkage ratios | IDENTIFIED_RATIO + SCALE_BOUND |
| distal H1 topology | CONFIRMED_TOPOLOGY |
| absolute scale | SCALE_BOUND |
| plate thickness | BOUNDED_ESTIMATE |
| layer order / Z positions | ESTIMATED |
| final production tolerances | PENDING |

## Next engineering task

1. validate the layer order from oblique photographs/video;
2. assign each traced profile to a patent/assembly part number;
3. perform a full 3D sweep using the traced silhouettes rather than capsule envelopes;
4. freeze print/machining clearances;
5. produce CAD v1.4 build candidate and BOM.
