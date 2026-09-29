# KIN-ID v1.1 findings

## Goal

Test whether candidate proximal landmarks remain geometrically invariant between two side-view states of the same X-Finger mechanism.

## Source states

Two project-supplied side photographs:
- extended state;
- flexed state.

The local proximal mechanism was manually digitized with neutral labels R0..R3. Neutral labels are intentional because exact mapping to patent axes O/A/B/C/D is not yet secure.

## Measurement uncertainty

Manual center-pick uncertainty is estimated at approximately ±4–6 pixels because of blur, perspective, partial occlusion and reflective hardware.

## Cross-state test

Each frame was normalized by R0-R1.

Measured normalized ratios:

- R0-R2: 2.1756 extended, 2.1300 flexed; disagreement ≈ 2.12%.
- R1-R2: 1.1793 extended, 1.1946 flexed; disagreement ≈ 1.28%.
- R0-R3: disagreement ≈ 15.45%.
- R1-R3: disagreement ≈ 7.52%.
- R2-R3: disagreement ≈ 31.86%.

## Conclusion

R0, R1 and R2 form a strong candidate for a rigid proximal subassembly. Their relative geometry is consistent across the two states within roughly 1–2%.

R3 fails the invariance test. At least one of the following is therefore true:

1. R3 is not on the same rigid body;
2. the chosen visual feature is not the actual pivot center;
3. R3 is strongly affected by perspective/occlusion.

Accordingly:

- triangle R0-R1-R2 is promoted to **IDENTIFIED_SUBASSEMBLY**;
- R3 remains **OBSERVED_LOW_CONFIDENCE**;
- exact patent-axis mapping remains pending.

## Identified normalized triangle

Using |R0R1| = 1:

- |R0R2| ≈ 2.1528
- |R1R2| ≈ 1.1870

These are geometric ratios only, not millimetres.

## Next action

Use assembly close-ups and patent figures to map R0/R1/R2 onto O/A/B/C/D and locate the missing fourth primary pivot without forcing a false quadrilateral.
