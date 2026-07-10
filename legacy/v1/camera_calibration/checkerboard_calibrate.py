"""Calibrate Canon EOS R7 camera intrinsics from checkerboard images.

The LIGHT ONE body analysis system uses these values as camera reliability
evidence for posture reference information. It is not a medical diagnosis
device and this module does not process personally identifiable images.
Use checkerboard or marker images only.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import cv2
import numpy as np


DEFAULT_PATTERN_SIZE = (9, 6)


@dataclass
class CalibrationResult:
    camera_id: str
    K: np.ndarray
    D: np.ndarray
    image_size: Tuple[int, int]
    rms_error: float
    image_count: int

    def to_json_dict(self) -> dict:
        return {
            "camera_id": self.camera_id,
            "K": self.K.tolist(),
            "D": self.D.ravel().tolist(),
            "image_size": list(self.image_size),
            "rms_error": float(self.rms_error),
            "image_count": int(self.image_count),
            "note": (
                "LIGHT ONE posture values are reference information only; "
                "this is not a medical diagnosis device."
            ),
        }


def build_checkerboard_object_points(
    pattern_size: Tuple[int, int] = DEFAULT_PATTERN_SIZE,
    square_size: float = 1.0,
) -> np.ndarray:
    """Return 3D checkerboard corner points for one image."""
    cols, rows = pattern_size
    objp = np.zeros((rows * cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)
    objp *= float(square_size)
    return objp


def collect_image_paths(patterns: Sequence[str]) -> List[str]:
    """Expand image globs, preserving deterministic order."""
    paths: List[str] = []
    for pattern in patterns:
        expanded = sorted(glob.glob(pattern))
        if expanded:
            paths.extend(expanded)
        elif os.path.isfile(pattern):
            paths.append(pattern)
    return sorted(dict.fromkeys(paths))


def find_checkerboard_corners(
    image_paths: Iterable[str],
    pattern_size: Tuple[int, int] = DEFAULT_PATTERN_SIZE,
    square_size: float = 1.0,
) -> Tuple[List[np.ndarray], List[np.ndarray], Tuple[int, int]]:
    """Find checkerboard image points from real calibration images."""
    objp = build_checkerboard_object_points(pattern_size, square_size)
    object_points: List[np.ndarray] = []
    image_points: List[np.ndarray] = []
    image_size: Tuple[int, int] | None = None

    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        30,
        0.001,
    )

    for path in image_paths:
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Cannot read image: {path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        current_size = (gray.shape[1], gray.shape[0])
        if image_size is None:
            image_size = current_size
        elif image_size != current_size:
            raise ValueError(
                f"All images for one camera must have the same size. "
                f"Expected {image_size}, got {current_size} for {path}"
            )

        found, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        if not found:
            continue

        refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        object_points.append(objp.copy())
        image_points.append(refined)

    if image_size is None:
        raise ValueError("No readable images found. Data required.")
    if not object_points:
        raise ValueError(
            "No checkerboard corners detected. Data required: provide clear "
            "9x6 checkerboard/marker images."
        )
    return object_points, image_points, image_size


def calibrate_camera(
    camera_id: str,
    image_paths: Sequence[str],
    pattern_size: Tuple[int, int] = DEFAULT_PATTERN_SIZE,
    square_size: float = 1.0,
) -> CalibrationResult:
    object_points, image_points, image_size = find_checkerboard_corners(
        image_paths=image_paths,
        pattern_size=pattern_size,
        square_size=square_size,
    )

    rms, K, D, _rvecs, _tvecs = cv2.calibrateCamera(
        object_points,
        image_points,
        image_size,
        None,
        None,
    )
    return CalibrationResult(
        camera_id=camera_id,
        K=K,
        D=D,
        image_size=image_size,
        rms_error=float(rms),
        image_count=len(object_points),
    )


def save_calibration(result: CalibrationResult, output_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result.to_json_dict(), f, indent=2)


def parse_pattern_size(value: str) -> Tuple[int, int]:
    try:
        cols, rows = value.lower().split("x", 1)
        return int(cols), int(rows)
    except Exception as exc:
        raise argparse.ArgumentTypeError("Pattern size must look like 9x6") from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calibrate one camera from checkerboard images."
    )
    parser.add_argument("--camera-id", required=True, help="Example: front, rear, left, right")
    parser.add_argument(
        "--images",
        nargs="+",
        required=True,
        help="Image paths or glob patterns for one camera.",
    )
    parser.add_argument("--output", required=True, help="Calibration JSON path.")
    parser.add_argument(
        "--pattern-size",
        type=parse_pattern_size,
        default=DEFAULT_PATTERN_SIZE,
        help="Inner checkerboard corners as COLSxROWS. Default: 9x6",
    )
    parser.add_argument(
        "--square-size",
        type=float,
        default=1.0,
        help="Checkerboard square size in any consistent unit.",
    )
    args = parser.parse_args()

    image_paths = collect_image_paths(args.images)
    if not image_paths:
        raise SystemExit("Data required: no checkerboard images matched --images.")

    result = calibrate_camera(
        camera_id=args.camera_id,
        image_paths=image_paths,
        pattern_size=args.pattern_size,
        square_size=args.square_size,
    )
    save_calibration(result, args.output)
    print(
        f"{result.camera_id}: saved {args.output} "
        f"({result.image_count} images, RMS={result.rms_error:.6f}px)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

