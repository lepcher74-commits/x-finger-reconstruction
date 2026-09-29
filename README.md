# X-Finger Reconstruction

Reverse-engineering and parametric reconstruction of the mechanical, body-powered X-Finger prosthetic finger.

## Current status

**KIN-ID v0.9 / CAD Prototype v0.3**

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
- **OBSERVED / LOW** — visible trend or manual pick with insufficient geometric certainty.
- **ESTIMATED** — current engineering hypothesis; not manufacturing data.

## Current identification results

- repeated upper/lower adjustment-hole pitch is internally consistent in the assembly-video closeup;
- promotional-video frames 150–155 s confirm the expected coupled flexion trend;
- those motion-frame joint picks remain LOW-confidence because of overlap and occlusion and are not allowed to drive manufacturing dimensions.

## Caution

This repository is an engineering/research reconstruction. Dimensions marked ESTIMATED or OBSERVED must not be treated as original X-Finger production dimensions or as a clinically validated prosthetic design.

## Next steps

- Select isolated-finger frames with directly visible pivots.
- Fit constant rigid lengths across at least three poses.
- Recover O/A/B/C/D first; then E/F/G distal geometry.
- Promote parameters to IDENTIFIED only after cross-frame consistency checks.
- Advance the CAD model only from IDENTIFIED or explicitly labelled prototype assumptions.
