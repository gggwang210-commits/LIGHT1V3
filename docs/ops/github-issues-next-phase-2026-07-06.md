# LIGHT ONE Next Execution Phase — GitHub Issue Plan

Repository: `gggwang210-commits/LightOne_V2`  
Created: 2026-07-06  
Source strategy: `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`

> GitHub issue creation status: unavailable in this environment because the GitHub CLI is not installed and no GitHub API token is configured. Use the issue templates below to create issues manually.

## Guardrails for all issues

- Do not frame LIGHT ONE as medical diagnosis, disease prediction, treatment, rehabilitation treatment, or prescription.
- Use “통증 반응 기록”, “트레이너 검토 보조”, “운동 상담 참고”, and “비의료 웰니스/운동 상담 지원” language.
- Keep personal data collection minimal, consent-based, and de-identified for validation logs.

## Proposed issues

### Documentation

#### Issue 1 — 샘플 리포트 3종 제작: Basic / Review / Retake

**Labels:** `docs`, `pitch`, `high priority`  
**Priority:** High  
**Related document path:** `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`, `docs/validation/pilot-validation-plan.md`

**Objective**  
Create three non-medical sample report drafts that can be shown during customer interviews: Basic, Review, and Retake. The reports should help trainers explain exercise records, RPE, pain response records, session consistency, and next counseling points without implying diagnosis or treatment.

**Acceptance criteria**

- [ ] Basic report template covers standard member/session summary and trainer memo sections.
- [ ] Review report template covers trainer review-needed signals using non-medical wording.
- [ ] Retake report template supports renewal/re-registration counseling with before/after exercise participation and consultation notes.
- [ ] Each report includes a non-medical disclaimer and trainer final-review statement.
- [ ] Each report avoids diagnosis, disease prediction, treatment, prescription, and pain-cause claims.
- [ ] At least one screenshot or PDF-ready preview is prepared for interview use.

**Risk note**  
Report wording may be interpreted as medical advice if pain or condition changes are over-explained. Keep language limited to records, observed responses, and trainer review prompts.

---

#### Issue 2 — 비의료 고지문 작성

**Labels:** `docs`, `risk`, `high priority`  
**Priority:** High  
**Related document path:** `docs/governance/non-medical-boundary.md`, `README.md`

**Objective**  
Draft a concise non-medical disclaimer for the MVP screens, reports, interview material, and submission documents.

**Acceptance criteria**

- [ ] Disclaimer states LIGHT ONE is a non-medical wellness/exercise counseling support tool.
- [ ] Disclaimer states trainers perform final review before sharing outputs with members.
- [ ] Disclaimer avoids diagnosis, disease prediction, treatment, rehabilitation treatment, and prescription claims.
- [ ] BLOCK/stop-session language clearly says it is not a diagnosis and may require professional consultation if needed.
- [ ] Final wording is reusable in README, reports, MVP UI, and demo scripts.

**Risk note**  
A weak disclaimer could create regulatory or user-expectation risk. A strong disclaimer should not make the product sound unusable; it should clarify boundaries.

---

#### Issue 3 — Google Drive 사업계획서와 GitHub README 내용 동기화

**Labels:** `docs`, `pitch`, `high priority`  
**Priority:** High  
**Related document path:** `README.md`, `docs/LIGHT_ONE_final_business_plan_v1_2026-07-07.md`, `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`

**Objective**  
Synchronize the GitHub README and Google Drive business plan so that positioning, target customer, validation status, safety boundaries, and next execution priorities are consistent.

**Acceptance criteria**

- [ ] README customer validation status matches the business plan status.
- [ ] Business plan and README both use non-medical positioning.
- [ ] Any unvalidated claims remain marked as `[확인필요]` or equivalent.
- [ ] Links to validation, privacy, and non-medical boundary documents are current.
- [ ] A short change log notes which sections were synchronized.

**Risk note**  
Mismatched claims between investor/submission documents and GitHub documentation can weaken credibility and increase compliance risk.

---

#### Issue 4 — Slack Canvas 실행 로그 업데이트

**Labels:** `docs`, `validation`, `good first issue`  
**Priority:** Medium  
**Related document path:** `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`, `docs/ops/customer-validation-execution-2026-07-04.md`

**Objective**  
Update the Slack Canvas execution log with the current 7-day action plan, interview targets, sample report status, and pending evidence gaps.

**Acceptance criteria**

- [ ] Slack Canvas includes the current execution phase and date.
- [ ] Interview target count, scheduled interviews, and completed interviews are visible.
- [ ] Sample report preparation status is visible.
- [ ] Open `[확인필요]` items are listed with owners and next actions.
- [ ] No personally identifying interview details are copied into public/shared logs.

**Risk note**  
Operational logs may accidentally include personal information or unverified claims. Keep records de-identified and evidence-based.

---

### MVP Development

#### Issue 5 — Django 회원·세션·통증 반응 입력폼 구현

**Labels:** `mvp`, `high priority`  
**Priority:** High  
**Related document path:** `lightone_v2_django/README.md`, `lightone_v2_django/lightone/models.py`, `docs/validation/pilot-validation-plan.md`

**Objective**  
Implement MVP input forms for member profile, exercise session, RPE, pain response record, and trainer notes so pilot users can enter the minimum data needed for non-medical counseling reports.

**Acceptance criteria**

- [ ] Member form captures only minimum pilot fields required for validation.
- [ ] Session form captures exercise/session records and RPE.
- [ ] Pain field is named and described as “통증 반응 기록,” not pain diagnosis or cause analysis.
- [ ] Trainer memo field supports final human review notes.
- [ ] Forms include basic validation and user-friendly errors.
- [ ] No field asks for diagnosis, disease history, prescription, or treatment plan.

**Risk note**  
Input fields can unintentionally collect sensitive health data. Keep scope to exercise counseling context and minimum necessary data.

---

#### Issue 6 — QS 규칙 엔진 초안 구현

**Labels:** `mvp`, `risk`, `high priority`  
**Priority:** High  
**Related document path:** `lightone_v2_django/lightone/services.py`, `docs/governance/non-medical-boundary.md`, `docs/validation/pilot-validation-plan.md`

**Objective**  
Implement a draft QS rules engine that converts session completeness, RPE, pain response records, and trainer notes into non-medical counseling support signals.

**Acceptance criteria**

- [ ] QS output is described as a counseling support score or quality signal, not a health risk score.
- [ ] Rules are transparent and easy to adjust after customer validation.
- [ ] Pain response increases review priority without diagnosing cause or severity.
- [ ] Unit or smoke tests cover normal, review-needed, and blocked examples.
- [ ] Rule constants and thresholds are documented.

**Risk note**  
Scoring can be misunderstood as clinical assessment. Use clear naming and explanatory copy to position it as a trainer workflow aid.

---

#### Issue 7 — AUTO/REVIEW/BLOCK 라우팅 구현

**Labels:** `mvp`, `risk`, `high priority`  
**Priority:** High  
**Related document path:** `docs/governance/non-medical-boundary.md`, `lightone_v2_django/README.md`, `lightone_v2_django/lightone/services.py`

**Objective**  
Implement AUTO/REVIEW/BLOCK routing for report workflow triage while preserving trainer final review and non-medical boundaries.

**Acceptance criteria**

- [ ] AUTO means report draft can proceed to trainer final review.
- [ ] REVIEW means trainer should inspect pain response, quality, or unusual input before sharing.
- [ ] BLOCK means session/report flow should stop or be escalated to trainer review with appropriate non-medical caution text.
- [ ] Routing copy avoids diagnosis, disease prediction, treatment, and prescription.
- [ ] Routing decisions are visible in the MVP report or admin workflow.
- [ ] Tests or sample scenarios cover all three routes.

**Risk note**  
BLOCK language can sound like a medical decision. It must remain a safety/workflow guardrail, not a clinical judgment.

---

#### Issue 8 — synthetic sample data 생성

**Labels:** `mvp`, `good first issue`  
**Priority:** Medium  
**Related document path:** `lightone_v2_django/setup_dummy.py`, `docs/validation/pilot-validation-plan.md`

**Objective**  
Generate synthetic sample data for demos, screenshots, routing tests, and sample reports without using real member personal data.

**Acceptance criteria**

- [ ] Synthetic data includes Basic, Review, and Block/Retake-style scenarios.
- [ ] Data uses fictional names or anonymized member IDs only.
- [ ] Data avoids real phone numbers, emails, addresses, diagnoses, and disease histories.
- [ ] Data can be loaded consistently in the Django project.
- [ ] README or setup notes explain how to regenerate/load the sample data.

**Risk note**  
Demo data must never include real customer or interview data. Use synthetic records only.

---

### Customer Validation

#### Issue 9 — 고객 인터뷰 질문지 작성

**Labels:** `validation`, `docs`, `high priority`  
**Priority:** High  
**Related document path:** `docs/validation/trainer-interview-script.md`, `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`

**Objective**  
Prepare a concise interview questionnaire to validate trainer/center pain points, report usability, willingness to pay, and pilot readiness.

**Acceptance criteria**

- [ ] Questions cover problem validation, buyer validation, willingness-to-pay, and pilot feasibility.
- [ ] Questions include sample report feedback prompts.
- [ ] Questions avoid leading participants toward positive answers.
- [ ] Questions avoid medical diagnosis/treatment framing.
- [ ] Interview notes template supports de-identified evidence capture.

**Risk note**  
Leading or medically framed questions can produce biased or risky evidence. Keep questions neutral and business/workflow oriented.

---

#### Issue 10 — 센터·트레이너 인터뷰 5건 진행

**Labels:** `validation`, `high priority`  
**Priority:** High  
**Related document path:** `docs/validation/customer-discovery-log-template.md`, `docs/validation/pilot-center-list-template.md`, `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`

**Objective**  
Conduct five customer interviews across center owners/managers and trainers to validate workflow problems, sample report usefulness, pilot feasibility, and payment assumptions.

**Acceptance criteria**

- [ ] At least five interview candidates are contacted.
- [ ] At least three interviews are completed; stretch goal is five completed interviews.
- [ ] Interview notes are de-identified before being stored in GitHub or shared logs.
- [ ] Each completed interview records problem severity, report feedback, WTP signal, and pilot readiness.
- [ ] Repeated objections and positive evidence are summarized.
- [ ] No participant is asked for medical diagnosis, treatment, or patient data.

**Risk note**  
Customer validation may produce personal or sensitive information. Store only de-identified summaries and avoid collecting member-level health data.

---

#### Issue 11 — Airtable 고객검증 DB 필드 정리

**Labels:** `validation`, `docs`, `good first issue`  
**Priority:** Medium  
**Related document path:** `docs/validation/customer-discovery-log-template.md`, `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`

**Objective**  
Define Airtable fields for customer validation tracking so candidates, interview status, evidence strength, objections, WTP signals, and pilot readiness are consistently recorded.

**Acceptance criteria**

- [ ] Fields include candidate type, organization type, status, interview date, evidence strength, WTP signal, pilot readiness, objections, and follow-up action.
- [ ] Fields include a de-identified participant code instead of personal identifiers for shared exports.
- [ ] Fields map open claims to `[확인필요]`, validated, rejected, or needs follow-up.
- [ ] Field descriptions explain what should and should not be recorded.
- [ ] Export guidance prevents real personal data from being committed to GitHub.

**Risk note**  
Airtable can become a source of uncontrolled personal data. Use minimum fields and de-identification for shared documentation.

---

### Safety & Privacy

#### Issue 12 — 개인정보 동의서 초안 작성

**Labels:** `privacy`, `risk`, `high priority`  
**Priority:** High  
**Related document path:** `docs/governance/privacy-checklist.md`, `docs/validation/pilot-validation-plan.md`

**Objective**  
Draft a pilot/interview consent form covering purpose, collected data, retention, withdrawal, de-identification, and data handling responsibilities.

**Acceptance criteria**

- [ ] Consent form states the purpose is customer validation and pilot operation for a non-medical exercise counseling support service.
- [ ] Consent form lists minimum data categories and excludes diagnosis/treatment records.
- [ ] Consent form explains voluntary participation and withdrawal.
- [ ] Consent form explains de-identification for shared summaries.
- [ ] Consent form includes retention/deletion expectations.
- [ ] Consent form is reviewed against the privacy checklist before pilot use.

**Risk note**  
Consent language must be clear enough for early pilots but should not over-promise legal coverage. Consider legal review before scaled deployment.

---

### Demo Assets

#### Issue 13 — 1분 데모 시나리오 작성

**Labels:** `pitch`, `docs`, `high priority`  
**Priority:** High  
**Related document path:** `docs/submission/one-page-business-summary.md`, `docs/submission/modu-startup-summary.md`, `docs/strategy/next-phase-customer-validation-strategy-2026-07-04.md`

**Objective**  
Write a one-minute demo script showing the LIGHT ONE workflow from session input to trainer-reviewed report without implying medical diagnosis or automated prescription.

**Acceptance criteria**

- [ ] Script fits within approximately one minute when spoken.
- [ ] Script shows member/session input, QS/routing, trainer review, and report use in consultation.
- [ ] Script mentions non-medical boundaries naturally and briefly.
- [ ] Script includes a sample customer validation or pilot-readiness callout if evidence is available.
- [ ] Script avoids diagnosis, disease prediction, treatment, prescription, and AI-final-decision claims.

**Risk note**  
Demo scripts can easily overclaim. Keep the story focused on trainer workflow, consultation clarity, and validation evidence.

---

### Support Program Submission

#### Issue 14 — 제출자료 고객검증 증거 반영 및 최종 점검

**Labels:** `pitch`, `validation`, `high priority`  
**Priority:** High  
**Related document path:** `docs/submission/modu-startup-summary.md`, `docs/submission/one-page-business-summary.md`, `docs/LIGHT_ONE_final_business_plan_v1_2026-07-07.md`

**Objective**  
Update support-program submission materials with the latest customer validation evidence, sample report feedback, pilot candidate status, and non-medical safety boundaries.

**Acceptance criteria**

- [ ] Submission summary reflects completed interviews and sample report feedback.
- [ ] Unvalidated items remain clearly marked instead of stated as proven facts.
- [ ] Non-medical positioning is consistent with governance documents.
- [ ] Pilot candidate status is summarized without revealing personal information.
- [ ] README/business plan/submission summary claims are aligned.
- [ ] Final review checks labels, dates, links, and evidence status.

**Risk note**  
Submission documents may incentivize overclaiming traction or product capability. Only include evidence that has been collected and documented.
