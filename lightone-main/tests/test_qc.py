"""Synthetic tests for booth QC gate without identity images."""

from __future__ import annotations

import unittest

import cv2
import numpy as np

from center_qc.booth_spec import BOOTH_SPEC, NEEDS_VERIFICATION
from center_qc.qc_gate import run_qc_gate
from center_qc.scale_reference import (
    correct_px_measurement,
    detect_floor_marker,
    estimate_scale_from_marker,
)


def synthetic_booth(
    width: int = 400,
    height: int = 600,
    subject_center_x: int | None = None,
    crop_subject: bool = False,
    textured_background: bool = False,
    include_marker: bool = True,
    subject_height: int = 420,
) -> np.ndarray:
    image = np.full((height, width, 3), 190, dtype=np.uint8)
    if textured_background:
        for x in range(0, width, 20):
            color = 150 if (x // 20) % 2 == 0 else 215
            image[:, x : x + 10] = color

    cx = subject_center_x if subject_center_x is not None else width // 2
    body_w = 82
    top = 70
    bottom = top + subject_height
    if crop_subject:
        top = 0
        bottom = height - 1
    cv2.rectangle(
        image,
        (cx - body_w // 2, top),
        (cx + body_w // 2, bottom),
        (45, 45, 45),
        -1,
    )
    cv2.circle(image, (cx, max(25, top - 28)), 28, (45, 45, 45), -1)

    if include_marker:
        cv2.rectangle(
            image,
            (width // 2 - 60, height - 55),
            (width // 2 + 60, height - 35),
            (0, 210, 0),
            -1,
        )
    return image


class CenterQcTest(unittest.TestCase):
    def test_unknown_physical_specs_are_marked_for_verification(self):
        camera = BOOTH_SPEC["camera"]
        subject_position = BOOTH_SPEC["subject_position"]
        layout = BOOTH_SPEC["four_direction_layout"]
        self.assertEqual(camera["camera_height_cm"], NEEDS_VERIFICATION)
        self.assertEqual(subject_position["subject_to_camera_distance_cm"], NEEDS_VERIFICATION)
        self.assertEqual(layout["front_angle_deg"], NEEDS_VERIFICATION)

    def test_standard_synthetic_image_passes_qc(self):
        report = run_qc_gate(synthetic_booth())
        self.assertTrue(report["pass"], report["message"])
        self.assertEqual(report["status"], "PASS")

    def test_off_center_subject_fails(self):
        report = run_qc_gate(synthetic_booth(subject_center_x=90))
        self.assertFalse(report["pass"])
        self.assertIn("프레임 중앙", report["message"])

    def test_cropped_subject_fails(self):
        report = run_qc_gate(synthetic_booth(crop_subject=True))
        self.assertFalse(report["pass"])
        self.assertIn("프레임 가장자리", report["message"])

    def test_textured_background_fails(self):
        report = run_qc_gate(synthetic_booth(textured_background=True))
        self.assertFalse(report["pass"])
        self.assertIn("배경", report["message"])

    def test_missing_marker_fails(self):
        report = run_qc_gate(synthetic_booth(include_marker=False))
        self.assertFalse(report["pass"])
        self.assertIn("바닥 기준 마커", report["message"])

    def test_floor_marker_scale_conversion(self):
        image = synthetic_booth()
        marker = detect_floor_marker(image)
        self.assertIsNotNone(marker)
        scale = estimate_scale_from_marker(image, marker_real_length_cm=60.0)
        self.assertAlmostEqual(scale["marker"]["pixel_length"], 120.0, delta=2.0)
        self.assertAlmostEqual(scale["cm_per_px"], 0.5, delta=0.02)
        self.assertAlmostEqual(correct_px_measurement(100.0, scale["cm_per_px"]), 50.0, delta=2.0)


if __name__ == "__main__":
    unittest.main()

