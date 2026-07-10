"""Undistort checkerboard or marker images using saved camera parameters.

The LIGHT ONE system uses this only to support camera measurement reliability
for posture reference information. It is not a medical diagnosis device, and
personally identifiable face/body photos are not the intended processing input.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Tuple

import cv2
import numpy as np


def load_calibration(path: str) -> Tuple[str, np.ndarray, np.ndarray, Tuple[int, int]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (
        str(data["camera_id"]),
        np.asarray(data["K"], dtype=np.float64),
        np.asarray(data["D"], dtype=np.float64).reshape(-1, 1),
        tuple(int(v) for v in data["image_size"]),
    )


def undistort_image(
    image: np.ndarray,
    K: np.ndarray,
    D: np.ndarray,
) -> np.ndarray:
    h, w = image.shape[:2]
    new_K, _roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), 1.0, (w, h))
    return cv2.undistort(image, K, D, None, new_K)


def save_before_after_comparison(
    original: np.ndarray,
    corrected: np.ndarray,
    output_path: str,
) -> None:
    h = min(original.shape[0], corrected.shape[0])
    original_crop = original[:h]
    corrected_crop = corrected[:h]
    comparison = np.hstack([original_crop, corrected_crop])

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(comparison, "before", (20, 40), font, 1.0, (0, 255, 255), 2)
    cv2.putText(
        comparison,
        "after",
        (original_crop.shape[1] + 20, 40),
        font,
        1.0,
        (0, 255, 255),
        2,
    )
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    if not cv2.imwrite(output_path, comparison):
        raise ValueError(f"Could not write comparison image: {output_path}")


def undistort_file(calibration_path: str, image_path: str, output_path: str) -> None:
    camera_id, K, D, expected_size = load_calibration(calibration_path)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")

    actual_size = (image.shape[1], image.shape[0])
    if actual_size != expected_size:
        raise ValueError(
            f"Image size mismatch for {camera_id}: calibration has "
            f"{expected_size}, image has {actual_size}"
        )

    corrected = undistort_image(image, K, D)
    save_before_after_comparison(image, corrected, output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Save before/after undistortion image.")
    parser.add_argument("--calibration", required=True, help="Calibration JSON path.")
    parser.add_argument("--image", required=True, help="Input checkerboard/marker image.")
    parser.add_argument("--output", required=True, help="Output comparison image path.")
    args = parser.parse_args()

    undistort_file(args.calibration, args.image, args.output)
    print(f"saved {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

