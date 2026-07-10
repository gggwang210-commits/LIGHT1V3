"""Tests for lighting normalization using synthetic gray-card images only."""

from __future__ import annotations

import os
import tempfile
import unittest

import cv2
import numpy as np

from lighting_normalization.before_after_report import create_report
from lighting_normalization.normalize import gray_world_white_balance, normalize_lighting
from lighting_normalization.uniformity_check import (
    calculate_uniformity,
    classify_uniformity,
)


def synthetic_biased_shadow_image(width: int = 320, height: int = 240) -> np.ndarray:
    base = np.full((height, width, 3), 150, dtype=np.float32)
    base[:, :, 0] *= 1.35
    base[:, :, 1] *= 0.92
    base[:, :, 2] *= 0.72

    x = np.linspace(0.55, 1.15, width, dtype=np.float32).reshape(1, width, 1)
    image = base * x

    yy, xx = np.mgrid[0:height, 0:width]
    shadow = ((xx - 95) ** 2 / (85**2) + (yy - 150) ** 2 / (65**2)) < 1.0
    image[shadow] *= 0.45
    return np.clip(image, 0, 255).astype(np.uint8)


class LightingNormalizationTest(unittest.TestCase):
    def test_gray_world_reduces_channel_bias(self):
        image = synthetic_biased_shadow_image()
        before_means = image.reshape(-1, 3).mean(axis=0)
        after = gray_world_white_balance(image)
        after_means = after.reshape(-1, 3).mean(axis=0)
        before_spread = float(before_means.max() - before_means.min())
        after_spread = float(after_means.max() - after_means.min())
        self.assertLess(after_spread, before_spread * 0.25)

    def test_normalization_moves_luminance_toward_target(self):
        image = synthetic_biased_shadow_image()
        normalized, metrics = normalize_lighting(image, target_mean=128.0)
        self.assertEqual(normalized.shape, image.shape)
        self.assertLess(abs(float(metrics["after_mean_luminance"]) - 128.0), 2.0)

    def test_uniformity_and_shadow_metrics_are_calculated(self):
        image = synthetic_biased_shadow_image()
        report = calculate_uniformity(image, grid=(8, 6))
        self.assertGreaterEqual(report["uniformity_percent"], 0.0)
        self.assertLessEqual(report["uniformity_percent"], 100.0)
        self.assertGreater(report["shadow_ratio_percent"], 0.0)
        self.assertIn(report["status"], {"PASS", "CHECK", "FAIL"})

    def test_uniform_gray_patch_passes(self):
        image = np.full((120, 160, 3), 128, dtype=np.uint8)
        report = calculate_uniformity(image, grid=(4, 3))
        self.assertGreaterEqual(report["uniformity_percent"], 90.0)
        self.assertEqual(report["status"], "PASS")

    def test_threshold_classification(self):
        self.assertEqual(classify_uniformity(90.0)[0], "PASS")
        self.assertEqual(classify_uniformity(80.0)[0], "CHECK")
        self.assertEqual(classify_uniformity(79.99)[0], "FAIL")

    def test_before_after_report_png_is_written(self):
        image = synthetic_biased_shadow_image(160, 120)
        normalized, _metrics = normalize_lighting(image)
        before_metrics = calculate_uniformity(image, grid=(4, 3))
        after_metrics = calculate_uniformity(normalized, grid=(4, 3))
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.png")
            create_report(image, normalized, path, before_metrics, after_metrics)
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 0)


if __name__ == "__main__":
    unittest.main()

