# KIN-ID v1.4 — Metric Scale + Z-Stack

## Outcome

KIN-ID v1.4 establishes a bounded metric envelope sufficient for a **preview STL**.

The source material does not contain a factory dimensional drawing, so absolute values that are not explicitly documented remain bounded estimates.

## Confirmed hardware

Assembly video explicitly shows:
- proximal connection: M1.4×5L;
- small-size note: M1.4×4L;
- distal connection: M1.4×2L.

These values are CONFIRMED.

## Metric seed

The adjustment-hole pitch is retained at a nominal **5.0 mm**, with a conservative working interval of **4.0–6.0 mm**.

This is not asserted as the original production dimension.

Using the KIN-ID v1.3 primary ratios:
- AB = 1.000
- AC = 9.622
- BD = 10.446
- CD = 2.136

and setting nominal AB ≈ one adjustment pitch gives the preview metric seed:
- AB = 5.0 mm
- AC = 48.1 mm
- BD = 52.2 mm
- CD = 10.7 mm

## Z-stack seed

Preview CAD uses:
- plate thickness: 1.0 mm, bounded 0.8–1.2 mm;
- upper/lower branch centre-plane separation: 3.0 mm, bounded 2.4–3.6 mm;
- adjustment bar width: 4.0 mm, bounded 3.2–4.8 mm;
- preview M1.4 clearance hole: 1.8 mm as a design reference.

## Status

The metric model is sufficient for geometric visualization and printable mock-up review.

It is **not yet a functional release**. KIN-ID v1.5 must perform:
- full motion sweep;
- inter-part collision check;
- minimum edge-distance review;
- fastener-stack verification;
- separate-part export.
