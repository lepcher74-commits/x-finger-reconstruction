# CAD v1.9 — Build BOM + Fastener Map

## Scope

This stage converts the current CAD v1.8a assembly into a build-oriented bill of materials and fastener map.

Important: fastener-family evidence and joint-by-joint assignments are tracked separately.

## Confirmed fastener-family evidence

From the assembly video:

- M1.4×5L proximal-family fastener.
- M1.4×4L note for the small version.
- M1.4×2L distal-family fastener.

These are confirmed as source evidence, but they are **not automatically mapped to every reconstructed joint**.

## Prototype build rule

A candidate screw length is accepted only when:

usable length reserve >= 0.50 mm

after subtracting the modeled plate/washer stack.

## Candidate joint map

- J0 upper proximal drive pivot — M1.4×5L candidate.
- J1 lower proximal drive pivot — M1.4×5L candidate.
- J2 upper clevis → central rocker — M1.4×5L candidate.
- J3 lower clevis → central rocker — M1.4×5L candidate.
- J4 distal input rocker pivot — M1.4×5L candidate.
- J5 distal S-link coupler pivot — M1.4×4L candidate.
- J6 distal output / tip rocker pivot — M1.4×4L candidate.
- J7 tip shell / cover hinge — provisional; see v1.9a correction.

## Status

The BOM is suitable for prototype planning only. It is not a claim of original factory hardware allocation.
