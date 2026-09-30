# KIN/CAD v1.6 — Distal rocker / slot resolution

## Key resolution

The former unresolved body `RX` is no longer required as an extra hidden link.

The user's multi-pose overlays plus the exploded side-profile geometry support a four-bar formed by:

- **Pivot plate** — ground / carrier of the distal four-bar.
- **Purple fork** — input rocker.
- **Orange S-link** — coupler.
- **Tip plate** — output rocker.

The important correction is that the **purple fork must not be merged rigidly with the long magenta drive link**. It is a separate rocker connected through a pin/fork interface.

Likewise, the **green fork should be treated as a separate front rocker** rather than being merged rigidly with the long blue rail.

## Recovered hole-center lengths from the side-profile source

Source-image geometry:

- Pivot-plate candidate ground pair P0-P1: **162.595 px**
- Purple-fork two-hole spacing: **52.010 px**
- Orange S-link hole spacing: **153.629 px**
- Tip-plate two-hole spacing: **44.102 px**

At the current scale-bound reference of 0.1 mm/px:

- Ground: **16.259 mm**
- Input rocker: **5.201 mm**
- Coupler: **15.363 mm**
- Output rocker: **4.410 mm**

These are prototype-scale candidate dimensions, not claimed factory dimensions.

## Why P0-P1 is the correct pivot-plate ground pair

Three possible hole pairs on the 3-hole pivot plate were tested against the other three identified link lengths.

Only **P0-P1** produces a near-change-point / Grashof-compatible four-bar. The other two candidate ground distances are geometrically incompatible with the recovered rocker/coupler/output lengths.

## Mobility

For the resolved distal linkage:

- planar links including ground: n = 4
- revolute lower pairs: j1 = 4

Gruebler mobility:

`M = 3(n-1) - 2j1 = 3(4-1) - 2(4) = 1`

So the distal mechanism is a valid **1-DOF four-bar**, consistent with observed tip motion.

## Updated rigid-body split

- B0: rear orange guide/support
- B1: long magenta drive link
- B2: purple fork — separate input rocker
- B3: long blue rail
- B4: green fork — separate front rocker
- B5: pivot plate / central carrier
- B6: orange S-link / distal coupler
- B7: tip plate / distal output

## Updated distal joints

- D0: B5 ↔ B2, revolute
- D1: B2 ↔ B6, revolute
- D2: B6 ↔ B7, revolute
- D3: B7 ↔ B5, revolute

The third pivot-plate hole connects toward the primary/lower branch through the green fork.

## Consequence for CAD

CAD v1.7 should rebuild the assembly with the forks as independent bodies and run the full traced-profile motion/collision sweep again. The older v1.5 body merge is deprecated.
