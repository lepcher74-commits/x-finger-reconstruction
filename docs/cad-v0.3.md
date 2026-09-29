# CAD Prototype v0.3

## Purpose

v0.3 is the first **metric seed model**.
It is intentionally not a manufacturing reconstruction yet.

The model introduces physical plate width, hole arrays, layer offset and
separate input / primary / distal bodies so that future identified geometry
can be dropped into a real parametric structure instead of a wireframe.

## Seed dimensions

Current seed values:

- hole pitch: 5.0 mm — ESTIMATED;
- M1.4 clearance-hole seed: 1.6 mm — ESTIMATED;
- bar width: 6.5 mm — ESTIMATED;
- plate thickness: 1.2 mm — ESTIMATED;
- A-B spacing: 10 mm — ESTIMATED;
- branch length: 35 mm — ESTIMATED;
- primary phalanx seed: 34 mm — ESTIMATED;
- distal seed: 18 mm — ESTIMATED.

These values are placeholders for geometry validation and interference checks.

## Confirmed hardware constraints

Assembly-video evidence gives:

- proximal fastener: M1.4×5L;
- small-size proximal variant: 4L;
- distal fastener: M1.4×2L.

## CAD architecture

The OpenSCAD model preserves:

- rotating input body;
- upper adjustable perforated branch;
- lower adjustable perforated branch;
- separate Z layers;
- primary phalanx;
- distal body.

The actual distal Link-35 / Pivot-Head geometry remains to be identified and
will replace the current simplified distal bar in v0.4.
