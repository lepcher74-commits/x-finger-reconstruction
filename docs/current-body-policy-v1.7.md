# Current Kinematic Body Policy — v1.7

## Core rule

A **physical plate** is not necessarily a distinct **kinematic body**.

Two fork cheeks separated in Z but fastened together around one link are modeled as one rigid body.

## Working body groups

- **GROUND / Matrix / hand-side support**
- **Upper adjustable drive body**
- **Lower adjustable drive body**
- **Central Pivot Block / carrier**
- **Distal input rocker**
- **Distal coupler**
- **Distal output / fingertip body**
- **Non-kinematic shells/covers**

## Adjustment vs operational DOF

Telescopic/perforated adjustments are configuration DOFs during fitting.
Once locked by paired screws they are removed from the operational mobility count.

## Rejected / downgraded hypotheses

- Proximal operational cam/slot pair: downgraded to NOT SUPPORTED.
- Treating every doubled fork cheek as a separate moving link: rejected.
- Inferring exact M1.4/M2 hardware from secondary render proportions: rejected.
