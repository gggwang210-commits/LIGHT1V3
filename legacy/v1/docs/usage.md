# Usage

```bash
python -m unittest discover -s tests
```

```bash
python scripts/generate_synthetic_samples.py --output-dir data/synthetic
```

```bash
python -m quality_pipeline.run_quality_check --input data/synthetic/synthetic_biased_lighting_patch.png --output-dir reports
```
