"""KIN-ID v1.3 — mirrored-view primary-stage registration.

Project reconstruction utility.
Coordinates are manual image measurements from project-supplied media.
They are normalized engineering-identification data, not production dimensions.
"""

import numpy as np

TOP = np.array([[430,58],[445,68],[606,100],[630,130]], dtype=float)
BOTTOM = np.array([[570,330],[555,342],[397,369],[370,400]], dtype=float)

def similarity_fit(X, Y):
    mx = X.mean(axis=0)
    my = Y.mean(axis=0)
    Xc = X - mx
    Yc = Y - my
    U, S, Vt = np.linalg.svd(Xc.T @ Yc)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    scale = np.sum(S) / np.sum(Xc**2)
    t = my - scale * (mx @ R)
    fit = scale * (X @ R) + t
    residual = np.linalg.norm(fit - Y, axis=1)
    return fit, residual, scale

if __name__ == "__main__":
    bottom_mirror = BOTTOM.copy()
    bottom_mirror[:,0] *= -1
    _, residual, scale = similarity_fit(bottom_mirror, TOP)
    print("RMS [px]:", np.sqrt(np.mean(residual**2)))
    print("scale:", scale)
