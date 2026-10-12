"""Build the P04-normalised proportion table for the four reference views.

Combines the objective pixel measurements (reference_measurements.json) with the
CAD bounding boxes of P04 and the revision shells.  The reference views are
kept as anonymous cells (view 1..4) because the drawings cannot be read
visually in this run (no image input in the model) -- see STATUS.md.
"""
from pathlib import Path
import json
import numpy as np
from cadquery import importers

HERE = Path(__file__).resolve().parent
V4 = HERE.parent / 'work' / 'stage2' / 'assembly' / 'parts'

ref = json.load(open(HERE / 'reference_measurements.json'))
rev = json.load(open(HERE / 'shells_revision_report.json'))


def bbox(step):
    b = importers.importStep(str(step)).val().BoundingBox()
    return dict(dx=round(b.xmax - b.xmin, 2), dy=round(b.ymax - b.ymin, 2),
                dz=round(b.zmax - b.zmin, 2))


p04 = bbox(V4 / 'P04_green.step')
gray = rev['gray_upper']['bbox']
blue = rev['blue_lower']['bbox']
cad = {
    'P04_green': p04,
    'P10_gray_upper': dict(dx=round(gray['x'][1] - gray['x'][0], 2),
                           dy=round(gray['y'][1] - gray['y'][0], 2),
                           dz=round(gray['z'][1] - gray['z'][0], 2)),
    'P11_blue_lower': dict(dx=round(blue['x'][1] - blue['x'][0], 2),
                           dy=round(blue['y'][1] - blue['y'][0], 2),
                           dz=round(blue['z'][1] - blue['z'][0], 2)),
}

# CAD ratio of the shell envelope to P04 (the same part used for mounting)
cad_ratios = {
    'P10_gray_upper/P04': {k: round(cad['P10_gray_upper'][k] / p04[k], 2)
                           for k in ('dx', 'dy', 'dz')},
    'P11_blue_lower/P04': {k: round(cad['P11_blue_lower'][k] / p04[k], 2)
                           for k in ('dx', 'dy', 'dz')},
}

# reference: per view, ratio of blue (shell) pixel extent to green (P04)
ref_rows = []
for v in ref['socket_views.png']['views']:
    g, b = v.get('green'), v.get('blue')
    r = {'view': v['view_index'], 'cell_xyxy': v['cell_xyxy'],
         'green_px_wh': [g['w'], g['h']] if g else None,
         'blue_px_wh': [b['w'], b['h']] if b else None}
    if g and b:
        r['blue_w/green_w'] = round(b['w'] / g['w'], 2)
        r['blue_h/green_h'] = round(b['h'] / g['h'], 2)
    ref_rows.append(r)

out = dict(
    note='Reference view labels/axes are NOT identified (image not readable in '
         'this run).  Reference ratios use blue-pixel extents over green-pixel '
         'extents per cell; drawing error is not calibrated.',
    p04_green_cad=p04,
    cad_shell_envelope=cad,
    cad_ratio_shell_over_p04=cad_ratios,
    reference_views=ref_rows,
)
json.dump(out, open(HERE / 'proportions_table.json', 'w'), indent=2)
print(json.dumps(out, indent=2))
