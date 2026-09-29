import numpy as np

UPPER = np.array([[310,189],[336,190],[361,190],[386,190]], dtype=float)
LOWER = np.array([[309,243],[334,243],[359,244],[384,244]], dtype=float)

def fit_row(points):
    k = np.arange(len(points), dtype=float)
    centered = points - points.mean(axis=0)
    _, _, vt = np.linalg.svd(centered)
    axis = vt[0]
    s = centered @ axis
    if np.corrcoef(s, k)[0,1] < 0:
        axis = -axis
        s = -s
    pitch, offset = np.polyfit(k, s, 1)
    residual = s - (pitch*k + offset)
    rms = float(np.sqrt(np.mean(residual**2)))
    return float(pitch), axis, rms

if __name__ == "__main__":
    pu, au, ru = fit_row(UPPER)
    pl, al, rl = fit_row(LOWER)
    pm = 0.5*(pu+pl)
    row_sep = np.linalg.norm(UPPER.mean(axis=0)-LOWER.mean(axis=0))
    print(f"upper pitch: {pu:.4f} px; RMS {ru:.4f} px")
    print(f"lower pitch: {pl:.4f} px; RMS {rl:.4f} px")
    print(f"mean pitch:  {pm:.4f} px")
    print(f"row separation: {row_sep:.4f} px = {row_sep/pm:.4f} pitch")
