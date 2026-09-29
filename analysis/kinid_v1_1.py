"""KIN-ID v1.1 cross-state invariance audit.

This script documents the manual landmark test performed on the two side-view
photographs. Coordinates are image-space observations, not manufacturing data.
"""

import numpy as np

P_EXT = np.array([
    [258,159],
    [231,149],
    [198,141],
    [204,162],
], dtype=float)

P_FLX = np.array([
    [330,296],
    [309,282],
    [279,279],
    [290,303],
], dtype=float)

def pairwise(P):
    out = {}
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            out[f"R{i}-R{j}"] = np.linalg.norm(P[j]-P[i])
    return out

def normalized_comparison(P1, P2, datum="R0-R1"):
    d1, d2 = pairwise(P1), pairwise(P2)
    b1, b2 = d1[datum], d2[datum]
    result = {}
    for key in d1:
        n1, n2 = d1[key]/b1, d2[key]/b2
        m = 0.5*(n1+n2)
        disagreement = abs(n1-n2)/m*100 if m else 0
        result[key] = (n1, n2, disagreement)
    return result

if __name__ == "__main__":
    for key, vals in normalized_comparison(P_EXT, P_FLX).items():
        print(key, vals)
