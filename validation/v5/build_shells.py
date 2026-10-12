"""V5: two open 1.5-unit shells (gray upper P10 + blue lower P11) for the
residual phalanx, mounted on the existing green part P04 of the frozen V4
assembly.

Stage of issue #7 that was resumed from the saved build (artifact
cad-validation-38204875171).  It fixes the defects of the previous save:

  * P11 used to be 3 disconnected solids (arc + two floating walls) -> now the
    side walls are welded into the arc, so each shell is ONE solid;
  * both shells used to intersect P01 (they started too far proximal, inside
    the black block) -> the socket now starts at x_start, distal of P01;
  * the two shells used to intersect each other -> the angular sectors now
    leave explicit side gaps;
  * P11 used to intersect the assumed phalanx -> the cradle curve is applied to
    the phalanx too, so the radial clearance stays constant along the length;
  * the old thickness estimate 2V/(A_out+A_in) mixed in the leg and the walls ->
    thickness is now measured on the shell walls only, as r_out - r_in along
    the radial normal, and confirmed with the minimum face distance.

The old V4 parts, their axes and the kinematics are NEVER modified.  The V4
scale is conventional (uncalibrated); the 1.5 wall is the value requested in
issue #7 and is applied in V4 model units.  This is a parametric demonstration,
wearability is not claimed.

Run:  python3 validation/v5/build_shells.py
"""
from pathlib import Path
import json, math
import numpy as np
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCP.gp import gp_Lin, gp_Pnt, gp_Dir
from OCP.TopAbs import TopAbs_State
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from PIL import Image, ImageDraw, ImageFont

D = Path(__file__).resolve().parent
V4 = D.parent / 'work' / 'stage2' / 'assembly'
V4PARTS = V4 / 'parts'
OUT = D

# ---------------------------------------------------------------------------
# Parametric demonstration dimensions (V4 model units).
# Fit dimensions race unknown; every value here is an assumed demo value except
# shell_t, which is the 1.5 requested in issue #7.
# ---------------------------------------------------------------------------
P = dict(
    shell_t=1.5,            # wall thickness (issue #7), applied along the normal
    phalanx_r=24.0,         # assumed residual-phalanx radius (demo)
    clearance=2.0,          # radial clearance phalanx -> inner wall (demo)
    y_center=-420.0,        # socket axis y = finger centre line (demo)
    z_ref=29.0,             # P04 top face (mounting surface)
    # The socket is rigidly attached to P04.  P01 sweeps the band
    # x <= 734, z 29..46 in P04's resting frame over the 74 V4 poses (computed
    # from motion.json); the socket therefore starts distal of that band so no
    # pose can drive P01 into it.
    x_start=744.0,          # socket fixed end (distal of P01's P04-frame xmax)
    x_end=824.0,            # socket/cradle free end
    gray_lo=-62.0,          # gray upper sector, deg from +Z toward +Y
    gray_hi=62.0,
    blue_lo=118.0,          # blue lower sector (leaves two side gaps 62..118)
    blue_hi=242.0,
    rise=6.0,               # longitudinal lift of the cradle at the free end
    n_slices=25,            # slices approximating the longitudinal curve
    wall_len=1.6,           # side wall thickness of the blue lower shell
    wall_hi=46.0,           # top z of the blue side walls
    leg_hw=7.0,             # gray leg half width (y)
    leg_x0=744.0,           # gray leg back face
    leg_x1=760.0,           # gray leg front face (in front of the phalanx)
    blue_x0=762.0,          # blue shell / phalanx start (clear of the leg)
    embed=0.5,              # designed weld penetration into P04 top
    phantom_extra=28.0,     # assumed phalanx length beyond the free end
)
P['r_in'] = P['phalanx_r'] + P['clearance']
P['r_out'] = P['r_in'] + P['shell_t']
P['z_axis'] = P['z_ref'] - P['embed'] + P['r_out']   # blue bottom touches P04

GRAY_COLOR = (150, 152, 157)
BLUE_COLOR = (60, 110, 190)
GREEN_COLOR = (115, 184, 32)
PHANTOM_COLOR = (210, 190, 120)


def polar(r, phi_deg):
    a = math.radians(phi_deg)
    return (r * math.sin(a), r * math.cos(a))


def cradle(x, p):
    """Longitudinal cradle curve (lift, +Z) at position x."""
    t = min(max((x - p['x_start']) / (p['x_end'] - p['x_start']), 0.0), 1.0)
    return p['rise'] * t * t


def sector_x(phi_lo, phi_hi, r_in, r_out, x0, x1):
    """Annular sector in YZ, extruded from x0 to x1, centred on the local axis."""
    mid = 0.5 * (phi_lo + phi_hi)
    return (cq.Workplane('YZ')
            .moveTo(*polar(r_out, phi_lo))
            .threePointArc(polar(r_out, mid), polar(r_out, phi_hi))
            .lineTo(*polar(r_in, phi_hi))
            .threePointArc(polar(r_in, mid), polar(r_in, phi_lo))
            .close()
            .extrude(x1 - x0)
            .translate((x0, 0.0, 0.0))
            .val())


def box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def fuse(solids):
    res = solids[0]
    for s in solids[1:]:
        res = res.fuse(s)
    return res.clean()


def build_shells(p):
    """Return (gray, blue, phantom); each of gray/blue is one connected solid."""
    yc = p['y_center']
    xa, xb = p['x_start'], p['x_end']
    xs = np.linspace(xa, xb, p['n_slices'])
    step = (xb - xa) / (p['n_slices'] - 1)
    x0 = lambda x: x - step * 0.55                       # slice overlap
    x1 = lambda x: x + step * 0.55

    gray, blue = [], []
    for x in xs:
        dz = cradle(x, p)
        gray.append(sector_x(p['gray_lo'], p['gray_hi'], p['r_in'], p['r_out'],
                             x0(x), x1(x)).translate((0, yc, p['z_axis'] + dz)))
    for x in np.linspace(p['blue_x0'], xb, p['n_slices']):
        dz = cradle(x, p)
        blue.append(sector_x(p['blue_lo'], p['blue_hi'], p['r_in'], p['r_out'],
                             x0(x), x1(x)).translate((0, yc, p['z_axis'] + dz)))
    # blue side walls: vertical plates welded into the angular ends of the arc,
    # running the blue length and dropping to the P04 top face.
    for phi in (p['blue_lo'], p['blue_hi']):
        u = p['r_out'] * math.sin(math.radians(phi))
        inner = u - math.copysign(p['wall_len'], u)
        for x in np.linspace(p['blue_x0'], xb, p['n_slices']):
            dz = cradle(x, p)
            ztop = p['z_axis'] + dz + p['r_out'] * math.cos(math.radians(phi)) + 3.0
            blue.append(box(x0(x), x1(x),
                            min(u, inner) + yc, max(u, inner) + yc,
                            p['z_ref'] - p['embed'], ztop))
    # gray central leg at the back, welded into the top shell and onto P04.
    gray.append(box(p['leg_x0'], p['leg_x1'],
                    yc - p['leg_hw'], yc + p['leg_hw'],
                    p['z_ref'] - p['embed'], p['z_axis'] + p['r_in'] + 1.0))

    phantom = []
    for x in np.linspace(p['blue_x0'], xb + p['phantom_extra'], p['n_slices']):
        dz = cradle(x, p)
        phantom.append(cq.Workplane('YZ').center(0, 0).circle(p['phalanx_r'])
                       .extrude(step * 1.1)
                       .translate((x0(x), yc, p['z_axis'] + dz)).val())
    return fuse(gray), fuse(blue), fuse(phantom)


# ---------------------------------------------------------------------------
# Thickness on the shell walls only (leg and side walls excluded).
# ---------------------------------------------------------------------------
def cyl_radius(face):
    s = BRepAdaptor_Surface(face.wrapped)
    if s.GetType() == GeomAbs_SurfaceType.GeomAbs_Cylinder:
        return s.Cylinder().Radius()
    return None


def _inside(cls, pt):
    cls.Perform(gp_Pnt(pt.x, pt.y, pt.z), 1e-6)
    return cls.State() == TopAbs_State.TopAbs_IN


def _ray_exit(solid, origin, direction):
    """Distance from origin (inside the material) to the first boundary exit
    along direction, measured by intersecting a ray with the solid."""
    it = IntCurvesFace_ShapeIntersector()
    it.Load(solid.wrapped, 1e-7)
    it.Perform(gp_Lin(gp_Pnt(*origin), gp_Dir(*direction)), 1e-4, 1000.0)
    o = cq.Vector(*origin)
    d = cq.Vector(*direction).normalized()
    ts = []
    for i in range(1, it.NbPnt() + 1):
        q = it.Pnt(i)
        t = (cq.Vector(q.X(), q.Y(), q.Z()) - o).dot(d)
        if t > 1e-4:
            ts.append(t)
    return min(ts) if ts else None


def _radial(p, cyl):
    ax = cyl.Axis()
    loc, dr = ax.Location(), ax.Direction()
    v = cq.Vector(p.x - loc.X(), p.y - loc.Y(), p.z - loc.Z())
    dd = cq.Vector(dr.X(), dr.Y(), dr.Z()).normalized()
    return v.sub(dd.multiply(v.dot(dd))).normalized()


def shell_thickness(solid, target, n=6):
    """Wall thickness measured directly along the surface normal.

    For every sampled point on the cylindrical shell walls a ray is marched
    into the material (outward from an inner wall, inward from an outer wall)
    and the distance to the first boundary exit is taken.  This is a real
    measurement, not `r_out - r_in`.

    Two face-distance figures are also reported to expose the earlier
    contradiction: `face_dist_cross_slice` is the minimum over ALL inner/outer
    face pairs (this is the 1.06398 in the old report, a *wrong pair* between
    neighbouring slices whose axes are shifted by the cradle lift), while
    `face_dist_coaxial` restricts the pairs to faces sharing one cylinder axis
    (the true, same-wall gap).
    """
    cls = BRepClass3d_SolidClassifier(solid.wrapped)
    cyl = {}
    for f in solid.Faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        if ad.GetType() == GeomAbs_SurfaceType.GeomAbs_Cylinder:
            cyl.setdefault(round(ad.Cylinder().Radius(), 3), []).append((f, ad.Cylinder()))
    radii = sorted(cyl)
    if len(radii) < 2:
        return dict(target=target, radii=radii, error=None,
                    method='no pair of wall cylinders found')

    # minimum inner/outer face distance, all pairs vs coaxial pairs
    def axis_key(c):
        ax = c.Axis(); loc, dr = ax.Location(), ax.Direction()
        return (round(loc.X(), 1), round(loc.Y(), 1), round(loc.Z(), 1),
                round(dr.X(), 3), round(dr.Y(), 3), round(dr.Z(), 3))
    r_in, r_out = radii[0], radii[-1]
    d_cross, d_coax = None, None
    for fi, ci in cyl[r_in]:
        ki = axis_key(ci)
        for fo, co in cyl[r_out]:
            try:
                d = fi.distance(fo)
            except Exception:
                continue
            d_cross = d if d_cross is None else min(d_cross, d)
            if axis_key(co) == ki:
                d_coax = d if d_coax is None else min(d_coax, d)

    # direct normal-ray thickness on the walls, with zones along x
    samples = []
    for r, faces in cyl.items():
        for f, c in faces:
            ad = BRepAdaptor_Surface(f.wrapped)
            u0, u1 = ad.FirstUParameter(), ad.LastUParameter()
            v0, v1 = ad.FirstVParameter(), ad.LastVParameter()
            for iu in range(n + 1):
                for iv in range(n + 1):
                    u = u0 + (u1 - u0) * (0.1 + 0.8 * iu / n)
                    v = v0 + (v1 - v0) * (0.1 + 0.8 * iv / n)
                    p = f.positionAt(u, v)
                    rad = _radial(p, c)
                    d = rad if _inside(cls, p.add(rad.multiply(0.12))) else rad.multiply(-1.0)
                    if not _inside(cls, p.add(d.multiply(0.12))):
                        continue
                    t = _ray_exit(solid, p.add(d.multiply(0.05)), (d.x, d.y, d.z))
                    if t is None:
                        continue
                    samples.append((t + 0.05, r, p.x, p.z))
    if not samples:
        return dict(target=target, radii=radii, error=None,
                    method='no wall samples could be measured')
    samples.sort()
    tv = [s[0] for s in samples]
    xmin = min(s[2] for s in samples); xmax = max(s[2] for s in samples)
    zones = []
    for b in range(6):
        lo = xmin + (xmax - xmin) * b / 6
        hi = xmin + (xmax - xmin) * (b + 1) / 6
        z = [s[0] for s in samples if lo <= s[2] <= hi]
        if z:
            zones.append(dict(x=[round(lo, 1), round(hi, 1)],
                              min=round(min(z), 4), max=round(max(z), 4)))
    return dict(
        target=target, radii=radii, r_in=r_in, r_out=r_out,
        nominal=round(r_out - r_in, 6),
        measured_min=round(samples[0][0], 4),
        measured_max=round(samples[-1][0], 4),
        measured_mean=round(sum(tv) / len(tv), 4),
        n_samples=len(samples),
        measured_min_zone=dict(x=round(samples[0][2], 2), z=round(samples[0][3], 2),
                               r=samples[0][1]),
        face_dist_cross_slice=round(float(d_cross), 6) if d_cross is not None else None,
        face_dist_coaxial=round(float(d_coax), 6) if d_coax is not None else None,
        zones=zones,
        error=round(abs((r_out - r_in) - target), 6),
        method='thickness measured along the wall normal by ray march (min/max/mean '
               'over samples, zoned by x); r_out-r_in reported only as the nominal '
               'construction value. face_dist_cross_slice is the min over ALL '
               'inner/outer face pairs and is a wrong pair between cradle-shifted '
               'slices; face_dist_coaxial is the same-wall gap (0.5 weld and leg/'
               'side-wall material excluded from the wall statistic).')


# ---------------------------------------------------------------------------
# Static preview (flat-shaded painter's algorithm) + reference comparison.
# ---------------------------------------------------------------------------
def tess(shapes):
    out = []
    for rgb, s in shapes:
        v, f = s.tessellate(1.2, 0.5)
        out.append((rgb, np.array([[p.x, p.y, p.z] for p in v]),
                    [list(t) for t in f]))
    return out


def view_basis(e, up_world):
    e = np.array(e, float)
    e /= np.linalg.norm(e)
    forward = -e
    right = np.cross(up_world, forward)
    right /= np.linalg.norm(right)
    up = np.cross(forward, right)
    return e, right, up


def render(models, e, up_world, w, h, bg='#f4f6fa', phantom_alpha=0.22):
    e, r, u = view_basis(e, np.array(up_world, float))
    tris, phantom, allx, ally = [], [], [], []
    for rgb, verts, faces in models:
        sx, sy, dep = verts @ r, verts @ u, verts @ e
        allx.append(sx)
        ally.append(sy)
        for fc in faces:
            pp = np.stack([sx[fc], sy[fc]], 1)
            n = np.cross(verts[fc[1]] - verts[fc[0]], verts[fc[2]] - verts[fc[0]])
            ln = np.linalg.norm(n) or 1.0
            shade = 0.55 + 0.45 * abs(float(n @ np.array([0.3, 0.25, 0.92])) / ln)
            col = tuple(int(c * shade) for c in rgb)
            item = (float(dep[fc].mean()), pp, col)
            (phantom if tuple(rgb) == tuple(PHANTOM_COLOR) else tris).append(item)
    xmin, xmax = min(a.min() for a in allx), max(a.max() for a in allx)
    ymin, ymax = min(a.min() for a in ally), max(a.max() for a in ally)
    cx, cy = 0.5 * (xmin + xmax), 0.5 * (ymin + ymax)
    s = 0.86 * min(w / (xmax - xmin + 1e-9), h / (ymax - ymin + 1e-9))
    im = Image.new('RGB', (w, h), bg)
    draw = ImageDraw.Draw(im)
    for depth, pp, col in sorted(tris, key=lambda t: t[0]):
        draw.polygon([(w / 2 + (px - cx) * s, h / 2 - (py - cy) * s) for px, py in pp],
                     fill=col)
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    for depth, pp, col in sorted(phantom, key=lambda t: t[0]):
        dl.polygon([(w / 2 + (px - cx) * s, h / 2 - (py - cy) * s) for px, py in pp],
                   fill=col + (int(255 * phantom_alpha),))
    return Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB')


VIEWS = [
    ('Side (longitudinal cradle)', (0, 1, 0), (0, 0, 1)),
    ('Back (arcs + leg)', (-1, 0.22, 0.25), (0, 0, 1)),
    ('Top', (0, 0, 1), (0, -1, 0)),
    ('Isometric', (-0.55, 0.72, 0.42), (0, 0, 1)),
]


def four_views(p4, gray, blue, phantom):
    tl = tess([(GREEN_COLOR, p4), (GRAY_COLOR, gray),
               (BLUE_COLOR, blue), (PHANTOM_COLOR, phantom)])
    W, H = 760, 620
    ims = [render(tl, e, up, W, H) for _, e, up in VIEWS]
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
        sf = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    except Exception:
        font = sf = ImageFont.load_default()
    canvas = Image.new('RGB', (W * 2, H * 2), '#ffffff')
    for i, (title, _, _) in enumerate(VIEWS):
        d = ImageDraw.Draw(ims[i])
        d.text((18, 14), title, font=font, fill='#202a36')
        canvas.paste(ims[i], ((i % 2) * W, (i // 2) * H))
    canvas.save(OUT / 'shells_preview_v5.png')

    # comparison: reference drawing next to the two most telling views
    ref_dir = D.parent.parent / 'references' / 'v5'
    badges = ['socket_views_dec.png', 'socket_photo_dec.png']
    refs = [Image.open(ref_dir / b).convert('RGB') for b in badges
            if (ref_dir / b).exists()]
    if refs:
        ch = 620
        cols = [im.resize((int(im.width * ch / im.height), ch)) for im in refs]
        side = ims[0].resize((int(ims[0].width * ch / ims[0].height), ch))
        back = ims[1].resize((int(ims[1].width * ch / ims[1].height), ch))
        total_w = sum(c.width for c in cols) + side.width + back.width + 60
        cmp_im = Image.new('RGB', (total_w, ch + 40), '#ffffff')
        dc = ImageDraw.Draw(cmp_im)
        x = 10
        for c, b in zip(cols, badges):
            cmp_im.paste(c, (x, 34))
            dc.text((x, 8), 'reference ' + b, font=sf, fill='#202a36')
            x += c.width + 10
        for im, lab in [(side, 'model side'), (back, 'model back')]:
            cmp_im.paste(im, (x, 34))
            dc.text((x, 8), lab, font=sf, fill='#202a36')
            x += im.width + 10
        cmp_im.save(OUT / 'shells_comparison_v5.png')


# ---------------------------------------------------------------------------
# Collision helpers.  Only P01 (zmax 46) and P04 (zmax 29) reach the new parts'
# z band (>= z_ref - embed); everything else is below z_ref and cannot touch.
# ---------------------------------------------------------------------------
def transform(solid, t):
    a = math.degrees(t['angle'])
    x, y = t['translation']
    return solid.rotate((0, 0, 0), (0, 0, 1), a).translate((x, y, 0.0))


def _closest_to(parts, other):
    """Closest-point coordinates between each shell and another body, so the
    reported minimum distance is traceable to a location."""
    res = {}
    for name, s in parts.items():
        try:
            d = BRepExtrema_DistShapeShape(s.wrapped, other.wrapped)
            d.Perform()
            p1, p2 = d.PointOnShape1(1), d.PointOnShape2(1)
            res[name] = dict(distance=round(float(d.Value()), 4),
                             on_shell=[round(p1.X(), 2), round(p1.Y(), 2), round(p1.Z(), 2)],
                             on_phantom=[round(p2.X(), 2), round(p2.Y(), 2), round(p2.Z(), 2)])
        except Exception as exc:
            res[name] = dict(error=str(exc))
    return res


def overlap_volume(a, b):
    ba, bb = a.BoundingBox(), b.BoundingBox()
    if any(getattr(ba, k + 'max') < getattr(bb, k + 'min') or
           getattr(bb, k + 'max') < getattr(ba, k + 'min') for k in 'xyz'):
        return 0.0
    common = a.intersect(b)
    return common.Volume() if common.Solids() else 0.0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'parameters': P, 'thickness_target': P['shell_t']}

    p4 = cq.importers.importStep(str(V4PARTS / 'P04_green.step')).val()
    p1 = cq.importers.importStep(str(V4PARTS / 'P01_black.step')).val()
    gray, blue, phantom = build_shells(P)
    parts = {'P10_gray_upper': gray, 'P11_blue_lower': blue}

    report['validity'] = {}
    for name, s in parts.items():
        report['validity'][name] = dict(valid=bool(s.isValid()),
                                        solids=len(s.Solids()),
                                        volume=round(s.Volume(), 3),
                                        faces=len(s.Faces()))

    report['thickness'] = {n: shell_thickness(s, P['shell_t'])
                           for n, s in parts.items()}

    # static (open) intersections -------------------------------------------
    others = {'P0%d' % i: cq.importers.importStep(str(V4PARTS / f)).val()
              for i, f in []}
    others = {}
    for f in sorted(V4PARTS.glob('*.step')):
        others[f.name[:3]] = cq.importers.importStep(str(f)).val()
    checks, intended = [], []
    report['intersections_open'] = {}
    for name, s in parts.items():
        for oname, o in list(others.items()) + [('phantom', phantom),
                                                ('P10_gray_upper', gray),
                                                ('P11_blue_lower', blue)]:
            if oname == name:
                continue
            vol = overlap_volume(s, o)
            report['intersections_open'].setdefault(name, {})[oname] = round(vol, 5)
            if vol <= 1e-3:
                continue
            (intended if oname == 'P04' else checks).append((name, oname, vol))
    report['open_forbidden_count'] = len(checks)
    report['open_forbidden_intersections'] = checks
    report['open_intended_contacts'] = intended
    report['open_collision_count'] = len(checks)   # forbidden only

    report['phalanx_clearance'] = {
        'assumed_phalanx_radius': P['phalanx_r'],
        'nominal_radial_clearance': round(P['r_in'] - P['phalanx_r'], 4),
        'radial_clearance_param': P['clearance'],
        'min_solid_distance_to_phantom': {
            n: round(float(s.distance(phantom)), 4) for n, s in parts.items()},
        'min_distance_location': _closest_to(parts, phantom),
        'note': 'the nominal RADIAL clearance is 2.0 on the circular walls, but the '
                'absolute minimum solid distance is smaller because it is set by the '
                'axial gap between the back leg / side-wall skirts and the proximal '
                'cap of the assumed phantom (x~760), not by the wall radius. The '
                'phantom is an assumed demo body; this gap is reported, not hidden.'}

    # connection to P04 (designed weld) and forbidden set -------------------
    conn = {n: round(float(s.distance(p4)), 4) for n, s in parts.items()}
    report['p04_connection'] = dict(distance=conn, embed=P['embed'],
                                    note='designed weld into P04 top face')

    # 74-pose check ----------------------------------------------------------
    motion = json.loads((V4 / 'motion.json').read_text())
    parts74 = {f.name[:3]: cq.importers.importStep(str(f)).val()
               for f in sorted(V4PARTS.glob('*.step'))}
    worst, frame_hits, weld_hits = {}, [], 0
    for fi, frame in enumerate(motion):
        tr = frame['transforms']
        g = transform(gray, tr['P04'])
        b = transform(blue, tr['P04'])
        ph = transform(phantom, tr['P04'])
        newp = {'P10_gray_upper': g, 'P11_blue_lower': b}
        for name, s in newp.items():
            for oname, o in parts74.items():
                oo = transform(o, tr[oname])
                vol = overlap_volume(s, oo)
                if vol > worst.get((name, oname), (0, -1))[0]:
                    worst[(name, oname)] = (vol, fi)
                if vol <= 1e-3:
                    continue
                if oname == 'P04':          # intended weld, same transform
                    weld_hits += 1
                    continue
                frame_hits.append(dict(frame=fi, part=name, other=oname,
                                       volume=round(vol, 5)))
        for a, b2, tag in [(g, b, 'P10|P11'), (g, ph, 'P10|phalanx'),
                           (b, ph, 'P11|phalanx')]:
            v = overlap_volume(a, b2)
            if v > 1e-3:
                frame_hits.append(dict(frame=fi, pair=tag, volume=round(v, 5)))
    report['poses_checked'] = len(motion)
    report['pose_forbidden_count'] = len(frame_hits)
    report['pose_forbidden_intersections'] = frame_hits[:60]
    report['pose_intended_weld_count'] = weld_hits
    report['pose_collision_count'] = len(frame_hits)   # forbidden only
    report['pose_worst'] = {f'{k[0]}|{k[1]}': dict(volume=round(v[0], 5), frame=v[1])
                            for k, v in worst.items() if v[0] > 1e-6}

    # key poses: open / mid / closed ----------------------------------------
    key = {}
    for lab, fi in [('open', 0), ('mid', len(motion) // 2), ('closed', len(motion) - 1)]:
        fr = motion[fi]['transforms']
        g = transform(gray, fr['P04']); b = transform(blue, fr['P04'])
        ph = transform(phantom, fr['P04'])
        forb = weld = 0
        for name, s in [('P10', g), ('P11', b)]:
            for oname, o in parts74.items():
                if overlap_volume(s, transform(o, fr[oname])) > 1e-3:
                    if oname == 'P04':
                        weld += 1
                    else:
                        forb += 1
        for a, b2 in [(g, b), (g, ph), (b, ph)]:
            if overlap_volume(a, b2) > 1e-3:
                forb += 1
        key[lab] = dict(frame=fi, forbidden=forb, intended_weld=weld)
    report['key_poses'] = key

    # exports ---------------------------------------------------------------
    for name, s in parts.items():
        cq.exporters.export(cq.Workplane(obj=s), str(OUT / f'{name}.step'))
        cq.exporters.export(cq.Workplane(obj=s), str(OUT / f'{name}.stl'))
    cq.exporters.export(cq.Workplane(obj=phantom), str(OUT / 'assumed_phalanx_demo.step'))

    ass = cq.Assembly(name='v5_socket_open')
    ass.add(p4, name='P04_green', color=cq.Color(115 / 255, 184 / 255, 32 / 255))
    ass.add(gray, name='P10_gray_upper', color=cq.Color(150 / 255, 152 / 255, 157 / 255))
    ass.add(blue, name='P11_blue_lower', color=cq.Color(60 / 255, 110 / 255, 190 / 255))
    ass.save(str(OUT / 'assembly_v5_open.step'))

    four_views(p4, gray, blue, phantom)

    (OUT / 'shells_parameters.json').write_text(json.dumps({'assumptions': {
        'note': 'Parametric demonstration only. V4 scale is conventional; physical '
                'mm are not established and wearability is not claimed.',
        'thickness': '1.5 (issue #7 value, applied along the surface normal)',
        'phalanx': 'assumed circular stump, radius %.1f, clearance %.1f'
                   % (P['phalanx_r'], P['clearance']),
        'socket_axis': 'along +X at y=%.1f, z=%.1f (finger centre line)'
                       % (P['y_center'], P['z_axis']),
        'free_end': '+X, cradle raised by %.1f at the free end' % P['rise'],
        'mount': 'sits on the P04 top face (z=%.1f), %.1f weld embed'
                 % (P['z_ref'], P['embed']),
    }, 'parameters': P}, indent=2))
    (OUT / 'shells_report.json').write_text(json.dumps(report, indent=2))

    print('validity:', report['validity'])
    print('thickness:', {k: (v.get('measured_min'), v.get('measured_max'),
                              v.get('face_dist_coaxial'), v.get('face_dist_cross_slice'))
                         for k, v in report['thickness'].items()})
    print('open forbidden:', report['open_forbidden_count'],
          'intended P04 welds:', len(report['open_intended_contacts']))
    print('key poses:', report['key_poses'])
    print('pose forbidden:', report['pose_forbidden_count'],
          '/', report['poses_checked'], 'poses;',
          'intended welds:', report['pose_intended_weld_count'])
    if report['pose_worst']:
        print('pose worst:', report['pose_worst'])


if __name__ == '__main__':
    main()
