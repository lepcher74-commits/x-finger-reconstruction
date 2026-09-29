# KIN-ID v1.3 Findings

## Objective

Close the primary four-point drive geometry using an independent source from the previous photographic rigid-body test.

## Source

The project-supplied side CAD rendering contains two mirrored side views of the same primary-stage architecture.

Four corresponding anchors were digitized in each view:

- Q0 / Q1 — hinge/input-side anchors.
- Q2 / Q3 — main-body / Pivot-Block-side anchors.

The lower rendering was mirrored and registered to the upper rendering with a 2D similarity transform.

## Registration result

Similarity-fit RMS residual:

**1.45 px**

This is small relative to the roughly 180–195 px long drive members and supports the interpretation that the same four-anchor geometry is present in both views.

## Working mapping to patent topology

The original patent states that:

- upper operating drive attaches to Bracket 2 through pivot 4a;
- upper actuating drive attaches to Pivot Block 10 through pivot 11;
- lower drive attaches to Bracket 2 through pivot 13a;
- lower drive attaches to Pivot Block 10 through pivots 13b.

Therefore the current working correspondence is:

- Q0/Q1 = the two Bracket/input-side anchors (4a / 13a, exact order pending);
- Q2/Q3 = the two Pivot-Block-side anchors (11 / 13b, exact order pending).

This closes a **candidate primary quadrilateral**, but the exact numbering of the two upper/lower points remains a mapping task.

## Identified normalized geometry

Using mean Q0-Q1 as AB = 1:

- AB = 1.0000
- AC = 9.6217
- BD = 10.4463
- CD = 2.1357

Cross-view disagreement:

- AB: 6.35 %
- AC: 2.01 %
- BD: 0.63 %
- CD: 6.77 %

The long drive lengths are substantially more stable than the short transverse spacings, as expected from limited image resolution.

## Status

- Four-anchor primary-stage geometry: **IDENTIFIED_GEOMETRY**
- Exact mapping Q0/Q1 to 4a/13a: **CANDIDATE_MAPPING**
- Exact mapping Q2/Q3 to 11/13b: **CANDIDATE_MAPPING**
- Absolute scale: **PENDING**
- Manufacturing dimensions: **NOT YET RELEASED**

## Consequence for STL roadmap

KIN-ID v1.3 has supplied the closed normalized primary-stage geometry needed before scale recovery.

Next: **KIN-ID v1.4 — metric scale and Z-stack**.
