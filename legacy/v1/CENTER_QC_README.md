# LIGHT ONE Center QC

This module defines a shooting booth specification and an automatic QC gate for repeatable LIGHT ONE capture. The QC gate checks only composition, background control, and floor reference marker presence. It does not save identity information or analyze faces.

Physical booth values are intentionally marked `[확인필요]` until measured at the real center. Do not replace them with guesses.

## Folder Structure

```text
center_qc/
  __init__.py
  booth_spec.py
  qc_gate.py
  scale_reference.py
tests/
  test_qc.py
requirements.txt
CENTER_QC_README.md
```

## Dependencies

The `center_qc` module uses only:

```text
opencv-python
numpy
```

## Shooting SOP Checklist

Before capture:

```text
[ ] Camera body/lens fixed: Canon EOS R7 + RF 35mm F1.8
[ ] Camera height: [확인필요]
[ ] Subject-to-camera distance: [확인필요]
[ ] Front/rear/left/right camera angles: [확인필요]
[ ] Background color/material: [확인필요]
[ ] Floor marker real length in cm: [확인필요]
[ ] Floor marker position: [확인필요]
[ ] Marker is visible in the bottom region of the frame
[ ] Subject stands on the center floor mark
[ ] Full body is inside the frame
[ ] Background is single-color and not patterned
[ ] QC gate returns PASS before posture measurement proceeds
```

## Print Booth Spec

```bash
python -m center_qc.booth_spec
python -m center_qc.booth_spec --json
```

The printed spec keeps unmeasured physical values as `[확인필요]`.

## Run QC Gate

```bash
python -m center_qc.qc_gate --input data/session_001/qc_frame.jpg --output reports/session_001_qc.json
```

The gate checks:

```text
1. 피험자가 프레임 중앙에 있고 전신이 포함되는지
2. 배경이 단색으로 통제되어 있는지
3. 거리/스케일 보정용 바닥 기준 마커가 보이는지
```

If any check fails, the JSON message starts with `다시 촬영하세요` and explains the failed item in Korean.

## Estimate px to cm Scale

```bash
python -m center_qc.scale_reference --input data/session_001/qc_frame.jpg --marker-length-cm 60 --output reports/session_001_scale.json
```

`--marker-length-cm` must be the real measured marker length. If the real marker length is not known, data is required and the value must not be guessed.

## Tests

```bash
python -m unittest discover -s tests
```

The tests use synthetic standard and non-standard booth images. They do not use human identity images.

## Interview Explanation Points

1. We wrote the booth conditions as a checklist, and unknown physical numbers are left as `[확인필요]` until the center measures them.
2. Before measurement, the software checks whether the person is centered, fully visible, on a controlled background, and captured with a visible floor marker.
3. If any condition is outside the standard, the system says why and asks for retake, so different operators produce comparable images.
