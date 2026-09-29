# CAD v1.4 — Traced-Profile Motion Sweep

## Scope

This stage uses the user-supplied exploded and assembled side-profile drawings as a geometric source.

Recovered 2D profiles:
- tip_plate
- pivot_plate
- fork_purple
- link_orange
- fork_green
- long_link_magenta
- cam_orange
- long_rail_blue

The traced profiles are registered from the exploded drawing into the assembled drawing, then candidate profile-to-kinematic-body mappings are audited before any hard collision conclusion is accepted.

## Important result: body-mapping audit

Two-point anchor length consistency against the current KIN-ID model:

| Part | Traced anchor | Model joint distance | mismatch | status |
|---|---:|---:|---:|---|
| long_link_magenta | 47.98 mm | 48.11 mm | -0.28% | ACCEPTED |
| pivot_plate | 19.50 mm | 22.04 mm | -11.52% | ACCEPTED / provisional mapping |
| link_orange | 15.36 mm | 12.06 mm | +27.35% | REJECTED for hard collision certification |
| tip_plate | 4.41 mm | 17.80 mm | -75.22% | REJECTED mapping |
| long_rail_blue | 5.60 mm | 31.00 mm | -81.92% | REJECTED mapping |

The large mismatches for the blue rail and tip plate show that the holes selected in those profiles are not the end-to-end kinematic anchors assumed in the earlier simplified model.

This is a useful correction: the side-profile drawings reveal additional structural holes and local pivots that must not be equated directly with the abstract KIN-ID segment endpoints.

## Motion sweep

Validated working branch:
- input angle: -35° to 0°
- step: 1°
- 36 poses

Only parts whose two-point anchor mismatch was <=25% were accepted into the hard collision test.

Accepted profiles:
- long_link_magenta
- pivot_plate

Result:
- hard collision poses after Z filtering: 0 / 36

This does **not** certify the complete traced assembly collision-free because several profile-to-body mappings are not yet resolved.

## Engineering implication

CAD v1.4 disproves part of the earlier direct profile mapping.

The next required step is **CAD v1.5 — Joint Reassignment**:
1. identify the correct functional holes on long_rail_blue and tip_plate;
2. resolve which orange/green/purple parts belong to Link 35, Pivot Head 33, fork 38, and fingertip 41;
3. use the assembled side drawing as a graph-matching problem rather than assigning profile holes by visual proximity;
4. rerun the full-profile sweep only after the joint graph closes consistently.

The geometry of long_link_magenta strongly supports the current ~48.1 mm upper-drive length.
