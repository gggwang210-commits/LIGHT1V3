# Member Dashboard Specification

## A. Purpose

The member dashboard should help members easily understand:
- today’s condition
- recent body/condition changes
- pain response trend
- posture/movement reference changes
- trainer feedback
- assigned next actions
- reservation status
- payment status
- consultation report history

## B. Core sections

| Section | Purpose | Main action |
|---|---|---|
| Today Summary | 오늘 컨디션, 예약, 알림을 한눈에 표시 | 오늘 할 일 확인 |
| Condition Score Card | 컨디션 참고 점수를 쉬운 상태로 요약 | 변화 상세 보기 |
| Pain Response Trend | 통증 반응 기록의 최근 흐름 표시 | 반응 입력/수정 |
| Posture & Movement Change | 자세·동작 참고 지표 변화 요약 | 리포트 보기 |
| Training Progress | 세션 참석, 수행, 과제 진행률 표시 | 진행 상황 확인 |
| Trainer Feedback | 트레이너가 검토한 메시지 표시 | 피드백 확인 |
| Next Conditioning Actions | 다음 세션 전 준비 과제 | 완료 체크 |
| Reservation | 예정 세션, 변경 가능 시간 표시 | 예약 변경/확인 |
| Payment | 이용권, 결제 예정, 미결제 상태 표시 | 결제하기 |
| Report History | 상담 리포트 목록과 상태 | 리포트 열람 |
| Requests to Trainer | 질문·요청 작성과 답변 상태 | 요청 보내기 |
| Notifications | 예약, 피드백, 결제, 리포트 알림 | 알림 확인 |

## C. Member UX rules

- Use simple words, not technical terms.
- Do not show raw complex metrics first.
- Show “what changed” before “why it matters.”
- Use traffic-light style state labels: **Good / Check / Review**.
- Avoid medical wording.
- Provide reassurance but do not diagnose.
- Make the next action obvious.

## D. Example member screen cards

| Card | Fields | State label | Primary CTA |
|---|---|---|---|
| 오늘의 컨디션 | date, conditionLabel, energy, sleep, stress | Good / Check / Review | 오늘 상태 입력 |
| 이번 주 변화 | weeklySummary, sessionsDone, consistency | Good / Check | 변화 보기 |
| 통증 반응 변화 | bodyArea, trend, latestLevel, note | Good / Check / Review | 반응 기록하기 |
| 자세 참고 지표 | referenceItems, changedItems, qcStatus | Check | 자세 리포트 보기 |
| 트레이너 피드백 | trainerName, reviewedAt, message | Good | 확인 완료 |
| 다음 세션 준비사항 | actions, dueDate, completion | Check | 과제 체크 |
| 예약 확인 | nextSession, location, trainer | Good | 예약 변경 |
| 결제 상태 | planName, remainingSessions, paymentState | Good / Check | 결제 확인 |
| 내 리포트 보기 | reportTitle, reportDate, status | Good | 리포트 열기 |

## E. Sample Korean UX copy

- 오늘의 컨디션: “오늘 컨디션은 안정적이에요. 수면 시간이 조금 짧아 다음 세션 전 가벼운 준비운동을 권장합니다.”
- 이번 주 변화: “이번 주는 세션 2회를 완료했고, 운동 기록이 꾸준히 쌓이고 있어요.”
- 통증 반응 변화: “최근 입력된 통증 반응이 지난주보다 낮게 기록되었습니다. 불편감이 계속되면 트레이너에게 알려주세요.”
- 자세 참고 지표: “촬영 조건이 양호하여 지난 리포트와 참고 비교가 가능합니다.”
- 트레이너 피드백: “오늘은 무리한 강도보다 동작 범위를 편안하게 유지하는 데 집중해 주세요.”
- 다음 세션 준비사항: “세션 전 물 섭취와 5분 가벼운 걷기를 완료해 주세요.”
- 예약 확인: “다음 예약은 7월 9일 목요일 오후 7시입니다.”
- 결제 상태: “이용권 4회가 남아 있습니다. 다음 결제 예정일을 확인해 주세요.”
- 내 리포트 보기: “트레이너 검토가 완료된 비의료 웰니스 참고 리포트를 확인할 수 있습니다.”

## Non-medical footer copy

“LIGHT ONE은 의료 진단이나 치료를 제공하지 않으며, 입력 기록을 바탕으로 트레이너 검토용 비의료 웰니스 참고 정보를 제공합니다.”
