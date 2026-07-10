# Trainer Dashboard Validation

## 1. Purpose

This document defines how the LIGHT ONE trainer dashboard MVP should be reviewed by public-sector evaluators, early investors, enterprise PoC reviewers, and pilot fitness-center operators.

The dashboard is not a medical product screen. It is a non-medical PT coaching operations screen that helps trainers review member session records, QS/JATC reference scores, pain response records, capture QC status, and AUTO/REVIEW/BLOCK routing before communicating with a member.

## 2. Primary User

The first validation user is a premium PT center trainer or center owner who already manages recurring PT sessions and needs a clearer way to:

- prepare for today's sessions
- find REVIEW/BLOCK cases before member communication
- check QS/JATC reference scores without treating them as final decisions
- review discomfort response and RPE records
- decide what the trainer must verify before sending a report

## 3. Validation Hypothesis

The trainer dashboard is valuable if it helps a trainer reduce missed review cases and prepare member communication faster without creating medical-device misunderstanding.

The MVP should validate these hypotheses:

| Hypothesis | What to observe | Pass signal |
|---|---|---|
| Trainers understand the review queue | Trainer can explain why REVIEW/BLOCK cases appear | Trainer identifies review reasons without external explanation |
| Trainers trust the safety boundary | Trainer understands that routing is a review priority, not a diagnosis | Trainer uses "check", "review", "record", or "coaching reference" language |
| The workflow is actionable | Trainer knows the next action for AUTO, REVIEW, and BLOCK | Trainer can choose whether to draft, review, or pause a session flow |
| The screen supports sales conversation | Center owner sees how this can support retention or feedback quality | Owner can name a pilot use case within one session |

## 4. Demo Scenario

Use synthetic demo data only.

1. Open the trainer console at `/lightone/trainer/`.
2. Start with the summary cards: today sessions, average QS, REVIEW/BLOCK count, pending confirmations.
3. Review the REVIEW/BLOCK queue.
4. For each queue item, explain the check items: discomfort response, RPE, QC status, QS/JATC.
5. Explain next actions:
   - AUTO: trainer may review the report draft before delivery.
   - REVIEW: trainer checks exercise range, difficulty, rest, and message wording.
   - BLOCK: trainer pauses the session flow and checks whether professional consultation guidance is needed.
6. Open one report preview only if the reviewer asks for session-level detail.

## 5. Success Criteria

The MVP passes validation when:

- a trainer can explain the dashboard workflow within 3 minutes
- REVIEW/BLOCK cases are visible without searching through a member list
- no UI copy implies diagnosis, treatment, prescription, rehabilitation treatment, disease prediction, injury prediction, or pain cause confirmation
- a reviewer can distinguish the trainer console from a marketing landing page
- the dashboard uses only synthetic/demo records in public review
- automated tests confirm the trainer dashboard renders and includes non-medical review language

## 6. Negative Scope

This validation does not include:

- medical diagnosis
- treatment recommendation
- exercise prescription as a medical claim
- rehabilitation treatment workflow
- pain cause analysis or confirmation
- injury or disease prediction
- real member data upload
- Hugging Face dataset/model publication
- payment, reservation, or CRM automation
- automated member delivery without trainer review

## 7. Evaluation Checklist

| Area | Question | Required answer |
|---|---|---|
| Positioning | Is this clearly a non-medical wellness/PT coaching support screen? | Yes |
| Workflow | Can the trainer find the next review action quickly? | Yes |
| Safety | Are AUTO/REVIEW/BLOCK described as review priority states? | Yes |
| Data | Is only synthetic or demo data used? | Yes |
| Investor readiness | Does the screen show an actual operating workflow, not only concept slides? | Yes |
| Enterprise readiness | Is there a clear path to audit, permissions, and review history later? | Yes, but not in this MVP |

## 8. Evidence From Current Implementation

Current implementation evidence:

- `/lightone/trainer/` renders a dedicated trainer console.
- `trainer_dashboard_context()` builds today sessions, REVIEW/BLOCK queue, route counts, average QS, and pending confirmation metrics.
- The dashboard keeps non-medical safety copy visible.
- Tests cover REVIEW/BLOCK prioritization and trainer dashboard rendering.
- GitHub Actions verifies the Django test suite on PRs.

## 9. Next Validation Step

Run a 20-minute synthetic pilot review with one trainer or center owner:

1. Give the reviewer the trainer dashboard URL.
2. Ask them to identify the first member they would review.
3. Ask what they would say to the member.
4. Ask what part of the screen is unclear or not useful.
5. Record whether they ask for more automation or more explanation.

The output should be a short validation note, not a medical or performance claim.

