# CAD v2.0 RC — Audit Before v3.0

## Why v2.0 RC is not manufacturing-valid
The RC is useful as a research baseline, but not as a faithful full assembly.

### Structural issues
- Several traced profiles are incomplete.
- Fork cheeks are inconsistently split as separate physical pieces.
- Some joints are represented only by coincident holes.
- Some physical pieces are merged in the assembly model.
- Adjustment bars/telescoping elements are not fully represented as separate parts.
- Fasteners are partly symbolic envelopes rather than true hardware.
- Some joints have candidate fastener assignments only.
- Shell/cover parts are mixed with kinematic elements in places.
- The Z-stack is an engineering candidate, not source-proven.

### Required v3.0 remediation
- rebuild component tree from source evidence;
- re-extract incomplete profiles;
- reassign all functional holes;
- explicitly model each axis;
- explicitly model spacers/washers;
- convert adjustment systems into real sliding/overlap subassemblies;
- distinguish mirrored cheek pairs from central links;
- add hardware as separate components;
- verify extended/intermediate/flexed states from the same assembly;
- perform solid-to-solid collision checking.

## Status of CAD v2.0
REFERENCE BASELINE ONLY.

Do not continue by simply editing or thickening the current STL.
