"""Tests for the integrated LIGHT ONE quality pipeline."""

from __future__ import annotations

import os
import tempfile
import unittest

import cv2
import numpy as np

from quality_pipeline.run_quality_check import run_quality_check


def synthetic_sample(width: int = 160, height: int = 120) -> np.ndarray:
    image = np.full((height, width, 3), 150, dtype=np.float32)
    gradient = np.linspace(0.70, 1.12, width, dtype=np.float32).reshape(1, width, 1)
    image *= gradient
    return np.clip(image, 0, 255).astype(np.uint8)


class QualityPipelineTest(unittest.TestCase):
    def test_pipeline_writes_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "sample.png")
            output_dir = os.path.join(tmpdir, "reports")
            cv2.imwrite(input_path, synthetic_sample())

            report = run_quality_check(input_path=input_path, output_dir=output_dir, grid=(4, 3))

            self.assertTrue(os.path.exists(report["normalized_image_path"]))
            self.assertTrue(os.path.exists(report["report_path"]))
            self.assertIn(report["status"], {"PASS", "CHECK", "FAIL"})
            self.assertGreaterEqual(float(report["uniformity_percent"]), 0.0)
            self.assertLessEqual(float(report["uniformity_percent"]), 100.0)

    def test_pipeline_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(FileNotFoundError):
                run_quality_check(input_path=os.path.join(tmpdir, "missing.png"), output_dir=tmpdir)


if __name__ == "__main__":
    unittest.main()
