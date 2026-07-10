"""Automatic QC gate for standard booth capture images.

The gate checks only composition, controlled background, and floor marker
presence. It does not save or identify a person.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

try:
    from .booth_spec import BOOTH_SPEC
    from .scale_reference import detect_floor_marker
except ImportError:
    from booth_spec import BOOTH_SPEC  # type: ignore
    from scale_reference import detect_floor_marker  # type: ignore


def _border_pixels(image: np.ndarray, border_ratio: float = 0.06) -> np.ndarray:
    h, w = image.shape[:2]
    border = max(2, int(round(min(h, w) * border_ratio)))
    top = image[:border, :, :]
    bottom = image[-border:, :, :]
    left = image[:, :border, :]
    right = image[:, -border:, :]
    return np.concatenate(
        [
            top.reshape(-1, 3),
            bottom.reshape(-1, 3),
            left.reshape(-1, 3),
            right.reshape(-1, 3),
        ],
        axis=0,
    )


def background_uniformity(image: np.ndarray) -> Dict[str, object]:
    """Measure whether border background is close to a single color."""
    border = _border_pixels(image)
    border_hsv = cv2.cvtColor(border.reshape(1, -1, 3), cv2.COLOR_BGR2HSV).reshape(-1, 3)
    neutral_border = border[border_hsv[:, 1] <= 70]
    if neutral_border.size == 0:
        neutral_border = border
    border = neutral_border.astype(np.float32)
    median_color = np.median(border, axis=0)
    color_distance = np.linalg.norm(border - median_color.reshape(1, 3), axis=1)
    return {
        "median_bgr": [float(v) for v in median_color],
        "border_color_std": float(np.std(color_distance)),
        "border_color_mean_distance": float(np.mean(color_distance)),
    }


def foreground_mask(image: np.ndarray, background_bgr: np.ndarray) -> np.ndarray:
    diff = np.linalg.norm(image.astype(np.float32) - background_bgr.reshape(1, 1, 3), axis=2)
    mask = (diff > 35.0).astype(np.uint8) * 255
    marker_mask = _saturated_mask(image)
    mask[marker_mask > 0] = 0
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)


def _saturated_mask(image: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return (((hsv[:, :, 1] > 70) & (hsv[:, :, 2] > 50)).astype(np.uint8)) * 255


def find_subject_bbox(image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    bg = np.asarray(background_uniformity(image)["median_bgr"], dtype=np.float32)
    mask = foreground_mask(image, bg)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    h, w = image.shape[:2]
    min_area = h * w * 0.02
    best_bbox = None
    best_area = 0.0
    for contour in contours:
        area = float(cv2.contourArea(contour))
        if area < min_area:
            continue
        x, y, bw, bh = cv2.boundingRect(contour)
        if area > best_area:
            best_area = area
            best_bbox = (x, y, bw, bh)
    return best_bbox


def check_subject_composition(
    image: np.ndarray,
    center_tolerance_ratio: float = 0.15,
    min_height_ratio: float = 0.45,
    edge_margin_px: int = 5,
) -> Dict[str, object]:
    h, w = image.shape[:2]
    bbox = find_subject_bbox(image)
    if bbox is None:
        return {
            "name": "피험자 구도",
            "pass": False,
            "reason": "피험자 전경 영역을 찾지 못했습니다.",
        }

    x, y, bw, bh = bbox
    center_x = x + bw / 2.0
    center_offset_ratio = abs(center_x - w / 2.0) / max(w, 1)
    height_ratio = bh / max(h, 1)
    touches_edge = (
        x <= edge_margin_px
        or y <= edge_margin_px
        or x + bw >= w - edge_margin_px
        or y + bh >= h - edge_margin_px
    )

    failures: List[str] = []
    if center_offset_ratio > center_tolerance_ratio:
        failures.append("프레임 중앙에서 벗어났습니다")
    if height_ratio < min_height_ratio:
        failures.append("전신이 충분히 크게 포함되지 않았습니다")
    if touches_edge:
        failures.append("몸 일부가 프레임 가장자리에 닿아 잘렸을 가능성이 있습니다")

    return {
        "name": "피험자 구도",
        "pass": not failures,
        "reason": "정상" if not failures else ", ".join(failures),
        "bbox": [int(v) for v in bbox],
        "center_offset_ratio": float(center_offset_ratio),
        "height_ratio": float(height_ratio),
    }


def check_background(image: np.ndarray, max_border_std: float = 12.0) -> Dict[str, object]:
    metrics = background_uniformity(image)
    pass_check = float(metrics["border_color_mean_distance"]) <= max_border_std
    return {
        "name": "배경 단색 통제",
        "pass": pass_check,
        "reason": "정상" if pass_check else "배경 색/무늬 변화가 커서 단색 배경으로 보기 어렵습니다.",
        **metrics,
        "threshold_border_mean_distance": float(max_border_std),
    }


def check_floor_marker(
    image: np.ndarray,
    min_area_ratio: float = 0.0005,
    bottom_region_ratio: float = 0.50,
) -> Dict[str, object]:
    marker = detect_floor_marker(
        image,
        min_area_ratio=min_area_ratio,
        bottom_region_ratio=bottom_region_ratio,
    )
    if marker is None:
        return {
            "name": "바닥 기준 마커",
            "pass": False,
            "reason": "거리/스케일 보정용 바닥 마커를 찾지 못했습니다.",
        }
    return {
        "name": "바닥 기준 마커",
        "pass": True,
        "reason": "정상",
        "marker": marker,
    }


def run_qc_gate(image: np.ndarray) -> Dict[str, object]:
    thresholds = BOOTH_SPEC["image_qc_thresholds"]
    composition = check_subject_composition(
        image,
        center_tolerance_ratio=float(thresholds["subject_center_tolerance_ratio"]),
        min_height_ratio=float(thresholds["subject_min_height_ratio"]),
        edge_margin_px=int(thresholds["subject_edge_margin_px"]),
    )
    background = check_background(
        image,
        max_border_std=float(thresholds["background_max_border_std"]),
    )
    marker = check_floor_marker(
        image,
        min_area_ratio=float(thresholds["marker_min_area_ratio"]),
        bottom_region_ratio=float(thresholds["marker_bottom_region_ratio"]),
    )
    checks = [composition, background, marker]
    failures = [check for check in checks if not bool(check["pass"])]
    passed = not failures
    return {
        "pass": passed,
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "message": "촬영 QC 통과" if passed else "다시 촬영하세요: " + " / ".join(
            f"{item['name']} - {item['reason']}" for item in failures
        ),
        "identity_policy": "신원 정보 비저장. QC는 구도/배경/마커만 판단.",
    }


def read_image(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def main() -> int:
    parser = argparse.ArgumentParser(description="Run LIGHT ONE center QC gate.")
    parser.add_argument("--input", required=True, help="Input booth QC image.")
    parser.add_argument("--output", help="Optional JSON output path.")
    args = parser.parse_args()

    report = run_qc_gate(read_image(args.input))
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
