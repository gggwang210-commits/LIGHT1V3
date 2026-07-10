# Repository Map

## Root

- `README.md`: project definition, non-medical positioning, technical-module overview
- `index.html`: static landing page with inline CSS and no external JavaScript dependency
- `requirements.txt`: Python dependencies for technical modules
- `.gitignore`: excludes local environment and build artifacts, including `.env`
- `.env.example`: non-secret environment template

## Technical modules

- `camera_calibration/`: checkerboard calibration and reprojection utilities
- `lighting_normalization/`: lighting normalization and uniformity checks
- `center_qc/`: center/booth quality-gate utilities
- `quality_pipeline/`: combined quality-check pipeline
- `scripts/generate_synthetic_samples.py`: synthetic sample generation helper
- `tests/`: pytest coverage for calibration, lighting, QC, and pipeline behavior

## Documentation

- `docs/governance/non-medical-boundary.md`: prohibited wording and non-medical disclaimer
- `docs/governance/privacy-checklist.md`: privacy readiness checklist
- `docs/validation/pilot-validation-plan.md`: pilot validation plan and non-claims
- `docs/submission/modu-startup-summary.md`: concise external-submission summary
- `docs/execution-guide/windows-run-guide.md`: Windows PowerShell run instructions
