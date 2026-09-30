# X-Finger Reconstruction — Work/Astra Handoff

## Mission
Rebuild the X-Finger reconstruction as a manufacturing-oriented, part-level parametric CAD assembly.

Treat all existing CAD v0.x–v2.0 artifacts as research evidence, not as authoritative manufacturing geometry.

## Project repository
`lepcher74-commits/x-finger-reconstruction`

## Current state
The project has progressed through patent/topology reconstruction, primary linkage identification, distal linkage identification, image/video audits, traced 2D profiles, Z-stack and hardware-envelope studies, collision sweeps, candidate BOM/fastener maps, and CAD v2.0 RC.

CAD v2.0 RC is not accepted as a manufacturing assembly because:
1. some profiles remain incomplete or partially traced;
2. several physical parts are merged into single bodies;
3. fork/clevis cheeks are not consistently represented as distinct physical pieces;
4. not every pivot/axis is explicitly modeled;
5. some fastener locations are inferred rather than source-confirmed;
6. telescopic/adjustment subassemblies are simplified;
7. the assembly lacks a rigorous part → joint → rigid-body hierarchy;
8. some geometry exists only as 2D extrusion without correct interfaces/features;
9. distal shell/cover has not been cleanly separated from the core linkage;
10. current metric scale is still SCALE_BOUND rather than factory-confirmed.

## Evidence classes
- CONFIRMED — directly supported by a primary source, assembly video, or explicit dimension.
- IDENTIFIED — recovered by multi-view / multi-pose geometric identification.
- SCALE_BOUND — relative geometry identified, absolute metric scale provisional.
- DESIGN_CANDIDATE — engineering choice introduced for the prototype.
- SECONDARY_REFERENCE — third-party CAD/renders useful for layer order/topology, not original dimensions.
- REJECTED — earlier hypothesis contradicted by later evidence.

## Source hierarchy
1. Primary patent / claims / figure topology.
2. Original X-Finger photographs and videos.
3. Assembly video and manufacturer/official technical material.
4. User-supplied 2D traced/reconstructed profiles.
5. Multi-pose overlays derived from user images.
6. Secondary commercial CAD renders / Etsy-like reconstructions.
7. Earlier assistant-generated CAD as derived evidence only.

## Known high-confidence topology
- Body-powered, one operational DOF after fitting.
- Two major drive branches transmit residual-finger motion.
- Adjustable telescopic/overlap members are fitting DOFs only; locked during use.
- Central carrier / Pivot Block is a rigid assembly body.
- Distal mechanism is a four-bar style linkage with a separate short rocker/fork and S-link/coupler.
- Purple fork and green fork must NOT be merged rigidly into the long links.
- Fork/clevis assemblies can consist of multiple physical plates but one kinematic rigid body.
- Distal shell/cover geometry must be separated from the kinematic core unless evidence proves it is load-bearing.

## Critical correction history
### Rejected / downgraded
- Early fixed-ground A/B four-bar interpretation without bracket motion.
- Treating outer + inner phalange as separate moving bodies during operation.
- Treating purple fork as rigidly merged with long magenta link.
- Treating green fork as rigidly merged with long blue rail.
- Treating a proximal secondary-CAD feature as definitive cam/slot.
- Assigning M1.4×2L directly to a 2.2 mm stack in v1.9; rejected.

### Current working values
Prototype candidates unless otherwise noted:
- AB = 5.0 mm — SCALE_BOUND
- AC ≈ 48.11 mm — IDENTIFIED_RATIO + SCALE_BOUND
- BD ≈ 52.23 mm — IDENTIFIED_RATIO + SCALE_BOUND
- CD ≈ 10.68 mm — IDENTIFIED_RATIO + SCALE_BOUND
- hole clearance = 1.8 mm — DESIGN_CANDIDATE
- plate thickness ~1.0 mm — DESIGN_CANDIDATE
- carrier thickness ~1.6 mm — DESIGN_CANDIDATE
- fork cheek thickness ~0.8 mm — DESIGN_CANDIDATE
- fork cheek Z ≈ ±1.5 mm — DESIGN_CANDIDATE
- orange S-link Z ≈ +1.6 mm — DESIGN_CANDIDATE
- M1.4 family — CONFIRMED FAMILY
- M1.4×5L proximal — CONFIRMED FAMILY
- M1.4×4L small note — CONFIRMED NOTE / candidate application
- M1.4×2L distal family — CONFIRMED FAMILY, exact joint unresolved

## Work/Astra rebuild objective
Create `CAD v3.0 Manufacturing Reconstruction`, rebuilt from evidence rather than by patching v2.0.

### Mandatory modeling rules
1. Every physical part must be a separate component unless evidence proves inseparability.
2. Every functional pivot must have axis ID, mating parts, hole diameter, fastener/shaft, washers/spacers, axial stack, and clearance.
3. Every adjustable member must be represented as separate sliding/overlap parts.
4. Distinguish physical part, rigid body, kinematic joint, fitting DOF, and operational DOF.
5. Do not fill missing geometry silently. Mark uncertain features.
6. Preserve confidence labels in parameter tables.
7. Maintain one master coordinate system and one assembly tree.
8. Run motion and collision tests on actual solids, not line-segment proxies only.
9. Produce exploded assembly and joint-axis drawings.
10. Preserve reversible parametric construction.

## Deliverables for CAD v3.0
- master parametric assembly;
- separate components for every physical plate/link/fork/cheek/carrier/shell;
- joint graph with axis IDs;
- rigid-body graph;
- parameter table with confidence tags;
- per-joint fastener stack table;
- full Z-stack;
- exploded assembly;
- extended/intermediate/flexed configurations;
- motion study;
- collision report;
- BOM;
- manufacturing drawings;
- STL exports;
- DXF exports for sheet/laser-cut parts;
- STEP-compatible export if available;
- changelog and audit notes.

## Acceptance gate before calling v3.0 build-ready
- no merged physical parts without evidence;
- no unassigned pivot holes;
- no unexplained floating fasteners;
- no unknown rigid-body parentage;
- all moving interfaces have clearance;
- all moving states close kinematically;
- no hard 3D collisions in working range;
- all non-confirmed dimensions carry confidence status;
- full assembly can be reconstructed from BOM + drawings alone.

## Immediate first task in Work
Perform a top-down audit of the current repository and produce:
1. `AUDIT_v3_0.md`
2. `PART_CATALOG_v3_0.csv`
3. `JOINT_MAP_v3_0.csv`
4. `RIGID_BODY_MAP_v3_0.csv`
5. `SOURCE_EVIDENCE_MATRIX_v3_0.csv`
6. a list of all missing geometry/features blocking a clean manufacturing assembly.

Do not start by modifying STL. First reconstruct the part/joint/body ontology and source traceability.
