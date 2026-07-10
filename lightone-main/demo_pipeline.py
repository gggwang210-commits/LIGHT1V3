"""One-command LIGHT ONE measurement reliability demo.

Run:
    python demo_pipeline.py

The demo uses synthetic checkerboard observations and synthetic booth images.
Every number printed is calculated by the pipeline; no benchmark values are
invented. LIGHT ONE provides body-shape reference information and does not
replace medical diagnosis.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Tuple

import cv2
import numpy as np

from camera_calibration.checkerboard_calibrate import (
    build_checkerboard_object_points,
)
from camera_calibration.reprojection_error import (
    calculate_reprojection_errors,
    summarize_errors,
)
from center_qc.booth_spec import BOOTH_SPEC, NEEDS_VERIFICATION
from center_qc.qc_gate import run_qc_gate
from center_qc.scale_reference import estimate_scale_from_marker
from lighting_normalization.normalize import normalize_lighting
from lighting_normalization.uniformity_check import calculate_uniformity


OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(OUTPUT_DIR, "demo_assets")
RESULT_JSON = os.path.join(OUTPUT_DIR, "demo_result.json")


def to_relative(path: str) -> str:
    """Return repository-relative paths for portable JSON reports."""
    return os.path.relpath(path, OUTPUT_DIR).replace(os.sep, "/")


def ensure_dirs() -> None:
    os.makedirs(ASSET_DIR, exist_ok=True)


def save_image(name: str, image: np.ndarray) -> str:
    path = os.path.join(ASSET_DIR, name)
    if not cv2.imwrite(path, image):
        raise ValueError(f"Could not save image: {path}")
    return path


def create_checkerboard_preview(
    cols: int = 10,
    rows: int = 7,
    square_px: int = 48,
) -> str:
    image = np.zeros((rows * square_px, cols * square_px), dtype=np.uint8)
    for y in range(rows):
        for x in range(cols):
            if (x + y) % 2 == 0:
                image[
                    y * square_px : (y + 1) * square_px,
                    x * square_px : (x + 1) * square_px,
                ] = 255
    return save_image("synthetic_checkerboard_preview.png", cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))


def synthetic_calibration_views(
    K: np.ndarray,
    D: np.ndarray,
    pattern_size: Tuple[int, int] = (9, 6),
    square_size: float = 25.0,
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    objp = build_checkerboard_object_points(pattern_size, square_size)
    object_points: List[np.ndarray] = []
    image_points: List[np.ndarray] = []
    poses = [
        ((0.04, -0.03, 0.02), (-100.0, -70.0, 980.0)),
        ((0.01, 0.05, -0.04), (-40.0, -60.0, 930.0)),
        ((-0.04, 0.02, 0.03), (20.0, -90.0, 1010.0)),
        ((0.03, -0.06, 0.01), (-80.0, -20.0, 960.0)),
        ((-0.02, -0.03, -0.04), (-20.0, 10.0, 1040.0)),
        ((0.05, 0.01, 0.03), (40.0, -30.0, 950.0)),
        ((-0.05, 0.05, 0.01), (-70.0, 0.0, 1000.0)),
        ((0.02, -0.04, -0.02), (10.0, 20.0, 970.0)),
        ((-0.01, 0.03, 0.05), (-50.0, -40.0, 1020.0)),
        ((0.04, 0.04, -0.01), (30.0, 15.0, 990.0)),
    ]
    for rvec_values, tvec_values in poses:
        rvec = np.asarray(rvec_values, dtype=np.float64).reshape(3, 1)
        tvec = np.asarray(tvec_values, dtype=np.float64).reshape(3, 1)
        projected, _ = cv2.projectPoints(objp, rvec, tvec, K, D)
        object_points.append(objp.astype(np.float32))
        image_points.append(projected.astype(np.float32))
    return object_points, image_points


def run_p1_camera_calibration() -> Dict[str, object]:
    image_size = (1920, 1080)
    camera_defs = {
        "front": (1400.0, 1395.0, -0.08, 0.014),
        "rear": (1410.0, 1402.0, -0.075, 0.012),
        "left": (1392.0, 1401.0, -0.082, 0.015),
        "right": (1405.0, 1398.0, -0.078, 0.013),
    }
    reports: Dict[str, object] = {}
    for camera_id, (fx, fy, k1, k2) in camera_defs.items():
        K_true = np.array(
            [[fx, 0.0, image_size[0] / 2.0], [0.0, fy, image_size[1] / 2.0], [0.0, 0.0, 1.0]],
            dtype=np.float64,
        )
        D_true = np.array([k1, k2, 0.0004, -0.0003, 0.0], dtype=np.float64)
        object_points, image_points = synthetic_calibration_views(K_true, D_true)
        rms, K_est, D_est, _rvecs, _tvecs = cv2.calibrateCamera(
            object_points,
            image_points,
            image_size,
            None,
            None,
        )
        errors = calculate_reprojection_errors(object_points, image_points, K_est, D_est)
        report = summarize_errors(camera_id, errors)
        report["rms_px"] = float(rms)
        report["image_size"] = list(image_size)
        reports[camera_id] = report
    return reports


def create_lighting_patch(width: int = 480, height: int = 320) -> np.ndarray:
    image = np.full((height, width, 3), 155, dtype=np.float32)
    image[:, :, 0] *= 1.28
    image[:, :, 1] *= 0.92
    image[:, :, 2] *= 0.75
    x_gain = np.linspace(0.97, 1.02, width, dtype=np.float32).reshape(1, width, 1)
    image *= x_gain
    yy, xx = np.mgrid[0:height, 0:width]
    shadow = ((xx - 150) ** 2 / (110**2) + (yy - 205) ** 2 / (75**2)) < 1.0
    image[shadow] *= 0.99
    return np.clip(image, 0, 255).astype(np.uint8)


def run_p2_lighting() -> Dict[str, object]:
    before = create_lighting_patch()
    before_path = save_image("lighting_before.png", before)
    after, normalization_metrics = normalize_lighting(before, target_mean=128.0)
    after_path = save_image("lighting_after.png", after)
    before_uniformity = calculate_uniformity(before, grid=(8, 8))
    after_uniformity = calculate_uniformity(after, grid=(8, 8))
    return {
        "input_image": to_relative(before_path),
        "normalized_image": to_relative(after_path),
        "normalization": normalization_metrics,
        "before": before_uniformity,
        "after": after_uniformity,
    }


def create_standard_booth_image(width: int = 500, height: int = 720) -> np.ndarray:
    image = np.full((height, width, 3), 190, dtype=np.uint8)
    cx = width // 2
    cv2.rectangle(image, (cx - 55, 125), (cx + 55, 610), (45, 45, 45), -1)
    cv2.circle(image, (cx, 82), 34, (45, 45, 45), -1)
    cv2.rectangle(image, (cx - 70, height - 65), (cx + 70, height - 43), (0, 210, 0), -1)
    return image


def run_p3_center_qc() -> Dict[str, object]:
    image = create_standard_booth_image()
    path = save_image("center_qc_standard.png", image)
    qc_report = run_qc_gate(image)
    scale_report = estimate_scale_from_marker(image, marker_real_length_cm=70.0)
    return {
        "input_image": to_relative(path),
        "qc": qc_report,
        "scale_reference_demo": scale_report,
        "booth_spec_unverified_marker": NEEDS_VERIFICATION,
        "booth_spec": {
            "camera_height_cm": BOOTH_SPEC["camera"]["camera_height_cm"],
            "subject_to_camera_distance_cm": BOOTH_SPEC["subject_position"]["subject_to_camera_distance_cm"],
            "front_angle_deg": BOOTH_SPEC["four_direction_layout"]["front_angle_deg"],
            "known_marker_length_cm": BOOTH_SPEC["floor_marker"]["known_marker_length_cm"],
        },
    }


def print_p1(camera_reports: Dict[str, object]) -> None:
    print("\n[P1] 카메라 캘리브레이션 / 재투영 오차")
    for camera_id, report_obj in camera_reports.items():
        report = dict(report_obj)
        print(
            f"- {camera_id}: 평균 {report['mean_px']:.6f}px, "
            f"표준편차 {report['std_px']:.6f}px, 최대 {report['max_px']:.6f}px, "
            f"{report['status']}"
        )


def print_p2(lighting_report: Dict[str, object]) -> None:
    before = lighting_report["before"]
    after = lighting_report["after"]
    print("\n[P2] 조명 정규화 / 균일도 검사")
    print(
        f"- 정규화 전: 균일도 {before['uniformity_percent']:.2f}%, "
        f"그림자 {before['shadow_ratio_percent']:.2f}%, {before['status']}"
    )
    print(
        f"- 정규화 후: 균일도 {after['uniformity_percent']:.2f}%, "
        f"그림자 {after['shadow_ratio_percent']:.2f}%, {after['status']}"
    )


def print_p3(center_report: Dict[str, object]) -> None:
    qc = center_report["qc"]
    print("\n[P3] 촬영 부스 QC 게이트")
    print(f"- 전체 결과: {qc['status']} / {qc['message']}")
    for check in qc["checks"]:
        status = "PASS" if check["pass"] else "FAIL"
        print(f"  - {check['name']}: {status} ({check['reason']})")
    scale = center_report["scale_reference_demo"]
    print(
        f"- 바닥 마커 스케일: {scale['cm_per_px']:.6f} cm/px "
        f"(데모 마커 실제 길이 {scale['marker_real_length_cm']:.2f} cm)"
    )
    print("- booth_spec 미확정 물리 스펙:", center_report["booth_spec"])


def main() -> int:
    ensure_dirs()
    checkerboard_path = create_checkerboard_preview()
    p1 = run_p1_camera_calibration()
    p2 = run_p2_lighting()
    p3 = run_p3_center_qc()
    result = {
        "system": "LIGHT ONE measurement reliability demo",
        "positioning": "체형 참고 정보 서비스이며 의료 진단기기가 아닙니다.",
        "synthetic_assets": {
            "checkerboard_preview": to_relative(checkerboard_path),
            "note": "합성 데이터로 실행되며 모든 출력 수치는 실제 계산값입니다.",
        },
        "P1_camera_calibration": p1,
        "P2_lighting_normalization": p2,
        "P3_center_qc": p3,
    }
    with open(RESULT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("LIGHT ONE 측정 신뢰성 통합 데모")
    print("체형 참고 정보 서비스이며 의료 진단기기가 아닙니다.")
    print_p1(p1)
    print_p2(p2)
    print_p3(p3)
    print(f"\n결과 JSON 저장: {to_relative(RESULT_JSON)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
