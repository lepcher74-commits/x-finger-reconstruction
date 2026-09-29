# Roadmap to STL

Current state: KIN-ID v1.2.

## Goal distinction

### Preview STL
A printable geometric mock-up for visual review, fit checks and mechanism layout.
It may still contain estimated dimensions.

### Functional prototype STL
A mechanically meaningful assembly candidate with:
- closed primary linkage;
- identified or bounded pivot geometry;
- explicit Z-stack;
- fastener clearances;
- motion-envelope and collision checks;
- manufacturable plate thicknesses and tolerances.

## Remaining steps

### KIN-ID v1.3 — close the primary linkage
Identify the opposite-side drive pivots that connect to the already identified Pivot Block articulation pair.
Target: complete the primary loop without guessing the fourth point.

### KIN-ID v1.4 — metric scale + Z-stack
Recover or bound:
- hole pitch in millimetres;
- plate thickness;
- spacer/washer stack;
- pivot/clearance diameters;
- branch offsets.

At the end of v1.4, a **preview STL** can be exported.

### CAD v0.5 / KIN-ID v1.5 — physical solids + collision sweep
Replace skeleton links with solids:
- upper/lower bars;
- rotating input bracket;
- Pivot Block;
- phalanx rails;
- distal link;
- Pivot Head;
- fingertip interface.

Run a motion sweep and remove interference.

### CAD v1.0 / KIN-ID v1.6 — prototype STL release
Freeze a prototype parameter set and export:
- per-part STL files;
- assembly STL for review;
- BOM / fasteners;
- parameter table with CONFIRMED / IDENTIFIED / ESTIMATED labels.

## Current estimate

- Preview STL: ~2 steps from KIN-ID v1.2.
- Functional prototype STL: ~4 steps from KIN-ID v1.2.

This is an engineering reconstruction, not a clinically validated medical-device design.
