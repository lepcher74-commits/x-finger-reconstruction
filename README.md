# X-Finger Reconstruction

Reverse-engineering and parametric reconstruction of the mechanical, body-powered X-Finger prosthetic finger.

## Current status

**KIN-ID v0.6 / CAD Prototype v0.2**

The project separates:

1. **Master kinematics** — linkage topology and normalized geometry.
2. **Size configuration** — discrete/continuous fitting parameters.
3. **Patient fit interface** — residual-finger clamp, hand base, alignment.

## Current verified architecture

Ground / hand interface → rotating input bracket → upper/lower adjustable branches → pivot block + adjustable phalanx → distal linkage → fingertip.

A key audit correction is that **Bracket 2 is not part of Ground**: in the original patent it is pivotally attached to stationary Matrix 1. Therefore rear branch pivots move with the rotating bracket.

## Evidence classes

- **CONFIRMED** — directly documented or clearly visible in source material.
- **IDENTIFIED** — recovered consistently from multiple images/video frames.
- **ESTIMATED** — current engineering hypothesis; not manufacturing data.

## Caution

This repository is an engineering/research reconstruction. Dimensions marked ESTIMATED must not be treated as original X-Finger production dimensions or as a clinically validated prosthetic design.

## Next steps

- Joint identification of primary linkage geometry from patent figures, supplied photographs and videos.
- Identify the distal four-bar around Link 35 / Pivot Head 33.
- Recover discrete hole pitch and Z-offset stack.
- Build CAD Prototype v0.3 with physical plates, pivots and adjustment geometry.
