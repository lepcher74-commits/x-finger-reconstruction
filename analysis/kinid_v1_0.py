"""KIN-ID v1.0
Reproducible consistency test for the five-landmark distal geometry.

The source coordinates below are manual center picks from two mirrored views
of one supplied CAD render. The script reports normalized segment ratios and
a similarity-registration residual.

No absolute scale is inferred.
"""
import numpy as np

TOP = np.array([
    [602., 95.],
    [702., 88.],
    [735.,106.],
    [778.,119.],
    [844.,125.],
])

BOTTOM = np.array([
    [399.,367.],
    [298.,363.],
    [265.,378.],
    [226.,392.],
    [157.,397.],
])

def segment_lengths(P):
    return np.linalg.norm(np.diff(P, axis=0), axis=1)

def similarity_fit(X, Y):
    mx, my = X.mean(0), Y.mean(0)
    Xc, Yc = X-mx, Y-my
    U, S, Vt = np.linalg.svd(Xc.T @ Yc)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    scale = S.sum() / np.sum(Xc**2)
    t = my - scale*(mx @ R)
    fit = scale*(X @ R) + t
    rms = np.sqrt(np.mean(np.sum((fit-Y)**2, axis=1)))
    return scale, R, t, fit, rms

lt = segment_lengths(TOP)
lb = segment_lengths(BOTTOM)

mirrored = BOTTOM.copy()
mirrored[:,0] *= -1

_, _, _, _, rms = similarity_fit(mirrored, TOP)

rt = lt/lt[0]
rb = lb/lb[0]
mean = (rt+rb)/2

print("RMS [px]:", rms)
for i, v in enumerate(mean):
    print(f"P{i}-P{i+1}: {v:.6f}")
