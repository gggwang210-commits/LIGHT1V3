"""Quantify lighting uniformity and shadow ratio.

All reported numbers are calculated from the input image. If lighting evidence
images are missing, the caller must capture gray-card or lighting patch data.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, Tuple

import cv2
import numpy as np


PASS_THRESHOLD = 90.0
FAIL_THRESHOLD = 80.0


def luminance(image: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    return lab[:, :, 0].astype(np.float32)


def grid_cell_means(luma: np.ndarray, grid: Tuple[int, int] = (8, 8)) -> np.ndarray:
    cols, rows = grid
    if cols <= 0 or rows <= 0:
        raise ValueError("Grid dimensions must be positive.")

    h, w = luma.shape
    cell_means = []
    for row in range(rows):
        y0 = int(round(row * h / rows))
        y1 = int(round((row + 1) * h / rows))
        for col in range(cols):
            x0 = int(round(col * w / cols))
            x1 = int(round((col + 1) * w / cols))
            cell = luma[y0:y1, x0:x1]
            if cell.size == 0:
                continue
            cell_means.append(float(cell.mean()))
    return np.asarray(cell_means, dtype=np.float64)


def classify_uniformity(uniformity_percent: float) -> Tuple[str, str]:
    if uniformity_percent >= PASS_THRESHOLD:
        return "PASS", "Lighting uniformity acceptable."
    if uniformity_percent < FAIL_THRESHOLD:
        return "FAIL", "Retake recommended: lighting is not uniform enough."
    return "CHECK", "Retake recommended if measurement repeatability is critical."


def calculate_uniformity(
    image: np.ndarray,
    grid: Tuple[int, int] = (8, 8),
    shadow_luma_threshold: float = 50.0,
    shadow_relative_threshold: float = 0.55,
) -> Dict[str, object]:
    """Return uniformity percentage and shadow ratio for a frame."""
    luma = luminance(image)
    cells = grid_cell_means(luma, grid)
    if cells.size == 0:
        raise ValueError("Data required: image is too small for uniformity analysis.")

    min_cell = float(cells.min())
    max_cell = float(cells.max())
    mean_cell = float(cells.mean())
    uniformity = 100.0 * min_cell / max(max_cell, 1e-6)

    frame_mean = float(luma.mean())
    shadow_threshold = max(
        float(shadow_luma_threshold),
        frame_mean * float(shadow_relative_threshold),
    )
    shadow_ratio = 100.0 * float(np.mean(luma < shadow_threshold))
    status, recommendation = classify_uniformity(uniformity)
    if status == "PASS" and shadow_ratio > 10.0:
        status = "CHECK"
        recommendation = "Retake recommended if shadow ratio affects marker detection."

    return {
        "uniformity_percent": float(uniformity),
        "shadow_ratio_percent": float(shadow_ratio),
        "grid": [int(grid[0]), int(grid[1])],
        "cell_mean_min": min_cell,
        "cell_mean_max": max_cell,
        "cell_mean_avg": mean_cell,
        "frame_mean_luminance": frame_mean,
        "shadow_luma_threshold_used": float(shadow_threshold),
        "status": status,
        "recommendation": recommendation,
    }


def read_image(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def parse_grid(value: str) -> Tuple[int, int]:
    try:
        x, y = value.lower().split("x", 1)
        return int(x), int(y)
    except Exception as exc:
        raise argparse.ArgumentTypeError("Grid must look like 8x8") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Check lighting uniformity.")
    parser.add_argument("--input", required=True, help="Input gray-card/lighting image.")
    parser.add_argument("--output", help="Optional JSON report path.")
    parser.add_argument("--grid", type=parse_grid, default=(8, 8))
    parser.add_argument("--shadow-luma-threshold", type=float, default=50.0)
    parser.add_argument("--shadow-relative-threshold", type=float, default=0.55)
    args = parser.parse_args()

    report = calculate_uniformity(
        read_image(args.input),
        grid=args.grid,
        shadow_luma_threshold=args.shadow_luma_threshold,
        shadow_relative_threshold=args.shadow_relative_threshold,
    )
    text = json.dumps(report, indent=2)
    print(text)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

