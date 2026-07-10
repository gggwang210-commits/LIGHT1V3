# LIGHT ONE Portfolio Summary

## One-Line Description

LIGHT ONE is a Python-based capture-quality verification module that checks camera distortion and lighting consistency before downstream AI posture-reference analysis.

## Project Positioning

LIGHT ONE is not a completed consumer service yet. It is the first reliability layer for an AI posture and body-reference analysis project.

The current repository focuses on the question:

> Can the input image be trusted enough before running posture or body-reference analysis?

To answer that, the project calculates measurable evidence from calibration and lighting images.

## Implemented Scope

### 1. Camera Calibration

Implemented in:

```text
camera_calibration/
```

What it does:

- Uses checkerboard images for camera calibration
- Calculates camera intrinsic matrix and distortion coefficients
- Measures reprojection error
- Classifies quality as `PASS`, `CHECK`, or `FAIL`
- Generates before/after undistortion comparison images

Why it matters:

Camera distortion can affect posture-angle or marker-position measurements. Calibration provides numerical evidence that the camera geometry is controlled.

### 2. Lighting Normalization

Implemented in:

```text
lighting_normalization/
```

What it does:

- Applies white-balance correction
- Normalizes luminance and contrast
- Calculates lighting uniformity
- Calculates shadow ratio
- Generates PNG and JSON reports

Why it matters:

Uneven lighting and shadows can reduce the reliability of marker detection or image-based analysis. LIGHT ONE checks lighting quality before relying on the frame.

### 3. Tests

Implemented in:

```text
tests/
```

What it checks:

- Synthetic calibration behavior
- Synthetic lighting-normalization behavior
- Output shape and report generation
- Quality-threshold classification logic

Limit:

Synthetic tests prove the code path, not real-world camera performance. Real validation requires actual checkerboard, gray-card, or lighting-patch images from the intended capture setup.

## Not Implemented Yet

These features are future plans and should not be presented as completed:

- Web UI
- Backend API
- Real pose-estimation model integration
- Real body-shape analysis model
- User image upload service
- Login or account system
- Database storage
- Payment system
- Cloud deployment
- Docker deployment

## Safe Portfolio Explanation

Use this wording:

> AI posture analysis depends heavily on input-image quality. In LIGHT ONE, I implemented a preprocessing and quality-verification layer that calculates lighting uniformity, shadow ratio, camera distortion, and reprojection error before downstream analysis.

Avoid this wording:

- This diagnoses posture problems
- This predicts disease
- This evaluates treatment effect
- This is a medical AI service
- This fully analyzes body shape

Better alternatives:

- Posture reference information
- Exercise-coaching support
- Capture-quality verification
- Preprocessing for body-reference analysis
- Measurement-reliability support

## Technical Strengths

This project demonstrates:

- Python module structure
- OpenCV image preprocessing
- Camera calibration workflow
- Quantitative quality metrics
- JSON and PNG report generation
- Testable image-processing logic
- Health-related expression risk control

## Recommended Interview Answer

> I noticed that posture-analysis results can become unreliable when the camera or lighting condition is poor. So instead of starting with a large AI model immediately, I first built a quality-verification layer. LIGHT ONE calculates camera reprojection error, distortion correction, lighting uniformity, and shadow ratio. This makes the project more realistic because it checks whether the input condition is reliable before trying to interpret posture.

## Next Development Roadmap

Recommended order:

1. Add an integrated quality-check pipeline that combines camera and lighting reports
2. Add sample synthetic data and CLI examples
3. Add a Colab demo notebook for presentation
4. Add a small FastAPI wrapper after the pipeline is stable
5. Experiment with pose estimation separately
6. Add privacy and safety documentation before handling real user images

## Human Review Checklist

Before presenting this project, check:

- README does not claim unimplemented features
- No medical diagnosis or treatment-effect language is used
- No real user image is committed
- `.env` is not committed
- Tests run successfully with `python -m unittest discover -s tests`
- Generated reports are treated as local outputs unless intentionally documented
