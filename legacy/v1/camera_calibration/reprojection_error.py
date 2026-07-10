"""Compute per-camera reprojection error in pixels.

Only actual calculated values are reported. If calibration images are missing,
the report explicitly says data is required. LIGHT ONE posture values are
reference information only and are not a medical diagnosis device output.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
from typing import List, Sequence, Tuple

import cv2
import numpy as np

try:
    from .checkerboard_calibrate import (
        DEFAULT_PATTERN_SIZE,
        build_checkerboard_object_points,
        collect_image_paths,
        find_checkerboard_corners,
        parse_pattern_size,
    )
except ImportError:
    from checkerboard_calibrate import (  # type: ignore
        DEFAULT_PATTERN_SIZE,
        build_checkerboard_object_points,
        collect_image_paths,
        find_checkerboard_corners,
        parse_pattern_size,
    )


PASS_THRESHOLD_PX = 0.5
FAIL_THRESHOLD_PX = 1.0


def load_calibration(path: str) -> Tuple[str, np.ndarray, np.ndarray, Tuple[int, int]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (
        str(data["camera_id"]),
        np.asarray(data["K"], dtype=np.float64),
        np.asarray(data["D"], dtype=np.float64).reshape(-1, 1),
        tuple(int(v) for v in data["image_size"]),
    )


def calculate_reprojection_errors(
    object_points: Sequence[np.ndarray],
    image_points: Sequence[np.ndarray],
    K: np.ndarray,
    D: np.ndarray,
) -> np.ndarray:
    """Return one mean reprojection error per calibration image."""
    errors: List[float] = []
    for objp, imgp in zip(object_points, image_points):
        success, rvec, tvec = cv2.solvePnP(objp, imgp, K, D)
        if not success:
            raise ValueError("Could not solve camera pose for a calibration image.")
        projected, _ = cv2.projectPoints(objp, rvec, tvec, K, D)
        delta = imgp.reshape(-1, 2) - projected.reshape(-1, 2)
        per_corner = np.linalg.norm(delta, axis=1)
        errors.append(float(np.mean(per_corner)))
    return np.asarray(errors, dtype=np.float64)


def classify_error(mean_px: float) -> str:
    if mean_px < PASS_THRESHOLD_PX:
        return "PASS"
    if mean_px >= FAIL_THRESHOLD_PX:
        return "FAIL"
    return "CHECK"


def summarize_errors(camera_id: str, errors: np.ndarray) -> dict:
    if errors.size == 0:
        return {
            "camera_id": camera_id,
            "status": "DATA_REQUIRED",
            "message": "Data required: no valid checkerboard detections.",
        }
    mean_px = float(np.mean(errors))
    return {
        "camera_id": camera_id,
        "mean_px": mean_px,
        "std_px": float(np.std(errors)),
        "max_px": float(np.max(errors)),
        "image_count": int(errors.size),
        "status": classify_error(mean_px),
    }


def report_for_camera(
    calibration_path: str,
    image_paths: Sequence[str],
    pattern_size: Tuple[int, int] = DEFAULT_PATTERN_SIZE,
    square_size: float = 1.0,
) -> dict:
    camera_id, K, D, expected_size = load_calibration(calibration_path)
    object_points, image_points, image_size = find_checkerboard_corners(
        image_paths=image_paths,
        pattern_size=pattern_size,
        square_size=square_size,
    )
    if image_size != expected_size:
        raise ValueError(
            f"Image size mismatch for {camera_id}: calibration has "
            f"{expected_size}, images have {image_size}"
        )
    errors = calculate_reprojection_errors(object_points, image_points, K, D)
    return summarize_errors(camera_id, errors)


def write_report(report: dict, output_path: str | None) -> None:
    text = json.dumps(report, indent=2)
    print(text)
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Report reprojection error in pixels.")
    parser.add_argument("--calibration", required=True, help="Calibration JSON path.")
    parser.add_argument("--images", nargs="+", required=True, help="Image paths or globs.")
    parser.add_argument("--output", help="Optional report JSON path.")
    parser.add_argument(
        "--pattern-size",
        type=parse_pattern_size,
        default=DEFAULT_PATTERN_SIZE,
        help="Inner checkerboard corners as COLSxROWS. Default: 9x6",
    )
    parser.add_argument("--square-size", type=float, default=1.0)
    args = parser.parse_args()

    image_paths = collect_image_paths(args.images)
    if not image_paths:
        raise SystemExit("Data required: no checkerboard images matched --images.")

    report = report_for_camera(
        calibration_path=args.calibration,
        image_paths=image_paths,
        pattern_size=args.pattern_size,
        square_size=args.square_size,
    )
    write_report(report, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

