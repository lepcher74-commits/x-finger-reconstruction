"""Objective measurement of the issue #7 reference drawings.

IMPORTANT LIMITATION (recorded in STATUS.md): the model driving this run has
NO image input, so the drawings cannot be *visually* read.  The four views and
their text labels therefore cannot be identified by looking at the picture.
This script only measures objective pixel data (colour-region extents) and
compares them with the CAD dimensions of the green part P04.  It does NOT
assign a semantic name (front/top/side) to a view and does NOT invent
dimensions from the picture.

Inputs : references/socket_views.png, references/socket_photo.png
         (may be either raw PNG or base64 text -> auto-decoded)
Outputs: reference_measurements.json
         views_detected.png (view boxes drawn for a human reviewer)
"""
from pathlib import Path
import base64, json, io
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REFS = HERE / 'references'
OUT = HERE


def load_png(path):
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return Image.open(io.BytesIO(data)).convert('RGB')
    txt = data.strip()
    if txt.startswith(b'data:image'):
        txt = txt.split(b',', 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(txt))).convert('RGB')


def color_masks(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    green = (g > r + 25) & (g > b + 25)
    blue = (b > r + 35) & (b > g + 5)
    side = (np.abs(r - g) < 25) & (np.abs(g - b) < 25) & (np.abs(r - b) < 25)
    bg = side & (r > 195)
    dark = side & (r > 40) & (r <= 175)
    return dict(green=green, blue=blue, darkgray=dark, background=bg)


def kmeans_views(pts, k=4, iters=60, seed=0):
    rng = np.random.default_rng(seed)
    c = pts[rng.choice(len(pts), k, replace=False)].astype(float)
    for _ in range(iters):
        d = ((pts[:, None, :] - c[None, :, :]) ** 2).sum(2)
        lab = d.argmin(1)
        for j in range(k):
            if (lab == j).any():
                c[j] = pts[lab == j].mean(0)
    return lab, c


def bbox(xs, ys):
    return dict(x=[int(xs.min()), int(xs.max())], y=[int(ys.min()), int(ys.max())],
                w=int(xs.max() - xs.min() + 1), h=int(ys.max() - ys.min() + 1))


def large_components(mask, min_pixels=350):
    """Keep only connected dark/gray regions large enough to be the shell
    (drops the text labels and thin outlines)."""
    from scipy import ndimage
    lbl, n = ndimage.label(mask, structure=np.ones((3, 3)))
    keep = np.zeros_like(mask)
    for i in range(1, n + 1):
        sel = lbl == i
        if sel.sum() >= min_pixels:
            keep |= sel
    return keep


# Fixed view cells, derived from the detected content bounding boxes in
# socket_views.png (top-left, mid-left, mid-right, bottom-left).  The right
# column of rows 1 and 3 is empty except labels.  Labels are stripped by the
# large-component filter.  These cells are geometric, NOT semantic: the script
# does not know which view is front/top/side because it cannot read the image.
VIEW_CELLS = {
    1: (40, 265, 55, 235),
    2: (40, 265, 240, 420),
    3: (280, 465, 250, 430),
    4: (40, 265, 425, 575),
}


def measure(path):
    im = load_png(path)
    a = np.array(im)
    m = color_masks(a)
    m['darkgray'] = large_components(m['darkgray'])
    views = []
    for idx, (x0, x1, y0, y1) in VIEW_CELLS.items():
        cell = (slice(y0, y1), slice(x0, x1))
        v = dict(view_index=idx, cell_xyxy=[x0, y0, x1, y1])
        for name in ('green', 'blue', 'darkgray'):
            mm = m[name][cell]
            vy, vx = np.where(mm)
            if len(vx) > 20:
                v[name] = bbox(vx + x0, vy + y0) | dict(pixels=int(mm.sum()))
            else:
                v[name] = None
        views.append(v)
    im2 = im.copy()
    dr = ImageDraw.Draw(im2)
    for idx, (x0, x1, y0, y1) in VIEW_CELLS.items():
        dr.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=2)
        dr.text((x0 + 2, y0 + 2), f"view {idx}", fill=(255, 0, 0))
    im2.save(OUT / (path.stem + '_views_detected.png'))
    return dict(image=path.name, size=[int(im.size[0]), int(im.size[1])], views=views)


def main():
    results = {p.name: measure(p) for p in sorted(REFS.glob('*.png'))}
    json.dump(results, open(OUT / 'reference_measurements.json', 'w'), indent=2)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
