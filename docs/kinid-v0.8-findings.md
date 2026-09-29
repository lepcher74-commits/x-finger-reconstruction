# KIN-ID v0.8 — First Image-Derived Geometry

## Frame used

Assembly video, approximately 340 s. This frame gives a close, nearly side-on view of the upper and lower indexed adjustment interfaces.

## Manual digitization

Four consecutive centers were digitized on each visible row.

Upper row:
- (310, 189)
- (336, 190)
- (361, 190)
- (386, 190)

Lower row:
- (309, 243)
- (334, 243)
- (359, 244)
- (384, 244)

## Fitted pitch

Least-squares fit along the row principal axis gives:

- upper pitch ≈ **25.30 px**
- lower pitch ≈ **25.00 px**
- mean pitch ≈ **25.15 px**

The agreement between the two rows is about 1.2%, which is strong evidence that the upper and lower interfaces share the same discrete indexing pitch.

The apparent row-to-row separation is ≈ **2.15 pitch units** in this frame, but this value remains perspective-sensitive and is not yet treated as a manufacturing dimension.

## Status

The **equality of upper/lower indexing pitch** is upgraded to **IDENTIFIED**.

The pitch in millimetres remains unknown. M1.4 fastener information alone is not sufficient for a defensible image scale because thread diameter, clearance-hole diameter and screw-head diameter are different quantities.

## Consequence for CAD

Prototype v0.4 should be parameterized by a master discrete pitch `P`.

Until metric calibration is obtained:

- all longitudinal adjustment-hole positions are integer multiples of `P`;
- upper/lower branches use the same `P`;
- absolute dimensions remain separate from normalized geometry.

This removes the arbitrary 5.0 mm pitch from the master geometry and turns it into a temporary display scale only.
