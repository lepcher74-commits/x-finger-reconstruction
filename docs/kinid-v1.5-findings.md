# KIN-ID v1.5 / CAD v0.5 — Motion and Collision Validation

## Scope

This stage validates the **primary-stage** mechanism over a motion sweep using the KIN-ID v1.3 identified ratios and the KIN-ID v1.4 bounded metric/Z-stack assumptions.

The distal linkage is not yet included in the dynamic collision proof and remains a separate validation task.

## Primary geometry used

Nominal metric seed:

- AB = 5.00 mm
- AC = 48.11 mm
- BD = 52.23 mm
- CD = 10.68 mm

These values combine identified dimensionless ratios with the v1.4 bounded scale assumption.

## Motion sweep

The upper-drive input angle was swept from -35° to +25° in 1° increments.

At each pose:
1. C was generated from AC and the input angle.
2. D was solved by circle intersection using BD and CD.
3. The lower assembly branch continuous with the v1.4 reference pose was selected.
4. The phalanx body axis was carried as a rigid offset from the Pivot Block orientation.

## Z-stack used

- input bracket: center Z = 0.0 mm, thickness 1.4 mm
- upper drive: center Z = +1.5 mm, thickness 1.0 mm
- lower drive: center Z = -1.5 mm, thickness 1.0 mm
- Pivot Block: center Z = 0.0 mm, thickness 1.6 mm
- upper outer phalanx rail: center Z = +3.0 mm, thickness 1.0 mm
- lower outer phalanx rail: center Z = -3.0 mm, thickness 1.0 mm

## Collision result

For the checked primary-stage body pairs:
- no 3D collisions were found in the -35° … +25° sweep;
- minimum useful face clearance for overlapping projected components was **0.50 mm**;
- the design target used for this stage was 0.30 mm.

Therefore the current nominal Z-stack passes the **primary-stage preview collision test**.

## Important limitation

This is **not yet a full functional prosthesis validation**.

Still pending:
- distal linkage motion and collision validation;
- pin/screw head envelopes;
- washer/bushing envelopes;
- tolerance stack-up;
- flexible patient interface;
- strength/fatigue checks;
- human-use safety validation.

## STL release status

CAD v0.5 has been split into separate solids for:
- input bracket;
- upper drive;
- lower drive;
- Pivot Block;
- outer phalanx rail;
- assembly preview.

All exported STL parts were checked for watertightness.

The project can now proceed to KIN-ID v1.6 / CAD v1.0, where the distal mechanism and final tolerance stack will be integrated.
