# KIN/CAD v1.5 — Reassignment of joints and rigid bodies based on multi-pose overlay

## New evidence

Five user-supplied side-view overlay poses were analyzed as one motion sequence.

This stage does **not** treat every visible hole as a valid kinematic axis. Instead, it uses motion invariance and mobility consistency to separate rigid bodies, revolute pairs and guided pairs.

## Strong proximal result

The orange proximal pivot remains stationary across all five poses:

- maximum measured image jitter: ~0.35 px.

The two holes/pins on the blue curved head preserve their mutual spacing extremely well:

- mean pair distance: ~51.36 px;
- coefficient of variation: ~0.30%.

At the same time, that rigid blue pair moves substantially relative to the orange base.

This is strong evidence that:

1. the orange proximal component belongs to Ground;
2. the blue long rail is a separate rigid body;
3. the blue head is **not** connected to the orange cam by a single fixed revolute axis;
4. the orange curved feature + blue head behave as a **guided cam / pin-in-slot style pair**.

This replaces the earlier oversimplified assumption of a pure four-bar at that interface.

## Reassigned rigid bodies

| Body | Components | Working role | Confidence |
|---|---|---|---|
| RB0 | orange cam + hand-side support | Ground | HIGH |
| RB1 | long magenta link + purple fork | upper / drive body | MEDIUM-HIGH |
| RB2 | long blue rail + green fork | guided / lower body | HIGH |
| RB3 | three-hole pivot plate | central carrier / rocker | MEDIUM-HIGH |
| RB4 | orange S-link | distal coupler | MEDIUM-HIGH |
| RB5 | tip plate | distal output | HIGH |

## Reassigned joints

| Joint | Bodies | Type | Confidence |
|---|---|---|---|
| J0 | RB0–RB1 | revolute | HIGH |
| J1 | RB0–RB2 | cam / pin-in-slot guided pair | HIGH |
| J2 | RB1–RB3 | revolute candidate | MEDIUM-HIGH |
| J3 | RB2–RB3 | revolute candidate | MEDIUM-HIGH |
| J4 | RB3-or-adjacent-rocker–RB4 | unresolved revolute | MEDIUM |
| J5 | RB4–RB5 | revolute candidate | MEDIUM-HIGH |
| J6 | RB3-or-adjacent-rocker–RB5 | unresolved output pivot | MEDIUM |

## Mobility audit

A naive distal mapping with only RB3, RB4 and RB5 connected by three revolute joints gives:

M = 3(n-1) - 2 j1
  = 3(3-1) - 2(3)
  = 0.

That would be a locked triangle, but the supplied multi-pose sequence clearly shows distal motion.

Therefore at least one of the following must be true:

- one distal pivot belongs to an additional short rocker/body;
- one pair is a guided/slot pair rather than a simple revolute;
- one earlier parent-body assignment is wrong.

The working graph therefore explicitly retains an unresolved short-rocker / slot-body candidate RX instead of forcing an impossible topology.

## Consequence for CAD

Do **not** freeze the final distal STL stack yet.

The next stage should focus on resolving J4/J6 and RX from the multi-pose overlays and the original photographs. Once that is solved, all traced profiles can be driven through a consistent 1-DOF motion model.

## Status upgrades

- Orange proximal pivot: CONFIRMED_GROUND_FEATURE
- Blue two-hole head: IDENTIFIED_RIGID_PAIR
- Blue/orange interface: IDENTIFIED_GUIDED_PAIR (exact slot contact geometry still pending)
- Direct RB3–RB4–RB5 3R triangle: REJECTED by mobility audit
