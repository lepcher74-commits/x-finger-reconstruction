#!/usr/bin/env python3
"""Stage 2: 74-pose verification of the reproduced V4 candidate assembly.

Uses the Stage-1 reproduction (validation/work/reproduction) as the candidate
geometry: P07/P04 reproduce the red-contour change, the other seven parts are
byte-identical to the accepted V3 baseline.

Runs the delivered V4 scripts in an isolated candidate directory and then
recomputes, independently of the delivered JSON reports:

  * body-body interference over all 74 poses (36 pairs each),
  * pin-body interference over all 74 poses,
  * coaxial error of the eight joint axes over all 74 poses,
  * rigid gray<->dark-blue link (constant relative transform + two shared axes),
  * gray containment inside the yellow housing over all 74 poses,
  * whether the P04 green-seat cut is necessary (V3 seat vs new P07 tongue) and
    whether the candidate cut removes exactly that interference,
  * preservation of the untouched parts, shared pink/dark-blue layer, yellow
    placement and the full black housing.

Artifacts (GIF, autonomous HTML viewer, STEP assemblies, previews) are copied
to validation/ for the workflow to upload. Report is written incrementally.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

import cadquery as cq
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PKG = ROOT / "handoff" / "current_assembly"
V3 = PKG / "assembly_3d_v3"
V4 = PKG / "assembly_3d_v4"
PARTS_2D = PKG / "parts_2d_v1"
STAGE1_WORK = HERE / "work" / "reproduction"
WORK = HERE / "work" / "stage2"
CAND = WORK / "assembly"
REPORT = HERE / "stage2_report.json"
STDOUT_DIR = HERE / "stage2_stdout"

BODY_COLLISION_TOL = 1e-3
PIN_COLLISION_TOL = 0.01
COAX_TOL = 1e-6
RIGID_TOL = 1e-9
CONTAIN_TOL = 1e-6
INTERFERENCE_TOL = 1e-3

PACKAGES = ["cadquery", "cadquery-ocp", "numpy", "scipy", "shapely", "pillow"]

# Joint pairs shared by the kinematic solver (present.py / kinematics).
PAIRS = [("P01", 0, "P02", 0), ("P02", 1, "P03", 0), ("P03", 1, "P05", 0),
         ("P05", 1, "P01", 2), ("P01", 1, "P04", 0), ("P06", 0, "P09", 0),
         ("P07", 0, "P08", 0), ("P07", 1, "P08", 1)]
PIN_RADIUS = 4.8

REPORT_DATA = {
    "stage": 2,
    "title": "Проверка сборки V4 в 74 положениях: тела, оси, штифты, "
             "серая внутри жёлтой, жёсткая связь с P07, необходимость выреза P04",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "кандидат = воспроизведение этапа 1 (P07/P04 по красному контуру, "
             "остальные 7 деталей = V3); ручная проверка пакета, без изготовления",
    "commands": [
        "tar -xzf handoff/current_assembly.tar.gz",
        "pip install -r validation/requirements.txt",
        "python3 validation/stage1_reproduce_red_contour.py",
        "python3 validation/stage2_verify_assembly.py",
    ],
    "environment": {},
    "stages": {},
    "checks": {},
    "passed": None,
}


def save() -> None:
    REPORT.write_text(json.dumps(REPORT_DATA, indent=2, ensure_ascii=False))


def environment() -> dict:
    env = {"python": sys.version.split()[0], "platform": platform.platform(),
           "executable": sys.executable}
    for name in PACKAGES + ["matplotlib"]:
        try:
            env[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            env[name] = None
    return env


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_step(path: Path):
    return cq.importers.importStep(str(path)).val()


def move(shape, transform, degrees=True):
    angle = transform["angle"]
    if degrees:
        angle = math.degrees(angle)
    x, y = transform["translation"]
    return shape.rotate((0, 0, 0), (0, 0, 1), angle).translate((x, y, 0))


def transform_matrix(f, part_id):
    t = f["transforms"][part_id]
    a = t["angle"]
    c, s = math.cos(a), math.sin(a)
    x, y = t["translation"]
    return np.array([[c, -s, x], [s, c, y], [0.0, 0.0, 1.0]])


def setup_candidate() -> dict:
    if not (STAGE1_WORK / "parts").is_dir():
        raise RuntimeError(
            f"нет готового воспроизведения этапа 1: {STAGE1_WORK}. "
            "Сначала выполните python3 validation/stage1_reproduce_red_contour.py")
    if WORK.exists():
        shutil.rmtree(WORK)
    (CAND / "parts").mkdir(parents=True)
    copied = []
    for part in sorted((STAGE1_WORK / "parts").glob("*.step")):
        shutil.copy2(part, CAND / "parts" / part.name)
        copied.append(part.name)
    for name in ("motion.json", "assembly_parameters.json"):
        shutil.copy2(STAGE1_WORK / name, CAND / name)
    scripts = []
    for name in ("verify_assembly.py", "check_pins.py", "present.py",
                 "make_viewer.py", "contour_preview.py", "red_contour.py"):
        src = V4 / name
        if src.exists():
            shutil.copy2(src, CAND / name)
            scripts.append(name)
    extra = ["contour_reference.png", "contour_change.json"]
    for name in extra:
        src = STAGE1_WORK / name if (STAGE1_WORK / name).exists() else V4 / name
        if src.exists():
            shutil.copy2(src, CAND / name)
    # present.py reads <parent>/parts_2d_v1/geometry.json
    (WORK / "parts_2d_v1").mkdir(parents=True)
    shutil.copy2(PARTS_2D / "geometry.json", WORK / "parts_2d_v1" / "geometry.json")
    return {"copied_parts": copied, "scripts": scripts,
            "parts_2d_v1": str((WORK / "parts_2d_v1" / "geometry.json").relative_to(ROOT))}


def run_script(name: str, timeout: int) -> dict:
    started = time.time()
    proc = subprocess.run([sys.executable, name], cwd=CAND,
                          capture_output=True, text=True, timeout=timeout)
    elapsed = time.time() - started
    out = (proc.stdout or "") + (proc.stderr or "")
    (STDOUT_DIR / f"{name}.stdout.txt").parent.mkdir(parents=True, exist_ok=True)
    (STDOUT_DIR / f"{name}.stdout.txt").write_text(out)
    return {"command": f"{sys.executable} {name}", "cwd": str(CAND.relative_to(ROOT)),
            "returncode": proc.returncode, "seconds": round(elapsed, 3),
            "stdout_tail": out.strip().splitlines()[-6:], "ok": proc.returncode == 0}


def holes_data() -> dict:
    data = json.loads((PARTS_2D / "geometry.json").read_text())
    return {p["id"]: np.array([h["center"] for h in p["holes"]]) @ np.array(p["R"]) + np.array(p["t"])
            for p in data["parts"]}


def merged_holes() -> dict:
    holes = holes_data()
    for a, i, b, j in PAIRS:
        holes[a][i] = holes[b][j] = (holes[a][i] + holes[b][j]) / 2
    return holes


def build_pins(holes: dict) -> dict:
    pins = {}
    for k, (a, i, b, j) in enumerate(PAIRS):
        x, y = holes[a][i] * [1, -1]
        z0, z1 = (-47, 47) if k < 5 else ((-77, -34) if k == 5 else (-77, -41))
        if k == 2:
            z0, z1 = (-29.4, 29.4)
        pins["J" + str(k + 1)] = {
            "parent": a, "radius": PIN_RADIUS,
            "solid": cq.Solid.makeCylinder(PIN_RADIUS, z1 - z0, cq.Vector(x, y, z0)),
        }
    return pins


def main() -> int:
    REPORT_DATA["environment"] = environment()
    save()
    if not V3.is_dir() or not V4.is_dir():
        REPORT_DATA["stages"]["setup"] = {
            "ok": False,
            "error": f"нет распакованного пакета {PKG}: tar -xzf handoff/current_assembly.tar.gz"}
        REPORT_DATA["passed"] = False
        save()
        print(REPORT_DATA["stages"]["setup"]["error"], file=sys.stderr)
        return 2

    STDOUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DATA["stages"]["setup"] = setup_candidate()
    REPORT_DATA["stages"]["setup"]["ok"] = True
    save()

    motion = json.loads((CAND / "motion.json").read_text())
    frames = len(motion)
    REPORT_DATA["stages"]["motion"] = {"frames": frames,
                                       "body_deg_end": motion[-1]["body_deg"],
                                       "tip_deg_end": motion[-1]["tip_deg"]}
    save()

    bodies = {p.name[:3]: load_step(p) for p in sorted((CAND / "parts").glob("*.step"))}
    holes = merged_holes()
    pins = build_pins(holes)

    # ---- Delivered scripts (isolated copy of the candidate) ----
    run_reports = {}
    for name, timeout in [("verify_assembly.py", 900), ("present.py", 900),
                          ("check_pins.py", 1200), ("make_viewer.py", 120),
                          ("contour_preview.py", 300)]:
        try:
            run_reports[name] = run_script(name, timeout)
        except subprocess.TimeoutExpired:
            run_reports[name] = {"command": f"{sys.executable} {name}", "ok": False,
                                 "returncode": None, "error": "timeout"}
        REPORT_DATA["stages"][name] = run_reports[name]
        save()

    checks = REPORT_DATA["checks"]

    # ---- 1. Body-body interference over 74 poses ----
    body_collisions = []
    max_overlap = 0.0
    worst = None
    keys = sorted(bodies)
    for idx, f in enumerate(motion):
        posed = {k: move(bodies[k], f["transforms"][k]) for k in keys}
        boxes = {k: posed[k].BoundingBox() for k in keys}
        for a, b in ((a, b) for i, a in enumerate(keys) for b in keys[i + 1:]):
            aa, bb = boxes[a], boxes[b]
            if any(getattr(aa, k + "max") < getattr(bb, k + "min")
                   or getattr(bb, k + "max") < getattr(aa, k + "min") for k in "xyz"):
                continue
            common = posed[a].intersect(posed[b])
            vol = float(common.Volume()) if common.Solids() else 0.0
            if vol > max_overlap:
                max_overlap, worst = vol, [idx, a, b]
            if vol > BODY_COLLISION_TOL:
                body_collisions.append({"frame": idx, "pair": [a, b], "volume": vol})
        if idx % 10 == 0:
            print("bodies", idx, "collisions", len(body_collisions), "max", max_overlap, flush=True)
    delivered_body = None
    delivered_coll = CAND / "collision_checks.json"
    if delivered_coll.exists():
        delivered_body = json.loads(delivered_coll.read_text())
    checks["body_collisions"] = {
        "ok": not body_collisions,
        "frames": frames,
        "pairs_per_frame": len(keys) * (len(keys) - 1) // 2,
        "threshold": BODY_COLLISION_TOL,
        "collisions": body_collisions,
        "max_overlap": max_overlap,
        "worst": worst,
        "delivered_script_collisions": delivered_body.get("collisions") if delivered_body else None,
        "agrees_with_delivered": (delivered_body is not None
                                  and delivered_body.get("collisions") == body_collisions),
    }
    save()

    # ---- 2. Pin-body interference over 74 poses ----
    pin_collisions = []
    for idx, f in enumerate(motion):
        posed_bodies = {k: move(bodies[k], f["transforms"][k]) for k in keys}
        boxes = {k: posed_bodies[k].BoundingBox() for k in keys}
        for jid, pin in pins.items():
            posed_pin = move(pin["solid"], f["transforms"][pin["parent"]])
            pa = posed_pin.BoundingBox()
            for k in keys:
                b = boxes[k]
                if any(getattr(pa, ax + "max") < getattr(b, ax + "min")
                       or getattr(b, ax + "max") < getattr(pa, ax + "min") for ax in "xyz"):
                    continue
                common = posed_pin.intersect(posed_bodies[k])
                vol = float(common.Volume()) if common.Solids() else 0.0
                if vol > PIN_COLLISION_TOL:
                    pin_collisions.append({"frame": idx, "pair": [jid, k], "volume": vol})
        if idx % 15 == 0:
            print("pins", idx, "collisions", len(pin_collisions), flush=True)
    delivered_pin = None
    if (CAND / "pin_checks.json").exists():
        delivered_pin = json.loads((CAND / "pin_checks.json").read_text())
    checks["pin_collisions"] = {
        "ok": not pin_collisions,
        "frames": frames,
        "pin_radius": PIN_RADIUS,
        "collisions": pin_collisions,
        "delivered_script_collisions": delivered_pin.get("collisions") if delivered_pin else None,
    }
    save()

    # ---- 3. Coaxial error of eight joints over 74 poses ----
    def hole_pos(f, part_id, k):
        t = f["transforms"][part_id]
        q = t["angle"]
        R = np.array([[math.cos(q), -math.sin(q)], [math.sin(q), math.cos(q)]])
        return (holes[part_id][k] * [1, -1]) @ R.T + np.array(t["translation"])

    max_coax = 0.0
    worst_coax = None
    for idx, f in enumerate(motion):
        for a, i, b, j in PAIRS:
            err = float(np.linalg.norm(hole_pos(f, a, i) - hole_pos(f, b, j)))
            if err > max_coax:
                max_coax, worst_coax = err, [idx, a, b]
    checks["coaxial"] = {"ok": max_coax <= COAX_TOL, "frames": frames,
                         "max_coaxial_error": max_coax, "worst": worst_coax,
                         "tol": COAX_TOL, "pairs": [list(p) for p in PAIRS]}
    save()

    # ---- 4. Gray rigid connection to dark-blue ----
    rel0 = np.linalg.inv(transform_matrix(motion[0], "P07")) @ transform_matrix(motion[0], "P08")
    max_rel = 0.0
    for f in motion:
        rel = np.linalg.inv(transform_matrix(f, "P07")) @ transform_matrix(f, "P08")
        max_rel = max(max_rel, float(np.abs(rel - rel0).max()))
    checks["gray_darkblue_rigid"] = {
        "ok": max_rel <= RIGID_TOL,
        "max_relative_transform_drift": max_rel,
        "tol": RIGID_TOL,
        "shared_pins": ["J7", "J8"],
        "pin_radius": PIN_RADIUS, "hole_radius": 5.3,
        "note": "две общие оси J7/J8 и постоянная относительная матрица P07->P08",
    }
    save()

    # ---- 5. Gray containment inside yellow over 74 poses ----
    contain = []
    max_protrusion = 0.0
    min_margin = None
    for idx, f in enumerate(motion):
        gy = move(bodies["P08"], f["transforms"]["P08"])
        ye = move(bodies["P09"], f["transforms"]["P09"])
        gb, yb = gy.BoundingBox(), ye.BoundingBox()
        # negative number = gray is inside the yellow envelope by that margin
        margins = [gb.xmin - yb.xmin, yb.xmax - gb.xmax,
                   gb.ymin - yb.ymin, yb.ymax - gb.ymax,
                   gb.zmin - yb.zmin, yb.zmax - gb.zmax]
        worst_margin = min(margins)
        min_margin = worst_margin if min_margin is None else min(min_margin, worst_margin)
        max_protrusion = max(max_protrusion, -worst_margin)
        inter = gy.intersect(ye)
        vol = float(inter.Volume()) if inter.Solids() else 0.0
        if worst_margin < -CONTAIN_TOL or vol > BODY_COLLISION_TOL:
            contain.append({"frame": idx, "worst_margin": worst_margin,
                            "intersection_volume": vol})
    checks["gray_in_yellow"] = {
        "ok": not contain and max_protrusion <= CONTAIN_TOL,
        "frames": frames,
        "method": "габаритная проверка (bounding box серой внутри bounding box жёлтой по всем осях) + отсутствие пересечения тел; это не строгая проверка внутреннего контура или полости жёлтой",
        "max_protrusion_beyond_envelope": max_protrusion,
        "min_clearance_margin": min_margin,
        "violations": contain,
    }
    save()

    # ---- 6. P04 cut necessity ----
    v3_p04 = load_step(V3 / "parts" / "P04_green.step")
    v3_p07 = load_step(V3 / "parts" / "P07_dark_blue.step")
    new_p07 = bodies["P07"]
    cand_p04 = bodies["P04"]

    removed = v3_p04.cut(cand_p04)
    removed_vol = float(removed.Volume()) if removed.Solids() else 0.0
    removed_box = removed.BoundingBox() if removed.Solids() else None

    interf_per_pose = []
    max_interf = 0.0
    interf_box = None
    interf_solids = 0
    interf_box_pose0 = None
    for idx, f in enumerate(motion):
        p04 = move(v3_p04, f["transforms"]["P04"])
        p07 = move(new_p07, f["transforms"]["P07"])
        common = p04.intersect(p07)
        vol = float(common.Volume()) if common.Solids() else 0.0
        interf_per_pose.append(vol)
        if idx == 0 and common.Solids():
            bb = common.BoundingBox()
            interf_box_pose0 = [bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]
        if vol > max_interf:
            max_interf = vol
            interf_solids = len(common.Solids())
            bb = common.BoundingBox()
            interf_box = [bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]

    cand_interf = 0.0
    for f in motion:
        p04 = move(cand_p04, f["transforms"]["P04"])
        p07 = move(new_p07, f["transforms"]["P07"])
        common = p04.intersect(p07)
        cand_interf = max(cand_interf,
                          float(common.Volume()) if common.Solids() else 0.0)

    old_interf = 0.0
    for f in motion:
        common = move(v3_p04, f["transforms"]["P04"]).intersect(
            move(v3_p07, f["transforms"]["P07"]))
        old_interf = max(old_interf, float(common.Volume()) if common.Solids() else 0.0)

    vol_match = abs(removed_vol - max_interf) / max(max_interf, 1e-12)
    removed_box_list = ([removed_box.xmin, removed_box.xmax, removed_box.ymin,
                         removed_box.ymax, removed_box.zmin, removed_box.zmax]
                        if removed_box else None)
    box_match = (removed_box_list is not None and interf_box_pose0 is not None
                 and max(abs(a - b) for a, b in zip(removed_box_list, interf_box_pose0)) <= 1e-3)
    necessary = max_interf > INTERFERENCE_TOL
    sufficient = cand_interf <= INTERFERENCE_TOL
    minimal = vol_match <= 1e-3
    checks["p04_cut_necessity"] = {
        "ok": bool(necessary and sufficient and minimal and box_match
                   and old_interf <= INTERFERENCE_TOL),
        "necessary": bool(necessary),
        "sufficient_in_candidate": bool(sufficient),
        "minimal": bool(minimal),
        "v3_p04_vs_new_p07_max_interference_volume": max_interf,
        "v3_p04_vs_new_p07_interference_bbox_max_pose": interf_box,
        "v3_p04_vs_new_p07_interference_bbox_pose0": interf_box_pose0,
        "v3_p04_vs_new_p07_interference_solids": interf_solids,
        "candidate_p04_vs_new_p07_max_interference_volume": cand_interf,
        "v3_p04_vs_v3_p07_max_interference_volume": old_interf,
        "removed_material_volume_v3_minus_candidate": removed_vol,
        "removed_material_bbox": removed_box_list,
        "removed_vs_interference_rel_diff": vol_match,
        "removed_bbox_matches_interference": box_match,
        "interference_per_pose": interf_per_pose,
        "conclusion": ("вырез P04 необходим: новый язык P07 пересекает посадочное "
                       "место V3; кандидат удаляет ровно этот объём и после выреза "
                       "пересечения нет"),
    }
    save()

    # ---- 7. Preservation checks ----
    changed = {"P04_green.step", "P07_dark_blue.step"}
    console_parts = {}
    for part in sorted((V3 / "parts").glob("*.step")):
        if part.name in changed:
            continue
        console_parts[part.name] = {
            "identical_to_v3": sha256(part) == sha256(CAND / "parts" / part.name)}
    black = bodies["P01"]
    bb = black.BoundingBox()
    black_ok = (console_parts["P01_black.step"]["identical_to_v3"]
                and black.isValid() and len(black.Solids()) == 1)
    # shared pink/dark-blue layer: overlapping Z bands
    p06_box = bodies["P06"].BoundingBox()
    p07_box = bodies["P07"].BoundingBox()
    layer_overlap = (min(p06_box.zmax, p07_box.zmax) - max(p06_box.zmin, p07_box.zmin))
    v3_p07_box = v3_p07.BoundingBox()
    v3_motion = json.loads((V3 / "motion.json").read_text())
    yellow_motion_same = all(
        motion[i]["transforms"]["P09"] == v3_motion[i]["transforms"]["P09"]
        for i in range(frames))
    checks["preservation"] = {
        "ok": bool(all(v["identical_to_v3"] for v in console_parts.values())
                   and black_ok and layer_overlap > 0 and yellow_motion_same),
        "untouched_parts_identical_to_v3": console_parts,
        "shared_pink_darkblue_layer_z_overlap": layer_overlap,
        "p06_z_span": [p06_box.zmin, p06_box.zmax],
        "p07_z_span": [p07_box.zmin, p07_box.zmax],
        "p07_z_span_preserved_vs_v3": abs(v3_p07_box.zmin - p07_box.zmin) <= 1e-3
                                      and abs(v3_p07_box.zmax - p07_box.zmax) <= 1e-3,
        "yellow_placement_transforms_identical_to_v3": yellow_motion_same,
        "black_housing_full_u": {
            "identical_to_v3": console_parts["P01_black.step"]["identical_to_v3"],
            "valid": bool(black.isValid()), "single_solid": len(black.Solids()) == 1,
            "width": bb.xmax - bb.xmin,
        },
    }
    save()

    # ---- 8. Copy artifacts to validation/ ----
    artifacts = {
        "assembly_motion_3d.gif": CAND / "assembly_motion_3d.gif",
        "assembly_viewer_v4.html": CAND / "assembly_viewer_v4.html",
        "assembly_preview.png": CAND / "assembly_preview.png",
        "contour_comparison.png": CAND / "contour_comparison.png",
        "collision_checks.json": CAND / "collision_checks.json",
        "pin_checks.json": CAND / "pin_checks.json",
        "joint_checks.json": CAND / "joint_checks.json",
    }
    copied_artifacts = []
    for name, src in artifacts.items():
        if src.exists():
            shutil.copy2(src, HERE / name)
            copied_artifacts.append(name)
    REPORT_DATA["artifacts"] = copied_artifacts

    all_ok = all([
        checks["body_collisions"]["ok"],
        checks["pin_collisions"]["ok"],
        checks["coaxial"]["ok"],
        checks["gray_darkblue_rigid"]["ok"],
        checks["gray_in_yellow"]["ok"],
        checks["p04_cut_necessity"]["ok"],
        checks["preservation"]["ok"],
    ])
    REPORT_DATA["passed"] = bool(all_ok)
    save()

    for key, val in checks.items():
        print(key, "OK" if val["ok"] else "FAIL", flush=True)
    print("stage2 passed:", REPORT_DATA["passed"], flush=True)
    print("report:", REPORT, flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
