#!/usr/bin/env python3
"""Stage 1: reproduce the V4 red-contour change from the V3 baseline and check it.

Copies the accepted V3 parts into validation/work/reproduction, applies the V4
red_contour.py with its contour_reference.png there, then checks:
  * P07/P04 validity and single-solid status,
  * preservation of the two P07 through-holes (radius, axis, span),
  * geometric coincidence of the result with the delivered V4 candidate parts
    (symmetric-difference volume, volume and bounding box),
  * registration parameters against V4 contour_change.json,
  * that all seven non-modified parts stay byte-identical to V3.

Results are written incrementally to validation/stage1_report.json so the
GitHub workflow can upload them even if a later step fails. This stage does not
run the 74-pose motion audit, rendering or viewer generation.
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
from OCP.BRepAdaptor import BRepAdaptor_Surface

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PKG = ROOT / "handoff" / "current_assembly"
V3 = PKG / "assembly_3d_v3"
V4 = PKG / "assembly_3d_v4"
WORK = HERE / "work" / "reproduction"
REPORT = HERE / "stage1_report.json"
STDOUT = HERE / "stage1_red_contour_stdout.txt"

SYMDIFF_TOL = 1e-3
VOLREL_TOL = 1e-6
HOLE_RADIUS_TOL = 1e-6
HOLE_AXIS_TOL = 1e-6
REG_TOL = 1e-6
CONTOUR_XY_TOL = 1e-6

PACKAGES = ["cadquery", "cadquery-ocp", "numpy", "scipy", "shapely", "pillow"]

REPORT_DATA = {
    "stage": 1,
    "title": "Воспроизведение изменения P07 по красному контуру из V3 (кандидат V4)",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "только этап 1: воспроизведение красного контура, валидность и совпадение с V4; "
             "74 положения, рендеринг и старый аудит не выполнялись",
    "commands": [
        "tar -xzf handoff/current_assembly.tar.gz",
        "pip install -r validation/requirements.txt",
        "python3 validation/stage1_reproduce_red_contour.py",
    ],
    "environment": {},
    "stages": {},
    "checks": {},
    "passed": None,
}


def save() -> None:
    REPORT.write_text(json.dumps(REPORT_DATA, indent=2, ensure_ascii=False))


def environment() -> dict:
    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "executable": sys.executable,
    }
    for name in PACKAGES:
        try:
            env[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            env[name] = None
    return env


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_step(path: Path):
    return cq.importers.importStep(str(path)).val()


def z_holes(shape) -> list[dict]:
    holes = []
    for face in shape.Faces():
        if face.geomType() != "CYLINDER":
            continue
        cyl = BRepAdaptor_Surface(face.wrapped).Cylinder()
        axis = cyl.Axis()
        direction = axis.Direction()
        if abs(direction.Z()) < 0.99:
            continue
        box = face.BoundingBox()
        loc = axis.Location()
        holes.append({
            "radius": float(cyl.Radius()),
            "axis_xy": [float(loc.X()), float(loc.Y())],
            "axis_dir_z": float(direction.Z()),
            "face_area": float(face.Area()),
            "z_span": [float(box.zmin), float(box.zmax)],
        })
    holes.sort(key=lambda h: (round(h["axis_xy"][0], 6), round(h["axis_xy"][1], 6)))
    return holes


def symmetric_difference(a, b) -> float:
    ab = a.cut(b)
    ba = b.cut(a)
    volume = 0.0
    if ab.Solids():
        volume += ab.Volume()
    if ba.Solids():
        volume += ba.Volume()
    return float(volume)


def bbox(shape) -> list[float]:
    box = shape.BoundingBox()
    return [box.xmin, box.xmax, box.ymin, box.ymax, box.zmin, box.zmax]


def main() -> int:
    REPORT_DATA["environment"] = environment()
    save()

    if not V3.is_dir() or not V4.is_dir():
        REPORT_DATA["stages"]["setup"] = {
            "ok": False,
            "error": f"не найден распакованный пакет: {PKG}. Выполните: tar -xzf handoff/current_assembly.tar.gz",
        }
        REPORT_DATA["passed"] = False
        save()
        print(REPORT_DATA["stages"]["setup"]["error"], file=sys.stderr)
        return 2

    if WORK.exists():
        shutil.rmtree(WORK)
    (WORK / "parts").mkdir(parents=True)

    copied_v3 = []
    for part in sorted((V3 / "parts").glob("*.step")):
        shutil.copy2(part, WORK / "parts" / part.name)
        copied_v3.append(part.name)
    for name in ("motion.json", "assembly_parameters.json"):
        src = V3 / name
        if src.exists():
            shutil.copy2(src, WORK / name)
    for name in ("red_contour.py", "contour_reference.png"):
        shutil.copy2(V4 / name, WORK / name)

    REPORT_DATA["stages"]["setup"] = {
        "ok": True,
        "work_dir": str(WORK.relative_to(ROOT)),
        "v3_parts_copied": copied_v3,
        "v4_inputs": ["red_contour.py", "contour_reference.png"],
    }
    save()

    command = [sys.executable, "red_contour.py"]
    started = time.time()
    proc = subprocess.run(command, cwd=WORK, capture_output=True, text=True)
    elapsed = time.time() - started
    stdout = proc.stdout + proc.stderr
    STDOUT.write_text(stdout)
    (WORK / "run_stdout.txt").write_text(stdout)
    REPORT_DATA["stages"]["apply_red_contour"] = {
        "ok": proc.returncode == 0,
        "command": " ".join(command),
        "cwd": str(WORK.relative_to(ROOT)),
        "returncode": proc.returncode,
        "seconds": round(elapsed, 3),
        "stdout": stdout.strip(),
        "stdout_file": str(STDOUT.relative_to(ROOT)),
    }
    save()
    if proc.returncode != 0:
        REPORT_DATA["passed"] = False
        save()
        print("red_contour.py failed; see", STDOUT, file=sys.stderr)
        return 1

    checks: dict = REPORT_DATA["checks"]

    repro_parts = WORK / "parts"
    v4_parts = V4 / "parts"
    v3_parts = V3 / "parts"

    holes_v3 = z_holes(load_step(v3_parts / "P07_dark_blue.step"))
    holes_v4 = z_holes(load_step(v4_parts / "P07_dark_blue.step"))

    geometry = {}
    for name in ("P07_dark_blue.step", "P04_green.step"):
        repro = load_step(repro_parts / name)
        delivered = load_step(v4_parts / name)
        baseline = load_step(v3_parts / name)
        symdiff = symmetric_difference(repro, delivered)
        vol_rel = abs(repro.Volume() - delivered.Volume()) / delivered.Volume()
        bb_repro = bbox(repro)
        bb_delivered = bbox(delivered)
        bb_max = max(abs(x - y) for x, y in zip(bb_repro, bb_delivered))
        entry = {
            "valid": bool(repro.isValid()),
            "solids": len(repro.Solids()),
            "valid_expected": True,
            "single_solid": len(repro.Solids()) == 1,
            "repro_volume": float(repro.Volume()),
            "v4_volume": float(delivered.Volume()),
            "v3_volume": float(baseline.Volume()),
            "volume_rel_diff_vs_v4": float(vol_rel),
            "symmetric_difference_volume_vs_v4": symdiff,
            "bbox_max_abs_diff_vs_v4": float(bb_max),
            "differs_from_v3": sha256(repro_parts / name) != sha256(v3_parts / name),
        }
        entry["ok"] = bool(
            entry["valid"]
            and entry["single_solid"]
            and symdiff <= SYMDIFF_TOL
            and vol_rel <= VOLREL_TOL
            and bb_max <= SYMDIFF_TOL
            and entry["differs_from_v3"]
        )
        geometry[name] = entry
    checks["geometry"] = geometry
    save()

    holes_repro = z_holes(load_step(repro_parts / "P07_dark_blue.step"))
    hole_matches = []
    for hole_repro in holes_repro:
        best = None
        for hole_v3 in holes_v3:
            dxy = math.dist(hole_repro["axis_xy"], hole_v3["axis_xy"])
            if best is None or dxy < best["axis_xy_distance"]:
                best = {
                    "axis_xy_distance": float(dxy),
                    "radius_diff": float(abs(hole_repro["radius"] - hole_v3["radius"])),
                    "v3_radius": hole_v3["radius"],
                    "v3_z_span": hole_v3["z_span"],
                }
        hole_matches.append({"repro": hole_repro, "nearest_v3": best})
    holes_ok = (
        len(holes_repro) == len(holes_v3) == 2
        and all(
            m["nearest_v3"] is not None
            and m["nearest_v3"]["axis_xy_distance"] <= HOLE_AXIS_TOL
            and m["nearest_v3"]["radius_diff"] <= HOLE_RADIUS_TOL
            for m in hole_matches
        )
    )
    checks["p07_holes"] = {
        "ok": bool(holes_ok),
        "count_v3": len(holes_v3),
        "count_v4": len(holes_v4),
        "count_repro": len(holes_repro),
        "axis_tol": HOLE_AXIS_TOL,
        "radius_tol": HOLE_RADIUS_TOL,
        "holes_v3": holes_v3,
        "holes_v4": holes_v4,
        "holes_repro": holes_repro,
        "matches_to_v3": hole_matches,
    }
    save()

    repro_contour = json.loads((WORK / "contour_change.json").read_text())
    v4_contour = json.loads((V4 / "contour_change.json").read_text())
    xy_repro = np.array(repro_contour["red_contour_xy"], float)
    xy_v4 = np.array(v4_contour["red_contour_xy"], float)
    xy_max = float(np.abs(xy_repro - xy_v4).max()) if xy_repro.shape == xy_v4.shape else None
    reg = {
        "scale_repro": repro_contour["image_scale"],
        "scale_v4": v4_contour["image_scale"],
        "scale_diff": abs(repro_contour["image_scale"] - v4_contour["image_scale"]),
        "angle_repro": repro_contour["angle"],
        "angle_v4": v4_contour["angle"],
        "angle_diff": abs(repro_contour["angle"] - v4_contour["angle"]),
        "rms_repro": repro_contour["fit_rms_pixels"],
        "rms_v4": v4_contour["fit_rms_pixels"],
        "rms_diff": abs(repro_contour["fit_rms_pixels"] - v4_contour["fit_rms_pixels"]),
        "contour_points_repro": int(len(xy_repro)),
        "contour_points_v4": int(len(xy_v4)),
        "contour_xy_max_abs_diff": xy_max,
        "tol": REG_TOL,
        "contour_xy_tol": CONTOUR_XY_TOL,
    }
    reg["ok"] = bool(
        reg["scale_diff"] <= REG_TOL
        and reg["angle_diff"] <= REG_TOL
        and reg["rms_diff"] <= REG_TOL
        and xy_max is not None
        and xy_max <= CONTOUR_XY_TOL
    )
    checks["registration"] = reg
    save()

    untouched = {}
    for part in sorted(v3_parts.glob("*.step")):
        if part.name in ("P07_dark_blue.step", "P04_green.step"):
            continue
        same = sha256(part) == sha256(repro_parts / part.name)
        untouched[part.name] = {"identical_to_v3": same, "ok": same}
    checks["untouched_parts"] = {
        "ok": all(v["ok"] for v in untouched.values()),
        "parts": untouched,
    }
    save()

    all_ok = all(
        [
            REPORT_DATA["stages"]["apply_red_contour"]["ok"],
            all(v["ok"] for v in geometry.values()),
            checks["p07_holes"]["ok"],
            checks["registration"]["ok"],
            checks["untouched_parts"]["ok"],
        ]
    )
    REPORT_DATA["passed"] = bool(all_ok)
    save()

    for key in ("p07_holes", "registration", "untouched_parts"):
        print(key, "OK" if checks[key]["ok"] else "FAIL", flush=True)
    for name, entry in geometry.items():
        print(name, "OK" if entry["ok"] else "FAIL", flush=True)
    print("stage1 passed:", REPORT_DATA["passed"], flush=True)
    print("report:", REPORT, flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
