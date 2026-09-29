"""KIN-ID v0.7 — multi-frame linkage identification scaffold.

This script is intentionally source-data agnostic.
It fits one constant mechanism to multiple digitized image/video frames,
while allowing an independent 2D similarity transform per frame.

All manufacturing use requires replacing ESTIMATED seed values with
IDENTIFIED / CONFIRMED dimensions.
"""

from dataclasses import dataclass
import numpy as np
from scipy.optimize import least_squares


@dataclass
class FrameObservation:
    # point labels must match model point labels
    points_px: dict
    weights: dict | None = None


def rot(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s], [s, c]])


def similarity_residual(model_xy, obs_xy, w=None):
    """Best-fit 2D similarity transform residual using Procrustes registration."""
    labels = [k for k in model_xy if k in obs_xy]
    X = np.array([model_xy[k] for k in labels], dtype=float)
    Y = np.array([obs_xy[k] for k in labels], dtype=float)

    Xc = X - X.mean(axis=0)
    Yc = Y - Y.mean(axis=0)

    U, S, Vt = np.linalg.svd(Xc.T @ Yc)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt

    denom = (Xc * Xc).sum()
    scale = S.sum() / max(denom, 1e-12)
    t = Y.mean(axis=0) - scale * X.mean(axis=0) @ R
    Yhat = scale * X @ R + t
    e = Yhat - Y

    if w:
        ww = np.array([w.get(k, 1.0) for k in labels])[:, None]
        e = e * ww

    return e.ravel()


def primary_model(alpha, p):
    """Corrected moving-base primary topology.

    p = [oa_x, oa_y, ob_x, ob_y, lac, lbd, lcd, beta_c]
    alpha = rotating input-bracket angle
    """
    oa = np.array(p[0:2])
    ob = np.array(p[2:4])
    lac, lbd, lcd, beta_c = p[4:8]

    A = rot(alpha) @ oa
    B = rot(alpha) @ ob

    # C is parameterized from A.
    C = A + lac * np.array([np.cos(beta_c), np.sin(beta_c)])

    # D is intersection of circle(B,lbd) and circle(C,lcd).
    v = C - B
    d = np.linalg.norm(v)
    if d < 1e-9:
        raise ValueError("degenerate geometry")

    a = (lbd*lbd - lcd*lcd + d*d) / (2*d)
    h2 = lbd*lbd - a*a
    if h2 < 0:
        h = 0.0
    else:
        h = np.sqrt(h2)

    P = B + a * v / d
    n = np.array([-v[1], v[0]]) / d
    D1, D2 = P + h*n, P - h*n
    D = D1 if D1[1] < D2[1] else D2

    return {"O": np.zeros(2), "A": A, "B": B, "C": C, "D": D}


def objective(x, frames):
    """Example objective layout.

    x:
      p[0:8]      constant mechanism geometry
      alphas[...] one input angle per frame
    """
    p = x[:8]
    alphas = x[8:8+len(frames)]
    res = []

    for alpha, frame in zip(alphas, frames):
        model = primary_model(alpha, p)
        res.extend(similarity_residual(model, frame.points_px, frame.weights))

    # Soft near-parallelogram regularizer, deliberately weak.
    oa, ob = np.array(p[0:2]), np.array(p[2:4])
    ab = np.linalg.norm(oa-ob)
    lac, lbd, lcd = p[4], p[5], p[6]
    res.extend([
        0.02*(lac-lbd),
        0.02*(ab-lcd),
    ])
    return np.asarray(res)


def fit(frames, x0):
    return least_squares(objective, x0, args=(frames,), loss="soft_l1")


if __name__ == "__main__":
    print("KIN-ID v0.7 scaffold. Add digitized frame observations before fitting.")
