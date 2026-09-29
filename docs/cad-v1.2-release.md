# CAD v1.2 — Single-Topology Release

CAD v1.2 removes the dual H1/H3 branch from the main build.

The release uses the patent-confirmed H1 distal topology and couples it directly to the primary upper-drive orientation.

Two assembly checkpoints are generated:

- extended: primary input 0°
- flexed: primary input -35°

The same rigid part geometry is used in both states.

## Exported part set

- input bracket
- upper drive
- lower drive
- Pivot Block
- main upper rail
- distal ground link
- distal input arm
- Link 35 coupler
- Pivot Head arm
- fingertip link

All current STL meshes passed watertight validation.

## Remaining limits before physical-build release

The following are still prototype assumptions rather than recovered factory dimensions:

- absolute metric scale AB = 5 mm seed;
- plate thicknesses and Z offsets;
- screw-head and washer envelopes;
- exact hole clearances and tolerances;
- patient-fit interface.

The model is suitable for engineering mock-up and mechanism validation, not clinical use.
