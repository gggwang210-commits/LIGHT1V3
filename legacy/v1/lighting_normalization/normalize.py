"""Normalize lighting variation before image measurement.

The LIGHT ONE workflow uses this module to reduce color temperature, brightness,
and local contrast differences for repeatable reference measurements. Inputs are
lighting patches, gray cards, or marker frames, not face or identity images.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, Tuple

import cv2
import numpy as np


def read_image(path: str) -> np.ndarray:
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def gray_world_white_balance(image: np.ndarray) -> np.ndarray:
    """Apply gray-world white balance to a BGR image."""
    image_f = image.astype(np.float32)
    channel_means = image_f.reshape(-1, 3).mean(axis=0)
    gray_mean = float(channel_means.mean())
    gains = gray_mean / np.maximum(channel_means, 1e-6)
    balanced = image_f * gains.reshape(1, 1, 3)
    return np.clip(balanced, 0, 255).astype(np.uint8)


def clahe_luminance(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Normalize local contrast using CLAHE on LAB luminance."""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_equalized = clahe.apply(l_channel)
    merged = cv2.merge([l_equalized, a_channel, b_channel])
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def normalize_exposure(image: np.ndarray, target_mean: float = 128.0) -> np.ndarray:
    """Scale exposure so the luminance mean maps to target_mean."""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB).astype(np.float32)
    current_mean = float(lab[:, :, 0].mean())
    if current_mean <= 1e-6:
        return image.copy()
    scale = float(target_mean) / current_mean
    lab[:, :, 0] = np.clip(lab[:, :, 0] * scale, 0, 255)
    return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)


def normalize_lighting(
    image: np.ndarray,
    target_mean: float = 128.0,
    clahe_clip_limit: float = 2.0,
    clahe_grid_size: Tuple[int, int] = (8, 8),
) -> Tuple[np.ndarray, Dict[str, object]]:
    """Run white balance, CLAHE, and exposure normalization."""
    before_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    before_channel_means = image.reshape(-1, 3).mean(axis=0)

    balanced = gray_world_white_balance(image)
    contrasted = clahe_luminance(
        balanced,
        clip_limit=clahe_clip_limit,
        tile_grid_size=clahe_grid_size,
    )
    normalized = normalize_exposure(contrasted, target_mean=target_mean)

    after_lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)
    after_channel_means = normalized.reshape(-1, 3).mean(axis=0)
    metadata: Dict[str, object] = {
        "target_mean_luminance": float(target_mean),
        "before_mean_luminance": float(before_lab[:, :, 0].mean()),
        "after_mean_luminance": float(after_lab[:, :, 0].mean()),
        "before_bgr_means": [float(v) for v in before_channel_means],
        "after_bgr_means": [float(v) for v in after_channel_means],
        "clahe_clip_limit": float(clahe_clip_limit),
        "clahe_grid_size": [int(v) for v in clahe_grid_size],
        "note": "Lighting/gray-card inputs only; faces and identity data are not processed.",
    }
    return normalized, metadata


def save_image(path: str, image: np.ndarray) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not cv2.imwrite(path, image):
        raise ValueError(f"Could not write image: {path}")


def parse_grid(value: str) -> Tuple[int, int]:
    try:
        x, y = value.lower().split("x", 1)
        return int(x), int(y)
    except Exception as exc:
        raise argparse.ArgumentTypeError("Grid must look like 8x8") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize lighting in a BGR image.")
    parser.add_argument("--input", required=True, help="Input gray-card/lighting image.")
    parser.add_argument("--output", required=True, help="Normalized output image path.")
    parser.add_argument("--metrics", help="Optional JSON metrics output path.")
    parser.add_argument("--target-mean", type=float, default=128.0)
    parser.add_argument("--clahe-clip-limit", type=float, default=2.0)
    parser.add_argument("--clahe-grid-size", type=parse_grid, default=(8, 8))
    args = parser.parse_args()

    image = read_image(args.input)
    normalized, metrics = normalize_lighting(
        image,
        target_mean=args.target_mean,
        clahe_clip_limit=args.clahe_clip_limit,
        clahe_grid_size=args.clahe_grid_size,
    )
    save_image(args.output, normalized)
    if args.metrics:
        os.makedirs(os.path.dirname(os.path.abspath(args.metrics)), exist_ok=True)
        with open(args.metrics, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

