"""Run one integrated LIGHT ONE lighting quality check."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Dict, Tuple

from lighting_normalization.normalize import normalize_lighting, read_image, save_image
from lighting_normalization.uniformity_check import calculate_uniformity

SAFETY_NOTE = "Capture-quality evidence only. Use non-identifying sample frames."


def ensure_output_dir(output_dir: str) -> str:
    normalized = os.path.abspath(output_dir)
    os.makedirs(normalized, exist_ok=True)
    return normalized


def build_output_paths(input_path: str, output_dir: str) -> Tuple[str, str]:
    base_name = os.path.splitext(os.path.basename(input_path))[0] or "quality_check"
    safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in base_name)
    image_path = os.path.join(output_dir, f"{safe_name}_normalized.png")
    report_path = os.path.join(output_dir, f"{safe_name}_quality_report.json")
    return image_path, report_path


def write_json(path: str, data: Dict[str, object]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def run_quality_check(
    input_path: str,
    output_dir: str,
    grid: Tuple[int, int] = (8, 8),
    target_mean: float = 128.0,
) -> Dict[str, object]:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    absolute_output_dir = ensure_output_dir(output_dir)
    normalized_image_path, report_path = build_output_paths(input_path, absolute_output_dir)

    original = read_image(input_path)
    normalized, normalization_metrics = normalize_lighting(original, target_mean=target_mean)
    save_image(normalized_image_path, normalized)

    quality_metrics = calculate_uniformity(normalized, grid=grid)
    report: Dict[str, object] = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": os.path.abspath(input_path),
        "normalized_image_path": normalized_image_path,
        "report_path": report_path,
        "image_shape": [int(v) for v in original.shape],
        "target_mean_luminance": float(target_mean),
        "uniformity_percent": quality_metrics["uniformity_percent"],
        "shadow_ratio_percent": quality_metrics["shadow_ratio_percent"],
        "status": quality_metrics["status"],
        "recommendation": quality_metrics["recommendation"],
        "normalization": normalization_metrics,
        "quality_metrics": quality_metrics,
        "safety_note": SAFETY_NOTE,
    }
    write_json(report_path, report)
    return report


def parse_grid(value: str) -> Tuple[int, int]:
    try:
        cols, rows = value.lower().split("x", 1)
        parsed = (int(cols), int(rows))
    except Exception as exc:
        raise argparse.ArgumentTypeError("Grid must look like 8x8") from exc
    if parsed[0] <= 0 or parsed[1] <= 0:
        raise argparse.ArgumentTypeError("Grid dimensions must be positive")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a LIGHT ONE lighting quality check.")
    parser.add_argument("--input", required=True, help="Input sample image.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated files.")
    parser.add_argument("--grid", type=parse_grid, default=(8, 8), help="Grid such as 8x8.")
    parser.add_argument("--target-mean", type=float, default=128.0)
    args = parser.parse_args()

    report = run_quality_check(
        input_path=args.input,
        output_dir=args.output_dir,
        grid=args.grid,
        target_mean=args.target_mean,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
