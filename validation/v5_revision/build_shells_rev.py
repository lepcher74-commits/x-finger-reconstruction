"""Issue #7, revision stage: re-orient the two shells from the *sides* of the
green part P04 to the *top / bottom* of P04 in P04's local frame, keeping P04,
the V4 axes and the kinetics untouched.

Frame used (derived from the frozen V4 assembly, NOT from the drawing):
  * the V4 hinges turn about +Z, the whole mechanism moves in XY, so
      X = finger (proximal->distal) axis,
      Y = dorsal/ventral  -> this is "top / bottom",
      Z = lateral width   -> this is "sides".
  * P04_green bbox  x[659.44,791.73]  y[-510.21,-395.57]  z[-29.04,29.04]
    (length 132.29 x height 114.64 x width 58.08), centre y=-452.89, z=0.
The previous V5 put both shells about +Z ("on the sides"); here the grey upper
shell is about +Y and the blue lower shell about -Y, with the two side gaps
left open at +-Z.

The socket is a cap on P04's distal face (x=791.73): it extends along +X.

HONEST LIMITS
  * The model running this stage has no image input: the reference PNGs CANNOT
    be read visually, so the four labelled views are not identified and no
    dimension is taken from the picture (see STATUS.md and
    reference_measurements.json for the objective pixel data only).
  * shell_t = 1.5 is the value requested in issue #7 in V4 *model units*; it is
    NOT a calibrated physical millimetre.  Every other value is an assumed
    demonstration value.  Wearability is not claimed.

Run:  python3 validation/v5_revision/build_shells_rev.py
"""
from pathlib import Path
import json, math
import numpy as np
import cadquery as cq
from cadquery import importers
from PIL import Image

HERE = Path(__file__).resolve().parent
V4 = HERE.parent / 'work' / 'stage2' / 'assembly' / 'parts'
OUT = HERE

P = dict(
    shell_t=1.5,
    phalanx_r=24.0,
    clearance=2.0,
    y_axis=-452.89,      # P04 centre (dorsal/ventral)  -> socket axis
    z_axis=0.0,          # P04 centre (lateral)
    x_start=792.0,       # P04 distal face 791.73 -> socket cap
    x_end=872.0,
    gray_lo=24.0,        # grey upper sector, around +Y (theta measured from +Y)
    gray_hi=156.0,
    blue_lo=204.0,       # blue lower sector, around -Y
    blue_hi=336.0,
    rise=6.0,            # free-end lift of the cradle (+Y)
    n_slices=25,
    embed=0.5,
    leg_x0=791.2, leg_x1=802.0, leg_hw=7.0,   # grey stem, distal of P04 face
    wall_x0=791.2, wall_x1=802.0, wall_z=11.5, wall_half=1.6,
    wall_y=(-490.0, -472.0), wall_z_out=29.5,  # blue side walls to P04 sides
    phantom_extra=28.0,
)
P['r_in'] = P['phalanx_r'] + P['clearance']
P['r_out'] = P['r_in'] + P['shell_t']
P['z_out'] = P['wall_z_out']

GRAY = (150, 152, 157)
BLUE = (60, 110, 190)
GREEN = (115, 184, 32)
PHANTOM = (210, 190, 120)


def pol(r, th_deg):
    t = math.radians(th_deg)
    return (r * math.sin(t), r * math.cos(t))   # (u=Z, v=Y) in Workplane('YZ')


def cradle(x):
    t = min(max((x - P['x_start']) / (P['x_end'] - P['x_start']), 0.0), 1.0)
    return P['rise'] * t * t


def sector(th_lo, th_hi, r_in, r_out, x0, x1, dy=0.0):
    n = 48
    outer = [pol(r_out, t) for t in np.linspace(th_lo, th_hi, n)]
    inner = [pol(r_in, t) for t in np.linspace(th_hi, th_lo, n)]
    return (cq.Workplane('YZ').polyline(outer + inner).close()
            .extrude(x1 - x0).translate((x0, P['y_axis'] + dy, P['z_axis'])).val())


def box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0,
                            cq.Vector(x0, y0, z0))


def fuse(solids):
    res = solids[0]
    for s in solids[1:]:
        res = res.fuse(s)
    return res.clean()


def build():
    xa, xb = P['x_start'], P['x_end']
    xs = np.linspace(xa, xb, P['n_slices'])
    step = (xb - xa) / (P['n_slices'] - 1)
    x0 = lambda x: x - step * 0.55
    x1 = lambda x: x + step * 0.55

    gray, blue = [], []
    for x in xs:
        gray.append(sector(P['gray_lo'], P['gray_hi'], P['r_in'], P['r_out'],
                           x0(x), x1(x), dy=cradle(x)))
        blue.append(sector(P['blue_lo'], P['blue_hi'], P['r_in'], P['r_out'],
                           x0(x), x1(x), dy=cradle(x)))
    # grey stem to P04's distal-top corner (0.5 weld)
    ya = P['y_axis']
    gray.append(box(P['leg_x0'], P['leg_x1'], ya + P['r_out'] - 2.0,
                    -P['embed'] - 395.57, -P['leg_hw'], P['leg_hw']))
    # blue side walls linking the lower shell's +-Z edges to P04's side faces
    for s in (+1, -1):
        blue.append(box(P['wall_x0'], P['wall_x1'], P['wall_y'][0], P['wall_y'][1],
                        min(s * P['wall_z'], s * P['wall_z_out']),
                        max(s * P['wall_z'], s * P['wall_z_out'])))
    phantom = []
    for x in np.linspace(xa, xb + P['phantom_extra'], P['n_slices']):
        phantom.append(cq.Workplane('YZ').circle(P['phalanx_r'])
                       .extrude(step * 1.1).translate((x0(x), ya + cradle(x),
                                                       P['z_axis'])).val())
    return fuse(gray), fuse(blue), fuse(phantom)


def p04():
    return importers.importStep(str(V4 / 'P04_green.step')).val()


def bbox_of(s):
    b = s.BoundingBox()
    return dict(x=[round(b.xmin, 2), round(b.xmax, 2)],
                y=[round(b.ymin, 2), round(b.ymax, 2)],
                z=[round(b.zmin, 2), round(b.zmax, 2)])


def render(solids, png):
    """Four orthographic panels + a P04-registered contour overlay.

    All panels use the *global assembly* coordinates and an equal aspect with a
    single scale per panel: P04, grey and blue are never scaled independently.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    def tri(solid):
        v, f = solid.tessellate(1.0, 0.4)
        return np.array([[p.x, p.y, p.z] for p in v]), np.array(f)

    pv, pf = tri(p04())
    parts = [(GREEN, *tri(solids[0])), (GRAY, *tri(solids[1])),
             (BLUE, *tri(solids[2]))]
    # views: name, horizontal index+sign, vertical index+sign
    views = [('front (look -Z): X vs Y', 0, 1),
             ('top (look -Y): X vs Z', 0, 2),
             ('side (look +X): Z vs Y', 2, 1),
             ('back (look +Z): X vs Y', 0, 1)]
    fig, axes = plt.subplots(2, 2, figsize=(11, 10))
    for ax, (title, hi, vi) in zip(axes.ravel(), views):
        for col, v, f in parts:
            xy = v[:, [hi, vi]].copy()
            if title.startswith('back'):
                xy[:, 0] = -xy[:, 0]
            for t in f:
                p = xy[t]
                ax.fill(p[:, 0], p[:, 1], color=np.array(col) / 255, alpha=0.35,
                        lw=0.2, edgecolor='k', zorder=2 if col != GREEN else 3)
        ax.set_title(title, fontsize=8)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel('', fontsize=6); ax.set_ylabel('', fontsize=6)
    fig.suptitle('V5 revision: P04 (green) + grey upper (+Y) + blue lower (-Y); '
                 'global assembly scale, no independent scaling', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / png, dpi=130)
    plt.close(fig)


def main():
    gray, blue, phantom = build()
    p = p04()
    report = dict(
        frame_note='X finger axis, Y top/bottom (+Y grey upper, -Y blue lower), '
                   'Z lateral sides; P04 axes/kinematics unchanged',
        assumed_values={k: v for k, v in P.items()},
        scale_note='V4 model units, shell_t=1.5 is the issue value in model '
                   'units, NOT calibrated physical mm',
        p04=dict(bbox=bbox_of(p), solids=len(p.Solids())),
        gray_upper=dict(bbox=bbox_of(gray), solids=len(gray.Solids()),
                        volume=round(gray.Volume(), 2), valid=gray.isValid()),
        blue_lower=dict(bbox=bbox_of(blue), solids=len(blue.Solids()),
                        volume=round(blue.Volume(), 2), valid=blue.isValid()),
    )
    cq.exporters.export(cq.Workplane(obj=gray), str(OUT / 'P10_gray_upper.step'))
    cq.exporters.export(cq.Workplane(obj=blue), str(OUT / 'P11_blue_lower.step'))
    cq.exporters.export(cq.Workplane(obj=gray), str(OUT / 'P10_gray_upper.stl'))
    cq.exporters.export(cq.Workplane(obj=blue), str(OUT / 'P11_blue_lower.stl'))
    render([gray, blue, phantom], 'four_views_p04_registered.png')
    json.dump(report, open(OUT / 'shells_revision_report.json', 'w'), indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
