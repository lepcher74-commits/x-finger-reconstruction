# CAD v1.9a — Fastener Mapping Correction

## Problem found

The first v1.9 mapping assigned the confirmed distal-family M1.4×2L fastener directly to J7.

However, the current reconstructed J7 layer stack is approximately:

- tip plate: 1.2 mm
- central link: 1.0 mm

Total modeled stack: **2.20 mm** before any usable thread reserve.

Therefore a direct M1.4×2L assignment is mechanically incompatible with the current model.

## Correction

The M1.4×2L item remains **CONFIRMED SOURCE EVIDENCE** for a distal connection, but its exact reconstructed joint is now marked unresolved.

For the current prototype geometry:

- J7 uses M1.4×4L as a design-candidate fastener.
- The source-confirmed ×2L fastener is retained in the discrepancy register until the exact original thin/tapped distal interface is identified.

## Engineering rule

Do not force source hardware evidence onto a reconstructed joint when the modeled stack does not physically fit.

## Current evidence classes

- M1.4 nominal family — CONFIRMED.
- 5L proximal-family length — CONFIRMED.
- 4L small-version note — CONFIRMED.
- 2L distal-family length — CONFIRMED.
- Joint-by-joint allocation — PROTOTYPE CANDIDATE unless independently verified.
