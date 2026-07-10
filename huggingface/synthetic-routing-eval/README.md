---
language:
- ko
tags:
- synthetic-data
- wellness
- non-medical
---

# LIGHT ONE Synthetic Routing Evaluation Set

This folder is a local, synthetic-only evaluation asset for the LIGHT ONE
non-medical routing rule. It is not a training dataset, a medical dataset, or
a source for clinical decision-making.

## Allowed contents

- Synthetic numeric QS scores and pain levels
- Synthetic safety flags
- Expected `AUTO`, `REVIEW`, or `BLOCK` routing outcomes

## Prohibited contents

- Member names, contact details, account IDs, or free-text consultation notes
- Photos, videos, audio, posture captures, or other biometric media
- Real health, pain, exercise, sleep, or wearable records
- Production exports, database files, environment files, or API credentials

## Publication gate

Do not upload this directory to Hugging Face until the G0 gate in
[`docs/judge_risk_review.md`](../../docs/judge_risk_review.md) is satisfied
and a project owner explicitly approves a private repository. Uploading any
real member data is out of scope, including for a private repository.

The examples in `examples.jsonl` must continue to match
`lightone.utils.qs_calculator.determine_routing`. The repository test suite
enforces that contract.
