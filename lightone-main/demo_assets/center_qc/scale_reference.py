"""Floor marker based pixel-to-centimeter scale conversion.

The marker must have a measured real-world length. If that value is unknown,
data is required; the code must not invent a physical scale.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, Optional, Tuple

import cv2
import numpy as np


def _candidate_marker_mask(image: np.ndarray) -> np.ndarray:
    """Detect saturated floor marker candidates without using identity data."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    mask = ((saturation > 70) & (value > 50)).astype(np.uint8) * 255
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)


def detect_floor_marker(
    image: np.ndarray,
    min_area_ratio: float = 0.0005,
    bottom_region_ratio: float = 0.50,
) -> Optional[Dict[str, object]]:
    """Return the strongest bottom-region rectangular marker candidate."""
    h, w = image.shape[:2]
    mask = _candidate_marker_mask(image)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = float(h * w * min_area_ratio)
    best = None
    best_area = 0.0

    for contour in contours:
        area = float(cv2.contourArea(contour))
        if area < min_area:
            continue
        rect = cv2.minAreaRect(contour)
        (cx, cy), (rw, rh), angle = rect
        if cy < h * bottom_region_ratio:
            continue
        if rw <= 1 or rh <= 1:
            continue
        aspect = max(rw, rh) / max(min(rw, rh), 1e-6)
        if aspect < 1.5:
            continue
        if area > best_area:
            best_area = area
            best = {
                "center_px": [float(cx), float(cy)],
                "size_px": [float(rw), float(rh)],
                "angle_deg": float(angle),
                "area_px": area,
                "pixel_length": float(max(rw, rh)),
            }
    return best


def pixel_to_cm_scale(marker_pixel_length: float, marker_real_length_cm: float) -> float:
    if marker_real_length_cm <= 0:
        raise ValueError("Data required: known marker length in cm must be positive.")
    if marker_pixel_length <= 0:
        raise ValueError("Marker pixel length must be positive.")
    return float(marker_real_length_cm) / float(marker_pixel_length)


def estimate_scale_from_marker(
    image: np.ndarray,
    marker_real_length_cm: float,
    min_area_ratio: float = 0.0005,
    bottom_region_ratio: float = 0.50,
) -> Dict[str, object]:
    marker = detect_floor_marker(
        image,
        min_area_ratio=min_area_ratio,
        bottom_region_ratio=bottom_region_ratio,
    )
    if marker is None:
        raise ValueError("바닥 기준 마커를 찾지 못했습니다. 다시 촬영하세요.")
    cm_per_px = pixel_to_cm_scale(
        float(marker["pixel_length"]),
        marker_real_length_cm,
    )
    return {
        "marker": marker,
        "marker_real_length_cm": float(marker_real_length_cm),
        "cm_per_px": cm_per_px,
        "px_per_cm": 1.0 / cm_per_px,
    }


def correct_px_measurement(measurement_px: float, cm_per_px: float) -> float:
    if measurement_px < 0:
        raise ValueError("Pixel measurement must be non-negative.")
    if cm_per_px <= 0:
        raise ValueError("Scale must be positive.")
    return float(measurement_px) * float(cm_per_px)


def read_image(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate px to cm scale from floor marker.")
    parser.add_argument("--input", required=True, help="Input QC image.")
    parser.add_argument(
        "--marker-length-cm",
        type=float,
        required=True,
        help="Measured real marker length in cm. Do not guess.",
    )
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    report = estimate_scale_from_marker(read_image(args.input), args.marker_length_cm)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

