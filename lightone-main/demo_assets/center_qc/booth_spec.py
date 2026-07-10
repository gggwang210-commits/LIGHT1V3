"""Standard booth specification placeholders for LIGHT ONE capture centers.

Physical values must be measured at the actual center before use. Unknown
specifications are intentionally marked as [확인필요]; do not replace them with
guesses. This module documents the capture standard used by the QC gate.
"""

from __future__ import annotations

import argparse
import json
from typing import Dict


NEEDS_VERIFICATION = "[확인필요]"


BOOTH_SPEC: Dict[str, object] = {
    "purpose": "센터별 촬영 조건 표준화 및 자동 QC 기준 문서",
    "identity_policy": "신원 정보 비저장. QC는 구도/배경/바닥 마커만 판단.",
    "camera": {
        "model": "Canon EOS R7",
        "lens": "RF 35mm F1.8",
        "mounting": "고정 설치",
        "camera_height_cm": NEEDS_VERIFICATION,
        "camera_pitch_deg": NEEDS_VERIFICATION,
        "camera_roll_deg": NEEDS_VERIFICATION,
        "camera_yaw_deg": NEEDS_VERIFICATION,
    },
    "subject_position": {
        "subject_to_camera_distance_cm": NEEDS_VERIFICATION,
        "standing_marker_center": NEEDS_VERIFICATION,
        "allowed_center_offset_cm": NEEDS_VERIFICATION,
    },
    "four_direction_layout": {
        "front_angle_deg": NEEDS_VERIFICATION,
        "rear_angle_deg": NEEDS_VERIFICATION,
        "left_angle_deg": NEEDS_VERIFICATION,
        "right_angle_deg": NEEDS_VERIFICATION,
        "angle_tolerance_deg": NEEDS_VERIFICATION,
    },
    "background": {
        "target_color_bgr": NEEDS_VERIFICATION,
        "material": NEEDS_VERIFICATION,
        "allowed_luminance_std": NEEDS_VERIFICATION,
        "allowed_texture": "단색/무문양 배경 권장",
    },
    "floor_marker": {
        "marker_shape": NEEDS_VERIFICATION,
        "marker_color": NEEDS_VERIFICATION,
        "known_marker_length_cm": NEEDS_VERIFICATION,
        "marker_position": NEEDS_VERIFICATION,
        "purpose": "px→cm 스케일 환산 및 거리/스케일 보정 기준",
    },
    "image_qc_thresholds": {
        "subject_center_tolerance_ratio": 0.15,
        "subject_min_height_ratio": 0.45,
        "subject_edge_margin_px": 5,
        "background_max_border_std": 12.0,
        "marker_min_area_ratio": 0.0005,
        "marker_bottom_region_ratio": 0.50,
    },
}


def spec_to_markdown() -> str:
    lines = [
        "# LIGHT ONE 촬영 부스 표준 스펙",
        "",
        "실제 센터에서 실측하지 않은 물리 스펙은 [확인필요]로 유지한다.",
        "임의 수치를 넣지 않는다.",
        "",
        "## 신원 정보 정책",
        "",
        str(BOOTH_SPEC["identity_policy"]),
        "",
        "## 표준 스펙",
        "",
    ]
    lines.append("```json")
    lines.append(json.dumps(BOOTH_SPEC, ensure_ascii=False, indent=2))
    lines.append("```")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Print LIGHT ONE booth spec.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()
    if args.json:
        print(json.dumps(BOOTH_SPEC, ensure_ascii=False, indent=2))
    else:
        print(spec_to_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

