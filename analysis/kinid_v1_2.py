"""KIN-ID v1.2

Interpret the v1.1 invariant landmark triangle as a rigid Pivot Block / phalange
subassembly and keep ambiguous patent-axis assignments explicit.

No manufacturing dimensions are produced in this script.
"""

CANDIDATE_MAPPING = {
    "R0": {"mapping": "11 or 13b", "confidence": "HIGH"},
    "R1": {"mapping": "13b or 11", "confidence": "HIGH"},
    "R2": {"mapping": "22/25 structural fastener region", "confidence": "MEDIUM-HIGH"},
    "R3": {"mapping": "moving drive/stirrup pivot candidate", "confidence": "LOW-MEDIUM"},
}

RIGID_SUBASSEMBLY = ("R0", "R1", "R2")
REJECTED_FROM_RIGID_SUBASSEMBLY = ("R3",)

if __name__ == "__main__":
    for k, v in CANDIDATE_MAPPING.items():
        print(k, v)
