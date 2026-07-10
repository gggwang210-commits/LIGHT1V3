# Dashboard Information Architecture

## IA tree

- Member App
  - Home
  - Condition
  - Progress
  - Report
  - Reservation
  - Payment
  - Messages
  - My Page
- Trainer Console
  - Home
  - Today Sessions
  - Members
  - Member Detail
  - Session Record
  - Report Builder
  - Review Queue
  - Messages
  - Retention
- Admin Console
  - Overview
  - Trainers
  - Members
  - Reservations
  - Payments
  - Reports
  - Risk Queue
  - Communications
  - Permissions
  - Settings

## Route catalog

| App | Route | Path | Role | Primary purpose | Key data displayed | Main action |
|---|---|---|---|---|---|---|
| Member App | Home | `/member/home` | Member | 오늘 상태와 주요 알림 | condition, reservation, feedback | 오늘 상태 입력 |
| Member App | Condition | `/member/condition` | Member | 컨디션과 통증 반응 기록 | conditionScore, painResponses | 반응 기록 |
| Member App | Progress | `/member/progress` | Member | 주간 변화와 세션 진행 | weeklyChange, progress | 변화 보기 |
| Member App | Report | `/member/reports` | Member | 트레이너 검토 리포트 | reports | 리포트 열기 |
| Member App | Reservation | `/member/reservations` | Member | 예약 확인/변경 | reservations | 예약 변경 |
| Member App | Payment | `/member/payments` | Member | 이용권/결제 상태 | payments | 결제 확인 |
| Member App | Messages | `/member/messages` | Member | 트레이너 요청/답변 | messages | 요청 보내기 |
| Member App | My Page | `/member/my` | Member | 동의/프로필/알림 설정 | consent, profile | 설정 변경 |
| Trainer Console | Home | `/trainer/home` | Trainer | 오늘 업무와 검토 큐 | sessions, queues | 우선순위 처리 |
| Trainer Console | Today Sessions | `/trainer/sessions/today` | Trainer | 오늘 세션 운영 | sessions | 세션 시작 |
| Trainer Console | Members | `/trainer/members` | Trainer | 회원 목록과 상태 | members | 회원 선택 |
| Trainer Console | Member Detail | `/trainer/members/:id` | Trainer | 회원 변화 타임라인 | timeline, reports | 상세 검토 |
| Trainer Console | Session Record | `/trainer/sessions/:id/record` | Trainer | 운동/RPE/통증 반응 기록 | exerciseLogs, rpe, pain | 기록 저장 |
| Trainer Console | Report Builder | `/trainer/reports/builder` | Trainer | 리포트 초안 검토 | draft, feedback | 리포트 확정 |
| Trainer Console | Review Queue | `/trainer/review-queue` | Trainer | REVIEW/BLOCK 처리 | queueItems | 검토 처리 |
| Trainer Console | Messages | `/trainer/messages` | Trainer | 회원 요청 응답 | requests, messages | 답변 작성 |
| Trainer Console | Retention | `/trainer/retention` | Trainer | 재등록 상담 준비 | candidates | 상담 준비 |
| Admin Console | Overview | `/admin/overview` | AdminUser | 센터 운영 요약 | kpis | 현황 확인 |
| Admin Console | Trainers | `/admin/trainers` | AdminUser | 트레이너 성과/업무량 | trainerMetrics | 배정 조정 |
| Admin Console | Members | `/admin/members` | AdminUser | 회원 상태 관리 | memberStatus | 상세 확인 |
| Admin Console | Reservations | `/admin/reservations` | AdminUser | 예약 캘린더 | reservations | 예약 조정 |
| Admin Console | Payments | `/admin/payments` | AdminUser | 결제/미납 관리 | payments | 결제 이슈 처리 |
| Admin Console | Reports | `/admin/reports` | AdminUser | 리포트 사용량 | reportMetrics | 누락 확인 |
| Admin Console | Risk Queue | `/admin/risk-queue` | AdminUser | 센터 검토 큐 | reviewQueue | 처리 상태 확인 |
| Admin Console | Communications | `/admin/communications` | AdminUser | 응답 품질 모니터링 | responseTimes, complaints | 후속 조치 |
| Admin Console | Permissions | `/admin/permissions` | AdminUser | 권한/동의/접근 로그 | roles, consents, auditLogs | 권한 변경 |
| Admin Console | Settings | `/admin/settings` | AdminUser | 센터 설정/SaaS 플랜 | plan, settings | 설정 저장 |
