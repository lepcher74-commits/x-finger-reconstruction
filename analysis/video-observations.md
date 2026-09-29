# Video observations — KIN-ID v0.7

## Assembly video

Project-supplied file: X-Finger assembly video.

### Confirmed observations

- Four main contemporary modules are shown separately before assembly.
- The hinge/input section connects to the main finger body through two perforated branches.
- Upper and lower branches must be installed with corresponding hole index positions.
- The branches occupy different Z layers.
- Fastener instruction visible in the assembly video:
  - proximal side: **M1.4×5L**;
  - small size: **4L** noted for that proximal fastener;
  - distal side: **M1.4×2L** for regular/small.
- Multiple discrete adjustment holes are visible in both upper and lower bars.

### Important geometric implication

The assembly is not adequately represented as a single flat four-bar.
The CAD master must preserve:
1. moving input bracket;
2. matched upper/lower branch indexing;
3. Z-offset layer stack;
4. downstream distal coupling.

## Promotional / motion video

Used as dynamic evidence only.
The relevant fitting target is not a single pose but the functions

q_residual -> q_input -> q_primary -> q_distal

across many frames.

## Current metrology policy

No absolute mechanism dimension is accepted solely from a perspective frame.
Known M1.4 hardware is used only as a calibration constraint together with
multiple images, not as a one-frame shortcut.
