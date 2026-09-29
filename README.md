# X-Finger Reconstruction

Reverse-engineering and parametric reconstruction of the mechanical, body-powered X-Finger prosthetic finger.

## Current status

**KIN-ID v0.7 / CAD Prototype v0.3**

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

## v0.7 / v0.3 additions

- reproducible multi-frame KIN-ID fitting scaffold;
- assembly-video observation register;
- first metric seed parameter table;
- parametric OpenSCAD prototype with two Z-separated adjustable branches;
- confirmed assembly hardware constraints: M1.4×5L proximal, small-size 4L note, M1.4×2L distal.

## Caution

This repository is an engineering/research reconstruction. Dimensions marked ESTIMATED must not be treated as original X-Finger production dimensions or as a clinically validated prosthetic design.

## Next steps

- Digitize primary pivots from multiple video frames and photographs.
- Fit one constant moving-base linkage across all selected poses.
- Recover the distal Link 35 / Pivot Head 33 geometry.
- Replace seed hole pitch / thickness / Z offsets with identified values.
- Advance to CAD Prototype v0.4 with a true distal four-bar and interference checks.
