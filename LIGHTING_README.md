# LIGHT ONE Lighting Normalization

This module normalizes lighting variation and calculates numerical quality evidence for LIGHT ONE measurement frames. It is intended for lighting patches, gray cards, and marker frames only. It does not process human faces or identity information.

All reported values are calculated from the supplied image. If no real image is provided, the system must say that data is required rather than inventing a benchmark.

## Folder Structure

```text
lighting_normalization/
  __init__.py
  normalize.py
  uniformity_check.py
  before_after_report.py
tests/
  test_lighting.py
requirements.txt
LIGHTING_README.md
```

## Install

```bash
python -m pip install -r requirements.txt
```

Allowed packages are `opencv-python`, `numpy`, and `matplotlib`.

## Normalize Lighting

```bash
python -m lighting_normalization.normalize --input data/graycard/session_001.jpg --output reports/session_001_normalized.jpg --metrics reports/session_001_normalized.json
```

The pipeline applies:

```text
1. Gray-world white balance
2. CLAHE local contrast normalization on LAB luminance
3. Exposure normalization to a target mean luminance
```

## Check Uniformity

```bash
python -m lighting_normalization.uniformity_check --input reports/session_001_normalized.jpg --output reports/session_001_uniformity.json --grid 8x8
```

Judgement:

```text
uniformity >= 90% => PASS
80% to < 90%     => CHECK, 재촬영 권고 가능
uniformity < 80%  => FAIL, 재촬영 권고
```

Uniformity is calculated as:

```text
100 * darkest grid-cell mean luminance / brightest grid-cell mean luminance
```

Shadow ratio is the percentage of pixels below the calculated shadow threshold. The threshold is the larger value of an absolute LAB luminance threshold and a relative threshold based on the frame mean.

## Before/After PNG Report

```bash
python -m lighting_normalization.before_after_report --input data/graycard/session_001.jpg --output-png reports/session_001_lighting_report.png --output-json reports/session_001_lighting_report.json
```

The PNG contains:

```text
before image
after image
luminance histogram comparison
uniformity and shadow-ratio comparison
```

## Tests

```bash
python -m unittest discover -s tests
```

The tests use synthetic gray-card images with artificial color bias and shadow. They verify the code path and correction behavior, but real center reliability evidence requires actual lighting patch or gray-card images from each capture setup.

## Interview Explanation Points

1. We first make the image color balance and average brightness consistent, so the same marker is seen under the same numerical conditions.
2. We divide the frame into a grid and calculate whether one area is much darker than another, so shadows are judged by numbers instead of by eye.
3. If the normalized frame passes the uniformity threshold, measurement variation from lighting is controlled; if it fails, the system recommends retaking before trusting the posture reference value.
