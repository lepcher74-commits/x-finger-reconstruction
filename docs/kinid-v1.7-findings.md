# KIN-ID v1.7 — Distal Closure Candidates

## Objective

Replace the free-form distal curl law used in CAD v1.0 with a closed four-bar candidate based on the identified P0...P4 geometry from KIN-ID v1.0.

## Candidate topologies

Three four-bar interpretations were evaluated.

- H1: ground P0-P1, input arm P0-P2, output arm P1-P3, coupler P2-P3.
- H2: ground P0-P1, input arm P0-P3, output arm P1-P2, coupler P3-P2.
- H3: ground P0-P2, input arm P0-P1, output arm P2-P3, coupler P1-P3.

## Result

H2 has only a narrow continuous interval around the observed pose and is not retained.

H1 and H3 both have one-sided continuous motion branches extending roughly 45 degrees from the observed pose, but in opposite input directions. This matters because the prosthesis primarily moves one-way from extension toward flexion.

Local output gain near the observed pose:

- H1: approximately 0.55 deg output / deg input.
- H3: approximately 3.0 deg output / deg input.

Therefore H1 and H3 remain competing candidate topologies. No final mapping to patent axes is asserted yet.

## Important correction

An initial rejection of H1 based on loss of closure for positive input was too strong. Because the physical device operates over a one-sided flexion branch, H1 remains geometrically viable over the opposite direction.

## Next discriminator

Use motion video to track at least three distal pivot centers through flexion. Compare measured output/input angular gain against H1 and H3.

Status:
- H1: CANDIDATE_TOPOLOGY
- H2: REJECTED_FOR_WORKING_RANGE
- H3: CANDIDATE_TOPOLOGY
