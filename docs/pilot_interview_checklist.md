# Pilot Interview Checklist

## 1. Objective

This checklist is used for a 20-minute synthetic demo interview with a PT center owner, center manager, or trainer. The goal is to validate whether LIGHT ONE's trainer dashboard is understandable, useful, and safe enough to proceed to a small pilot.

The interview must not be used to claim medical effect, treatment outcome, diagnosis quality, injury prediction, or real-member performance improvement.

## 2. Interview Role

The interviewer should act as a product validation lead, not a salesperson.

Primary responsibilities:

- observe whether the reviewer understands the workflow without heavy explanation
- capture concrete objections and unclear areas
- identify whether the dashboard supports session preparation, review queue handling, and member communication
- avoid leading the reviewer toward positive answers
- record only non-identifying notes

## 3. Required Setup

Before the interview:

- Use synthetic/demo records only.
- Open the trainer console at `/lightone/trainer/`.
- Keep `docs/trainer_dashboard_validation.md` available for reference.
- Prepare a non-medical positioning sentence.
- Do not collect member names, phone numbers, health records, photos, videos, or private center data.

Suggested opening sentence:

> LIGHT ONE is a non-medical PT coaching support dashboard. It helps trainers review session records, discomfort responses, QS/JATC reference scores, and review-priority routing before communicating with a member.

## 4. 20-Minute Interview Flow

| Time | Step | Prompt | What to observe |
|---:|---|---|---|
| 0-2 min | Context | "How do you currently prepare for a member session or review?" | Current workflow, friction, repeated pain points |
| 2-5 min | Problem | "Where do records or member feedback usually get missed?" | Whether the problem is recent and operationally meaningful |
| 5-9 min | Dashboard read | "Please look at this screen and tell me what you think the first action should be." | Whether the reviewer finds REVIEW/BLOCK without instruction |
| 9-13 min | Queue review | "Pick one REVIEW or BLOCK case and explain what you would check." | Whether route, discomfort response, RPE, and QC are understood |
| 13-16 min | Communication | "What would you say to the member before or after this session?" | Whether wording stays non-medical and trainer-reviewed |
| 16-18 min | Adoption | "Where would this fit in your current center workflow?" | User, timing, operational owner, required integrations |
| 18-20 min | Decision | "What would need to be true for a 2-4 week pilot?" | Pilot condition, proof required, blocker |

## 5. Core Questions

Ask these without promising outcomes:

1. What part of session preparation is most time-consuming today?
2. What records are hardest to find before member communication?
3. When you see AUTO, REVIEW, and BLOCK, what do you think each state means?
4. Which member would you review first on this dashboard, and why?
5. What information is missing before you could confidently speak to the member?
6. Does the dashboard feel like an operations screen or a medical/diagnostic screen?
7. Would this help with feedback quality, retention conversation, or trainer consistency?
8. What would stop you from using this in a real center workflow?
9. What evidence would you need before paying for a pilot?
10. Who else in the center would need to approve or use this?

## 6. Pass / Hold Criteria

| Area | Pass | Hold |
|---|---|---|
| Problem clarity | Reviewer gives a recent concrete workflow problem | Reviewer says it is only "nice to have" |
| Dashboard comprehension | Reviewer identifies first review action without long explanation | Reviewer cannot interpret route or queue meaning |
| Safety boundary | Reviewer understands this is trainer-reviewed, non-medical reference information | Reviewer interprets it as diagnosis, treatment, or automated decision |
| Pilot fit | Reviewer can name a 2-4 week pilot use case | Reviewer cannot place it in center operations |
| Data safety | Reviewer accepts synthetic/demo review and minimal data collection | Reviewer expects real sensitive data before safe process exists |
| Commercial signal | Reviewer can describe payment condition or proof needed | Reviewer shows no condition under which they would pay |

## 7. Note-Taking Template

Use this structure for every interview note:

```text
Interview ID:
Segment:
Role:
Date:
Synthetic demo used: yes/no

Current workflow:
Recent problem evidence:
Dashboard first action:
REVIEW/BLOCK interpretation:
Non-medical boundary understood: yes/no
Useful use case:
Missing information:
Pilot condition:
Payment or budget signal:
Main blocker:
Next action:
```

## 8. Negative Items

Do not ask:

- "Would this diagnose the member better?"
- "Would this reduce pain?"
- "Would this prevent injury?"
- "Would this replace trainer judgment?"
- "Can we upload your members' health data now?"
- "Is this hospital-grade enough?"

Do not record:

- real member names
- phone numbers
- photos or videos
- health records
- detailed pain histories
- payment identifiers
- private center staff records

## 9. Output After Interview

After each interview, produce a short validation note with:

- one strongest problem signal
- one strongest adoption blocker
- whether the reviewer understood REVIEW/BLOCK
- whether non-medical positioning was understood
- pilot readiness: `pass`, `hold`, or `reject`
- next action

Do not convert one positive reaction into traction, paid demand, clinical evidence, or product-market fit.

