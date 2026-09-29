# KIN-ID v1.8 — Patent-Coupled Distal Resolution

## Result

The distal topology is resolved to **H1**.

Patent text establishes the physical chain:

- upper actuating drive 7 terminates in fork 7a;
- fork 7a connects to Link 35 through pivot pin 37;
- Link 35 connects to Pivot Head 33 through member 34;
- Pivot Head 33 pivots on inner phalanx 26 through screw 32.

Therefore the second four-bar is:

- ground: C–E (primary phalanx body);
- input: C–F (upper-drive extension);
- coupler: F–G (Link 35);
- output: E–G (Pivot Head arm).

This is exactly the previously named H1 topology.

## Important correction

The distal input is not governed by an arbitrary empirical curl law.

Because F=37 lies on the same rigid upper-drive body that participates in the primary stage, the distal input angle is driven by the **relative rotation of the upper drive with respect to the Pivot Block / phalanx body**.

This couples the two four-bars mechanically.

## Coupled sweep

Using the identified primary geometry and identified distal ratios, the patent-coupled solver closes successfully across the working branch:

- primary input: **-35° to 0°**
- distal topology: H1
- no independent distal motion law is used.

Positive motion beyond the observed reference branch does not close with this assembly branch and is not treated as the intended working direction.

## Photo discriminator

Manual side-photo picks gave a nominal gain around 1.7, but uncertainty propagation showed the photographs are too occluded/perspective-sensitive to distinguish H1/H3 reliably by gain alone.

Therefore H1 is selected by the patent-confirmed connectivity, not by over-interpreting low-confidence photo picks.

## Status upgrade

- H1 distal topology: **CONFIRMED_TOPOLOGY**
- Distal link-length ratios: **IDENTIFIED_GEOMETRY**
- Absolute metric scale: **SCALE_BOUND**
- Coupling principle upper-drive → distal input: **CONFIRMED_TOPOLOGY**
