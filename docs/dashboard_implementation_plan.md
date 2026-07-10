# LIGHT ONE 대시보드 구현 계획

작성일: 2026-07-07  
상태: 설계/구현 지시 문서  
적용 저장소: `gggwang210-commits/LightOne_V2`  
참조 저장소: `gggwang210-commits/lightone`  

---

## 1. 목적

본 문서는 Manus 작업이 토큰 소모로 중단된 이후, LIGHT ONE의 회원·트레이너·관리자 대시보드를 Codex/GitHub 기준으로 이어가기 위한 구현 계획이다.

현재 기준:

- Manus ZIP은 React + Vite + Tailwind + shadcn/ui 기반 템플릿 수준이다.
- `Home.tsx`는 Example Page 수준이며 실제 LIGHT ONE 대시보드는 구현되지 않았다.
- 기존 `lightone` 저장소에는 V1 대시보드 견본 이미지가 있다.
- 현재 개발·사업 기준 저장소는 `LightOne_V2`다.

따라서 본 단계에서는 Django에 바로 붙이는 것보다, 먼저 다음 산출물을 만든다.

1. 역할별 IA 문서
2. 회원·트레이너·관리자 화면 명세
3. 컴포넌트 라이브러리 문서
4. 합성 샘플 데이터
5. 정적 HTML/CSS/JS 프로토타입
6. pytest 기반 구조 검증 테스트

---

## 2. 비의료 안전 경계

LIGHT ONE은 비의료 PT 상담 리포트 SaaS + 데이터 기반 프리미엄 컨디셔닝 브랜드 운영 시스템이다.

LIGHT ONE은 다음을 제공하지 않는다.

- 의료 진단
- 치료
- 처방
- 질병 예측
- 재활 처방
- 통증 원인 확정
- 임상 의사결정 지원
- 의료 수준 분석

안전한 표현은 다음을 사용한다.

| 금지 표현 | 대체 표현 |
|---|---|
| AI 진단 | AI 기반 상담 보조 |
| 통증 원인 분석 | 통증 반응 기록 |
| 질병 위험도 예측 | 주의 신호 확인 |
| 치료 효과 | 운동 상담 변화 기록 |
| 처방 | 컨디셔닝 과제 제안 |
| 재활 처방 | 운동 난이도·동작 범위 조정 |
| 의료 수준 분석 | 비의료 웰니스 참고 리포트 |
| AI가 판단 | 트레이너 검토 필요 |

공통 하단 문구:

> 본 화면은 운동상담 및 컨디셔닝 관리를 위한 비의료 참고 자료입니다. 의료 진단·치료·처방을 대체하지 않으며, 의학적 판단이 필요한 경우 관련 전문가의 상담을 권장합니다.

---

## 3. 정보 구조 IA

```text
LIGHT ONE
├── Member App
│   ├── Home
│   ├── Condition
│   ├── Progress
│   ├── Reports
│   ├── Reservation
│   ├── Payment
│   ├── Messages
│   └── My Page
│
├── Trainer Console
│   ├── Home
│   ├── Today Sessions
│   ├── Members
│   ├── Member Detail
│   ├── Session Record
│   ├── Report Builder
│   ├── Review Queue
│   ├── Messages
│   └── Retention
│
└── Admin Console
    ├── Overview
    ├── Trainers
    ├── Members
    ├── Reservations
    ├── Payments
    ├── Reports
    ├── Risk Queue
    ├── Communications
    ├── Permissions
    └── Settings
```

---

## 4. 화면별 구성

### 4.1 회원 대시보드

회원 화면의 핵심은 복잡한 지표보다 `무엇이 변했는지`, `다음에 무엇을 해야 하는지`를 쉽게 보여주는 것이다.

필수 구성:

- 오늘의 컨디션
- 이번 주 변화
- 통증 반응 변화
- 자세·움직임 참고 지표
- 운동 수행 변화
- 트레이너 피드백
- 다음 컨디셔닝 과제
- 예약 확인
- 결제 상태
- 내 리포트 보기
- 트레이너에게 요청하기
- 알림
- 동의 상태

회원 UX 규칙:

- 쉬운 한국어를 사용한다.
- 기술 지표보다 변화 요약을 먼저 보여준다.
- Good / Check / Review 상태 라벨을 사용한다.
- 의료 진단·치료·처방 표현을 사용하지 않는다.
- 다음 행동 버튼을 명확히 제공한다.

### 4.2 트레이너 대시보드

트레이너 화면의 핵심은 회원 변화 추적, 세션 기록, REVIEW/BLOCK 관리, 다음 세션 계획, 상담 리포트 생성이다.

필수 구성:

- 오늘 세션 목록
- 회원 검색/리스트
- 회원별 변화 타임라인
- QS/JATC 요약
- 통증 반응·RPE 변화
- 운동 수행 기록
- AUTO/REVIEW/BLOCK 큐
- 리포트 초안
- 회원 요청사항
- 피드백 인박스
- 다음 세션 계획
- 재등록 상담 후보
- 커뮤니케이션 기록

트레이너 업무 흐름:

```text
세션 전 → 회원 상태 확인 → 지난 피드백 확인 → REVIEW/BLOCK 여부 확인 → 오늘 세션 계획 확인
세션 중 → 운동 수행 기록 → RPE 입력 → 통증 반응 입력 → 조정 내용 메모
세션 후 → 리포트 초안 생성 → 트레이너 피드백 추가 → 다음 과제 부여 → 회원에게 공유
주간 리뷰 → 4주/8주 변화 확인 → 재등록 상담 후보 확인 → 상담 리포트 생성
```

### 4.3 관리자 페이지

관리자 화면의 핵심은 센터 운영 KPI, 트레이너 관리, 회원 유지, 예약·결제, 개인정보 권한 관리다.

필수 구성:

- 센터 운영 요약
- 트레이너별 회원 관리 현황
- 회원 상태
- 예약 캘린더
- 결제 현황
- 리포트 생성률
- 재등록 후보
- REVIEW/BLOCK 현황
- 커뮤니케이션 품질
- 피드백·클레임
- 개인정보 접근권한
- 감사 로그
- SaaS 플랜/결제 관리

관리자 KPI:

- 활성 회원 수
- 예정 세션 수
- 완료 세션 수
- 리포트 생성률
- REVIEW/BLOCK 건수
- 재등록 후보 수
- 트레이너 응답 시간
- 회원 만족도
- 미납 건수
- 이탈 위험 회원 수
- 동의 완료율
- 민감정보 접근 로그 수

---

## 5. 컴포넌트 목록

### 5.1 공통 컴포넌트

- `SidebarNav`
- `TopBar`
- `MetricCard`
- `StatusBadge`
- `TrendMiniChart`
- `SectionHeader`
- `EmptyState`
- `NonMedicalDisclaimerFooter`
- `ActionButton`
- `DataTable`

### 5.2 회원용 컴포넌트

- `TodayConditionCard`
- `WeeklyChangeCard`
- `PainResponseCard`
- `PostureReferenceCard`
- `TrainingProgressCard`
- `TrainerFeedbackCard`
- `NextActionCard`
- `ReservationCard`
- `PaymentStatusCard`
- `ReportHistoryList`
- `RequestToTrainerBox`

### 5.3 트레이너용 컴포넌트

- `TodaySessionList`
- `MemberSearchPanel`
- `MemberChangeTimeline`
- `QSJATCSummaryCard`
- `PainRPEPanel`
- `ExerciseLogTable`
- `ReviewQueueTable`
- `ReportDraftList`
- `MemberRequestInbox`
- `NextSessionPlanCard`
- `RetentionCandidateList`

### 5.4 관리자용 컴포넌트

- `CenterOverviewKPI`
- `TrainerPerformanceTable`
- `MemberStatusTable`
- `ReservationCalendar`
- `PaymentOverviewPanel`
- `ReportGenerationMetrics`
- `ReRegistrationPipeline`
- `RiskQueuePanel`
- `CommunicationMonitor`
- `PermissionAuditTable`
- `ConsentStatusPanel`

---

## 6. 샘플 데이터 구조

샘플 데이터는 모두 합성 데이터만 사용한다.

생성 대상:

- `sample_data/dashboard_member_example.json`
- `sample_data/dashboard_trainer_example.json`
- `sample_data/dashboard_admin_example.json`

금지:

- 실제 회원 이름
- 실제 전화번호
- 실제 사진
- 실제 영상
- 실제 건강정보
- 실제 통증 기록

권장 표기:

- 회원 A
- 트레이너 K
- 센터 데모
- 데모 수치 / 참고 수치 / [검증필요]

---

## 7. UI 문구

### 회원용

| 요소 | 문구 |
|---|---|
| 오늘의 컨디션 | 오늘은 `확인 필요` 상태입니다. 다음 세션 전 불편감 변화를 기록해 주세요. |
| 이번 주 변화 | 이번 주에는 운동 이행률과 하체 안정성이 좋아졌습니다. |
| 통증 반응 변화 | 입력된 통증 반응 기록 기준으로 확인이 필요한 변화가 있습니다. |
| 자세 참고 지표 | 자세 참고 지표는 운동상담을 위한 변화 확인 자료입니다. |
| 트레이너 피드백 | 이번 주는 무리한 중량보다 움직임 안정성을 우선합니다. |
| 다음 과제 | 다음 세션 전 홈 컨디셔닝 과제를 완료해 주세요. |
| 예약 확인 | 다음 세션 일정을 확인하세요. |
| 결제 상태 | 이용권 잔여 횟수와 결제 상태를 확인하세요. |

### 트레이너용

| 요소 | 문구 |
|---|---|
| 오늘 세션 | 오늘 REVIEW 확인이 필요한 회원이 있습니다. |
| QS 요약 | QS는 운동상담 참고 점수이며 의료 판단 기준이 아닙니다. |
| JATC 요약 | 통증 반응, 자세 참고 지표, 운동 수행, 생활습관을 함께 확인하세요. |
| REVIEW 큐 | 트레이너 확인 후 세션 계획을 조정하세요. |
| BLOCK 상태 | 운동 진행 전 추가 확인이 필요한 주의 신호입니다. 진단하지 마세요. |
| 리포트 초안 | 회원에게 공유하기 전 트레이너 코멘트를 확인하세요. |

### 관리자용

| 요소 | 문구 |
|---|---|
| 센터 현황 | 오늘 예약, 리포트 생성, 결제 상태를 한눈에 확인합니다. |
| 트레이너 관리 | 트레이너별 회원 관리 현황과 응답 상태를 확인하세요. |
| 회원 상태 | 재등록 후보와 확인이 필요한 회원을 우선 관리하세요. |
| 리포트 생성률 | 리포트 생성률은 상담 품질 표준화의 핵심 지표입니다. |
| 권한 관리 | 민감정보 접근은 역할별 권한에 따라 제한됩니다. |

---

## 8. 권장 파일 구조

```text
LightOne_V2/
├── docs/
│   ├── dashboard_information_architecture.md
│   ├── member_dashboard_spec.md
│   ├── trainer_dashboard_spec.md
│   ├── admin_dashboard_spec.md
│   ├── dashboard_component_library.md
│   ├── dashboard_data_model.md
│   ├── dashboard_sample_user_flows.md
│   ├── dashboard_safety_copy_guidelines.md
│   └── dashboard_implementation_plan.md
│
├── prototype/
│   └── dashboards/
│       ├── index.html
│       ├── member_dashboard.html
│       ├── trainer_dashboard.html
│       ├── admin_dashboard.html
│       ├── dashboard_theme.css
│       ├── dashboard_mock_data.js
│       └── README.md
│
├── sample_data/
│   ├── dashboard_member_example.json
│   ├── dashboard_trainer_example.json
│   └── dashboard_admin_example.json
│
└── tests/
    ├── test_dashboard_docs.py
    ├── test_dashboard_sample_data.py
    └── test_dashboard_prototype_files.py
```

---

## 9. Codex 구현 순서

1. 기존 README·docs 구조 확인
2. 대시보드 IA 문서 생성
3. 역할별 화면 명세 작성
4. 컴포넌트 라이브러리 문서 작성
5. 합성 샘플 데이터 JSON 생성
6. 정적 HTML/CSS/JS 프로토타입 생성
7. 네이비/블루 대시보드 테마 CSS 생성
8. README 링크 추가
9. pytest 테스트 추가
10. 위험 표현 검색·수정

---

## 10. 테스트 항목

추가할 테스트:

- `tests/test_dashboard_docs.py`
- `tests/test_dashboard_sample_data.py`
- `tests/test_dashboard_prototype_files.py`

검증 항목:

- 대시보드 문서 존재
- 샘플 데이터 JSON 유효성
- 프로토타입 파일 존재
- README가 대시보드 문서로 연결
- 민감정보 폴더가 없는지 확인

금지 폴더:

- `real_member_data`
- `member_photos`
- `member_videos`
- `private_health_data`
- `health_records`
- `real_patient_data`

---

## 11. 남은 검증 필요 항목

- 실제 회원 사용성 검증 [검증필요]
- 트레이너 업무 흐름 적합성 검증 [검증필요]
- 센터장 KPI 필요성 검증 [검증필요]
- QS/JATC 임계값 검증 [검증필요]
- REVIEW/BLOCK 운영 기준 검증 [검증필요]
- 개인정보 동의·보관·삭제 정책 검토 [검증필요]
- 예약·결제 실제 연동 범위 검토 [검증필요]
