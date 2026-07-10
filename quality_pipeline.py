"""Integrated capture-quality pipeline for LIGHT ONE.

This CLI combines lighting normalization and lighting-uniformity reporting for
safe capture-quality verification before downstream posture-reference analysis.
Use lighting patches, gray-card images, or marker frames only. Do not use real
user body images, face images, private health data, credentials, or API keys.

The output is quality evidence for capture conditions only. It is not medical
advice, diagnosis, disease prediction, or treatment-effect evaluation.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, Tuple

from lighting_normalization.normalize import normalize_lighting, read_image, save_image
from lighting_normalization.uniformity_check import calculate_uniformity, parse_grid

SAFETY_NOTICE = (
    "Use lighting patches, gray-card images, or marker frames only. "
    "Do not use real user body images, face images, private health data, "
    "credentials, or API keys. This pipeline reports capture-quality evidence "
    "only and does not provide medical judgment."
)


def ensure_parent_dir(path: str) -> None:
    """Create a parent directory for a file path when needed."""
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def build_quality_report(
    input_path: str,
    normalized_output_path: str,
    grid: Tuple[int, int],
    target_mean: float,
    clahe_clip_limit: float,
    clahe_grid_size: Tuple[int, int],
    shadow_luma_threshold: float,
    shadow_relative_threshold: float,
) -> Dict[str, object]:
    """Run lighting normalization and uniformity analysis."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            "Input image not found. Provide a synthetic image, gray-card image, "
            "lighting patch, or marker frame. Do not use real user or face images."
        )

    image = read_image(input_path)
    normalized, normalization_metrics = normalize_lighting(
        image,
        target_mean=target_mean,
        clahe_clip_limit=clahe_clip_limit,
        clahe_grid_size=clahe_grid_size,
    )
    save_image(normalized_output_path, normalized)

    uniformity_metrics = calculate_uniformity(
        normalized,
        grid=grid,
        shadow_luma_threshold=shadow_luma_threshold,
        shadow_relative_threshold=shadow_relative_threshold,
    )

    return {
        "pipeline": "LIGHT ONE integrated capture-quality pipeline",
        "input_path": input_path,
        "normalized_output_path": normalized_output_path,
        "safety_notice": SAFETY_NOTICE,
        "normalization_metrics": normalization_metrics,
        "uniformity_metrics": uniformity_metrics,
        "interpretation_boundary": (
            "Results are capture-quality evidence for lighting consistency only. "
            "They do not assess health status, posture diagnosis, disease risk, "
            "or treatment effect."
        ),
    }


def write_json_report(path: str, report: Dict[str, object]) -> None:
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run LIGHT ONE integrated capture-quality checks."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input synthetic image, gray-card image, lighting patch, or marker frame.",
    )
    parser.add_argument(
        "--normalized-output",
        required=True,
        help="Path for the normalized output image.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Path for the integrated JSON quality report.",
    )
    parser.add_argument("--grid", type=parse_grid, default=(8, 8))
    parser.add_argument("--target-mean", type=float, default=128.0)
    parser.add_argument("--clahe-clip-limit", type=float, default=2.0)
    parser.add_argument("--clahe-grid-size", type=parse_grid, default=(8, 8))
    parser.add_argument("--shadow-luma-threshold", type=float, default=50.0)
    parser.add_argument("--shadow-relative-threshold", type=float, default=0.55)
    args = parser.parse_args()

    print(SAFETY_NOTICE)
    report = build_quality_report(
        input_path=args.input,
        normalized_output_path=args.normalized_output,
        grid=args.grid,
        target_mean=args.target_mean,
        clahe_clip_limit=args.clahe_clip_limit,
        clahe_grid_size=args.clahe_grid_size,
        shadow_luma_threshold=args.shadow_luma_threshold,
        shadow_relative_threshold=args.shadow_relative_threshold,
    )
    write_json_report(args.report, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
