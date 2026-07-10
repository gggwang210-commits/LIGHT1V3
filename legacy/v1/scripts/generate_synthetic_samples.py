"""Generate synthetic LIGHT ONE sample images for local checks."""

from __future__ import annotations

import argparse
import os

import cv2
import numpy as np


def synthetic_uniform_graycard(width: int = 320, height: int = 240) -> np.ndarray:
    return np.full((height, width, 3), 128, dtype=np.uint8)


def synthetic_biased_lighting_patch(width: int = 320, height: int = 240) -> np.ndarray:
    base = np.full((height, width, 3), 150, dtype=np.float32)
    base[:, :, 0] *= 1.30
    base[:, :, 1] *= 0.95
    base[:, :, 2] *= 0.75

    gradient = np.linspace(0.60, 1.18, width, dtype=np.float32).reshape(1, width, 1)
    image = base * gradient

    yy, xx = np.mgrid[0:height, 0:width]
    shadow = ((xx - 95) ** 2 / (85**2) + (yy - 150) ** 2 / (65**2)) < 1.0
    image[shadow] *= 0.45
    return np.clip(image, 0, 255).astype(np.uint8)


def write_image(path: str, image: np.ndarray) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if not cv2.imwrite(path, image):
        raise ValueError(f"Could not write image: {path}")


def generate_samples(output_dir: str) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    outputs = [
        os.path.join(output_dir, "synthetic_uniform_graycard.png"),
        os.path.join(output_dir, "synthetic_biased_lighting_patch.png"),
    ]
    write_image(outputs[0], synthetic_uniform_graycard())
    write_image(outputs[1], synthetic_biased_lighting_patch())
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic LIGHT ONE samples.")
    parser.add_argument("--output-dir", default="data/synthetic")
    args = parser.parse_args()
    outputs = generate_samples(args.output_dir)
    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
