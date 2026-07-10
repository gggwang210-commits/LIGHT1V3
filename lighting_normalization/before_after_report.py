"""Create a PNG report comparing lighting before and after normalization."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from typing import Dict, Tuple

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(tempfile.gettempdir(), "lightone_matplotlib"),
)

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    from .normalize import normalize_lighting, read_image
    from .uniformity_check import calculate_uniformity, luminance
except ImportError:
    from normalize import normalize_lighting, read_image  # type: ignore
    from uniformity_check import calculate_uniformity, luminance  # type: ignore


def histogram(luma: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    counts, bins = np.histogram(luma.ravel(), bins=256, range=(0, 255))
    return counts, bins[:-1]


def create_report(
    before: np.ndarray,
    after: np.ndarray,
    output_png: str,
    before_metrics: Dict[str, object],
    after_metrics: Dict[str, object],
) -> None:
    before_rgb = cv2.cvtColor(before, cv2.COLOR_BGR2RGB)
    after_rgb = cv2.cvtColor(after, cv2.COLOR_BGR2RGB)
    before_counts, bins = histogram(luminance(before))
    after_counts, _ = histogram(luminance(after))

    fig = plt.figure(figsize=(12, 8), dpi=140)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1.0])

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(before_rgb)
    ax0.set_title("Before")
    ax0.axis("off")

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(after_rgb)
    ax1.set_title("After")
    ax1.axis("off")

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(bins, before_counts, label="before", color="#b23a48", linewidth=1.8)
    ax2.plot(bins, after_counts, label="after", color="#2a6f97", linewidth=1.8)
    ax2.set_title("Luminance Histogram")
    ax2.set_xlabel("LAB Luminance")
    ax2.set_ylabel("Pixel Count")
    ax2.legend()
    ax2.grid(True, alpha=0.25)

    ax3 = fig.add_subplot(gs[1, 1])
    labels = ["Uniformity %", "Shadow %"]
    before_values = [
        float(before_metrics["uniformity_percent"]),
        float(before_metrics["shadow_ratio_percent"]),
    ]
    after_values = [
        float(after_metrics["uniformity_percent"]),
        float(after_metrics["shadow_ratio_percent"]),
    ]
    x = np.arange(len(labels))
    width = 0.35
    ax3.bar(x - width / 2, before_values, width, label="before", color="#b23a48")
    ax3.bar(x + width / 2, after_values, width, label="after", color="#2a6f97")
    ax3.set_xticks(x, labels)
    ax3.set_ylim(0, 100)
    ax3.set_title("Calculated Lighting Quality")
    ax3.legend()
    ax3.grid(axis="y", alpha=0.25)

    title = (
        "Lighting Normalization Report\n"
        f"Before: {before_metrics['status']} / After: {after_metrics['status']}"
    )
    fig.suptitle(title, fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.94])

    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    fig.savefig(output_png)
    plt.close(fig)


def write_json(path: str, data: Dict[str, object]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create before/after lighting report PNG.")
    parser.add_argument("--input", required=True, help="Input gray-card/lighting image.")
    parser.add_argument("--output-png", required=True, help="Report PNG path.")
    parser.add_argument("--output-json", help="Optional report metrics JSON path.")
    parser.add_argument("--target-mean", type=float, default=128.0)
    parser.add_argument("--grid", default="8x8", help="Uniformity grid, e.g. 8x8.")
    args = parser.parse_args()

    grid_parts = args.grid.lower().split("x", 1)
    grid = (int(grid_parts[0]), int(grid_parts[1]))

    before = read_image(args.input)
    after, normalization_metrics = normalize_lighting(before, target_mean=args.target_mean)
    before_metrics = calculate_uniformity(before, grid=grid)
    after_metrics = calculate_uniformity(after, grid=grid)
    create_report(before, after, args.output_png, before_metrics, after_metrics)

    report = {
        "normalization": normalization_metrics,
        "before": before_metrics,
        "after": after_metrics,
        "note": "Calculated from lighting patch/gray-card image only; no identity data used.",
    }
    if args.output_json:
        write_json(args.output_json, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
