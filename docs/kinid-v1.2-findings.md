# KIN-ID v1.2 findings

## Objective

Map the rigid triangle identified in v1.1 to the original patent structure and avoid forcing an incorrect fourth point into the primary linkage.

## Patent cross-check

The patent states that the upper actuating drive connects to Pivot Block 10 through pivot screw 11. The lower actuating drive connects to Pivot Block 10 through stirrup pin pivoting screws 13b. Pivot Block 10 is subsequently fastened into Outer Phalange 18 using screw 22 and screw 25.

This creates a strong mechanical expectation: visible axes 11 and 13b plus structural fasteners 22/25 should move as one rigid assembly once Pivot Block 10 is installed in the phalange.

## Image result

Across the supplied extended/flexed side-view pair, landmarks R0-R1-R2 preserve their internal geometry to approximately 1–2% for the strongest pairwise ratios, while R3 does not.

Therefore:

- R0 and R1 are the strongest candidates for the two Pivot Block articulation axes 11 and 13b.
- R2 is more consistent with a Pivot Block / Outer Phalange structural fastening location (22/25 region) than with an independent drive pivot.
- R3 must not be treated as a fixed Pivot Block point. It is either a point on another moving link or a misidentified visual center.

## Status

R0-R1-R2: **IDENTIFIED_SUBASSEMBLY**

R0/R1 exact assignment to 11 vs 13b: **CANDIDATE_MAPPING**

R2 exact assignment to 22 vs 25: **CANDIDATE_MAPPING**

R3: **REJECTED_FROM_RIGID_SUBASSEMBLY**

## Consequence for the model

The v1.1 triangle is not evidence for a new four-bar by itself. It is evidence for the geometry of the Pivot Block / phalange rigid assembly.

The next identification task is to find the actual opposite pivots of the upper and lower drives in the input/ground-side structure and close the primary four-bar against the already-identified 11/13b pair.
