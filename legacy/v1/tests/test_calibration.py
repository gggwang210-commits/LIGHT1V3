"""Synthetic calibration tests for LIGHT ONE camera reliability utilities."""

from __future__ import annotations

import json
import os
import tempfile
import unittest

import cv2
import numpy as np

from camera_calibration.checkerboard_calibrate import (
    CalibrationResult,
    build_checkerboard_object_points,
    save_calibration,
)
from camera_calibration.reprojection_error import (
    calculate_reprojection_errors,
    classify_error,
    load_calibration,
    summarize_errors,
)
from camera_calibration.undistort import undistort_image


class CalibrationMathTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pattern_size = (9, 6)
        self.image_size = (1920, 1080)
        self.objp = build_checkerboard_object_points(self.pattern_size, 25.0)
        self.K = np.array(
            [[1400.0, 0.0, 960.0], [0.0, 1390.0, 540.0], [0.0, 0.0, 1.0]],
            dtype=np.float64,
        )
        self.D = np.array([-0.08, 0.015, 0.0005, -0.0003, 0.0], dtype=np.float64)

    def synthetic_views(self):
        object_points = []
        image_points = []
        poses = [
            ((0.05, -0.03, 0.02), (-100.0, -60.0, 900.0)),
            ((0.02, 0.04, -0.03), (-40.0, -40.0, 850.0)),
            ((-0.04, 0.02, 0.04), (20.0, -80.0, 920.0)),
            ((0.03, -0.06, 0.01), (-90.0, 20.0, 880.0)),
            ((-0.02, -0.03, -0.04), (-20.0, 10.0, 940.0)),
            ((0.04, 0.01, 0.03), (30.0, -20.0, 870.0)),
            ((-0.05, 0.05, 0.02), (-70.0, -10.0, 910.0)),
            ((0.01, -0.04, -0.02), (10.0, 30.0, 890.0)),
        ]
        for rvec_values, tvec_values in poses:
            rvec = np.asarray(rvec_values, dtype=np.float64).reshape(3, 1)
            tvec = np.asarray(tvec_values, dtype=np.float64).reshape(3, 1)
            projected, _ = cv2.projectPoints(self.objp, rvec, tvec, self.K, self.D)
            object_points.append(self.objp.astype(np.float32))
            image_points.append(projected.astype(np.float32))
        return object_points, image_points

    def test_reprojection_error_is_near_zero_for_exact_synthetic_points(self):
        object_points, image_points = self.synthetic_views()
        errors = calculate_reprojection_errors(object_points, image_points, self.K, self.D)
        self.assertLess(float(np.mean(errors)), 1e-3)
        report = summarize_errors("front", errors)
        self.assertEqual(report["status"], "PASS")

    def test_opencv_calibration_returns_usable_synthetic_intrinsics(self):
        object_points, image_points = self.synthetic_views()
        rms, K_est, D_est, _rvecs, _tvecs = cv2.calibrateCamera(
            object_points,
            image_points,
            self.image_size,
            None,
            None,
        )
        self.assertLess(float(rms), 1e-3)
        self.assertEqual(K_est.shape, (3, 3))
        self.assertGreater(float(K_est[0, 0]), 0.0)
        self.assertGreater(float(K_est[1, 1]), 0.0)
        self.assertTrue(np.all(np.isfinite(K_est)))
        self.assertTrue(np.all(np.isfinite(D_est)))

    def test_calibration_json_round_trip(self):
        result = CalibrationResult(
            camera_id="left",
            K=self.K,
            D=self.D,
            image_size=self.image_size,
            rms_error=0.123,
            image_count=8,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "left.json")
            save_calibration(result, path)
            camera_id, K, D, image_size = load_calibration(path)
        self.assertEqual(camera_id, "left")
        self.assertEqual(image_size, self.image_size)
        self.assertTrue(np.allclose(K, self.K))
        self.assertTrue(np.allclose(D.ravel(), self.D))

    def test_threshold_classification(self):
        self.assertEqual(classify_error(0.499), "PASS")
        self.assertEqual(classify_error(0.5), "CHECK")
        self.assertEqual(classify_error(0.999), "CHECK")
        self.assertEqual(classify_error(1.0), "FAIL")

    def test_undistort_preserves_image_shape(self):
        image = np.zeros((self.image_size[1], self.image_size[0], 3), dtype=np.uint8)
        corrected = undistort_image(image, self.K, self.D)
        self.assertEqual(corrected.shape, image.shape)


if __name__ == "__main__":
    unittest.main()
