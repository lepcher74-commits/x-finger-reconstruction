"""KIN-ID v0.9: preliminary promotional-video motion audit.

This script intentionally keeps the 150–155 s picks as LOW-CONFIDENCE.
The frames contain overlapping fingers and partially occluded pivot centres.
The purpose of this stage is to establish the motion-envelope workflow,
not to declare production linkage dimensions.
"""

import numpy as np
import pandas as pd

POINTS = {
    150: np.array([[245,147],[305,140],[350,128],[410,130]], float),
    152: np.array([[245,145],[315,145],[365,127],[425,128]], float),
    154: np.array([[215,130],[275,162],[330,218],[405,270]], float),
    155: np.array([[210,130],[275,165],[310,205],[340,270]], float),
}

def signed_angle_deg(v):
    return np.degrees(np.arctan2(v[1], v[0]))

def pose_metrics(p):
    seg = [p[i+1]-p[i] for i in range(3)]
    a = [signed_angle_deg(v) for v in seg]
    j1 = ((a[1]-a[0]+180)%360)-180
    j2 = ((a[2]-a[1]+180)%360)-180
    return {
        "prox_segment_px": np.linalg.norm(seg[0]),
        "middle_segment_px": np.linalg.norm(seg[1]),
        "distal_segment_px": np.linalg.norm(seg[2]),
        "relative_joint_1_deg": j1,
        "relative_joint_2_deg": j2,
    }

if __name__ == "__main__":
    rows = []
    for t,p in POINTS.items():
        row = {"frame_s": t, **pose_metrics(p),
               "confidence": "LOW - manual/occluded"}
        rows.append(row)
    print(pd.DataFrame(rows).to_string(index=False))
