# KIN-ID v0.9 — preliminary multi-pose motion audit

## Scope

Frames from the promotional video around 150–155 s were sampled because the hand is shown from a near-side perspective while the prosthetic fingers move from a relatively extended configuration into flexion.

## Important limitation

Several prosthetic fingers overlap in these frames. Some actual pivot centres are hidden by side plates or adjacent fingers. For that reason the current point picks are classified:

**LOW-CONFIDENCE OBSERVATIONS — not IDENTIFIED linkage geometry.**

They are useful for validating the workflow and motion envelope only.

## Preliminary observation

After translating each picked chain to its proximal point, rotating the first segment onto +X, and normalizing by the first visible segment length, the later frames show increasing downward curvature.

This supports the qualitative model already adopted:

residual/input motion -> proximal mechanism -> coupled middle/distal flexion.

It does **not** yet justify assigning exact values to O/A/B/C/D/E/F/G.

## Why this step matters

The v0.8 hole-pitch measurement was suitable for geometric identification because repeated hole centres are sharply visible and internally redundant.

The promotional motion frames are different: overlap and perspective make direct pivot recovery less reliable. v0.9 therefore introduces an explicit confidence gate:

- high-repeatability repeated features can become IDENTIFIED;
- partially occluded joint picks stay OBSERVED/LOW;
- no LOW-confidence points are allowed to overwrite CAD master dimensions.

## Next gate: v1.0

Before primary linkage dimensions can be promoted to IDENTIFIED, use frames satisfying all of the following:

1. one target finger is isolated;
2. at least three relevant pivot centres are directly visible;
3. camera perspective is approximately constant;
4. the same rigid distances agree across at least three poses;
5. normalized length coefficient of variation is within the accepted tolerance.

If promotional-video frames fail this gate, use the supplied close-up photographs and assembly-video closeups as the geometric source, and use the promotional video only for motion validation.
