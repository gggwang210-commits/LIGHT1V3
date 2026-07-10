# LIGHT ONE V2 MVP 개발 지시서 — Codex용

> 목적: 이 문서는 LIGHT ONE V2 Django MVP를 Codex로 고도화하기 위한 작업 지시서입니다.  
> 권장 위치: `docs/CODEX_LIGHTONE_V2_MVP.md`

---

## 0. Codex에 붙여넣을 짧은 실행 프롬프트

아래 문장만 Codex에 먼저 붙여 넣으세요.

```text
프로젝트 루트의 docs/CODEX_LIGHTONE_V2_MVP.md를 먼저 읽고, 지시서에 따라 LIGHT ONE V2 Django MVP를 단계별로 고도화해 주세요.

진행 순서:
1. 현재 프로젝트 구조를 먼저 확인합니다.
2. 기존 구조를 삭제하거나 대규모로 갈아엎지 않습니다.
3. QS/JATC 계산 엔진, 대시보드, HTML 리포트, 테스트, README를 순서대로 구현합니다.
4. 각 Step 완료 후 작업 로그를 남깁니다.
5. 실제 회원정보, 실제 건강정보, API 키, 토큰은 절대 사용하지 않습니다.
6. 모든 화면과 리포트에 비의료 안전 문구를 포함합니다.
7. python manage.py check, migrate, test, runserver 기준으로 최종 확인합니다.

작업 전 먼저 `pwd`, `ls`, `python manage.py check`, `find . -maxdepth 3 -type f | sort` 결과를 확인하고 Step 0 로그부터 작성해 주세요.
```

---

## 1. 프로젝트 정체성

LIGHT ONE V2는 **Django 기반 비의료 PT 상담 리포트 SaaS MVP**입니다.

서비스 목적은 트레이너가 회원의 운동 수행 기록, 불편감 반응, RPE, 자세 관찰, 생활습관 데이터를 구조화해 상담과 재등록 상담에 활용하도록 돕는 것입니다.

### 핵심 원칙

- AI/알고리즘은 트레이너 판단을 보조합니다.
- 최종 상담과 운동 진행 여부는 트레이너가 검토합니다.
- 의료 진단, 치료, 처방, 재활 효과 판단을 제공하지 않습니다.
- 모든 데이터는 MVP 단계에서 synthetic/demo 데이터만 사용합니다.

### 핵심 방법론

1. **파악**: 운동 수행, 불편감 반응, 자세 관찰, RPE, 생활습관을 구조화
2. **회복**: 약한 기능과 운동 수행 방해 요인을 트레이너가 확인할 수 있게 정리
3. **트레이닝**: 컨디셔닝 기초 위에서 운동 방향을 조정할 수 있도록 상담 자료 제공

> 주의: 여기서 “회복”은 의료적 재활이나 치료가 아니라, PT 현장에서 운동 수행을 준비하는 비의료 컨디셔닝 표현입니다.

---

## 2. 절대 규칙

반드시 지켜야 합니다.

1. 실제 회원정보, 실제 건강정보, API 키, 비밀번호, 토큰을 사용하지 않습니다.
2. 모든 테스트와 seed 데이터는 synthetic/demo 데이터만 사용합니다.
3. 의료 진단, 치료, 처방, 재활, 교정, 통증 원인 확정 표현을 사용하지 않습니다.
4. 모든 주요 화면과 리포트에는 아래 안전 문구를 포함합니다.

```text
본 자료는 비의료 운동상담 참고 자료이며, 최종 상담과 운동 진행 여부는 트레이너 검토가 필요합니다.
```

5. BLOCK은 의료 판단이 아니라 **세션 진행 전 안전 확인 신호**입니다.
6. PDF 라이브러리는 이번 MVP에서 추가하지 않습니다. 우선 HTML 리포트 + 인쇄용 CSS + print 버튼으로 구현합니다.
7. 기존 프로젝트 구조를 삭제하거나 대규모로 갈아엎지 않습니다.
8. 명령 실행 결과를 꾸며내지 않습니다. 실패하면 실패 원인과 수정 계획을 기록합니다.

### 금지 표현

- 진단
- 치료
- 처방
- 재활
- 교정
- 완치
- 정상/비정상 판정
- 통증 원인은 ~입니다
- 질환이 의심됩니다
- 치료가 필요합니다
- 재활이 필요합니다

### 대체 표현

- 확인 필요
- 상담 참고
- 운동 수행 기록 기준
- 트레이너 검토 필요
- 세션 진행 전 안전 확인
- 전문가 상담 권고 가능
- 불편감 반응이 높게 기록됨

---

## 3. 전체 개발 범위

이번 MVP에서 구현할 범위는 다음입니다.

1. QS/JATC 계산 엔진
2. AUTO / REVIEW / BLOCK 라우팅
3. 세션 입력 폼
4. 대시보드 시각화
5. HTML 기반 Basic Report Generator
6. synthetic demo 데이터
7. 테스트 코드
8. README 초보자 실행 가이드
9. GitHub PR 형태 정리

이번 MVP에서 하지 않는 것:

- 실제 Airtable API 연동
- 실제 고객/건강정보 수집
- PDF 라이브러리 도입
- 외부 AI API 연동
- 의료 판단 자동화
- 운영용 개인정보 처리 시스템 구축

---

## 4. Step 0 — 프로젝트 구조 확인

먼저 현재 프로젝트 구조를 확인합니다.

```bash
pwd
ls
python manage.py check
find . -maxdepth 3 -type f | sort
```

`tree`가 설치되어 있을 때만 실행합니다.

```bash
tree -L 3
```

확인할 것:

- Django settings 위치
- app 이름
- models.py
- views.py
- forms.py
- urls.py
- templates 구조
- static 구조
- README.md
- requirements.txt
- 기존 테스트 파일
- 기존 seed/demo 파일

주의:

- app 이름이 `lightone`이 아니라면 실제 app 이름을 기준으로 작업합니다.
- 기존 `MemberSession` 또는 유사 모델이 있으면 중복 생성하지 말고 확장합니다.
- 기존 구조가 예상과 다르면 먼저 구조 요약과 수정 계획을 기록합니다.

### Step 0 완료 로그

```text
[STEP 0] 프로젝트 구조 확인
- 확인한 app 이름:
- 주요 파일:
- 기존 모델:
- 기존 URL 흐름:
- 위험한 변경 가능성:
- 다음 작업 계획:
```

---

## 5. Step 1 — 데이터 모델 고도화

목표는 Member / Session / Indicator Layer 구조를 반영하되, 기존 프로젝트를 깨지 않도록 구현하는 것입니다.

### 권장 구조

- Member 또는 Client: 최소 식별 정보만 보관
- MemberSession 또는 SessionRecord: 세션 입력 기록
- QS/JATC 관련 필드: 세션 단위 계산 결과로 저장

### 개인정보 최소화

- 실제 이름, 전화번호, 이메일, 주소, 민감 건강정보 사용 금지
- demo 데이터는 “데모회원 A”, “DEMO-001” 형태 사용
- 실제 운영 전 개인정보 정책 필요 문구를 README에 기록

### 기존 MemberSession 모델이 있을 때 추가 권장 필드

```text
member_name
goal
exercise_name
form_accuracy
planned_reps
completed_reps
planned_rest_seconds
actual_rest_seconds
pain_response
rpe
posture_score
lifestyle_score
rep_achievement_rate
rest_compliance
pain_score
function_training_score
qs_score
jatc_score
route
review_note
trainer_confirmed
created_at
```

주의:

- 이미 유사 필드가 있으면 중복 필드를 만들지 말고 기존 필드명을 활용합니다.
- 기존 DB를 불필요하게 파괴하는 migration은 만들지 않습니다.

실행:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py check
```

### Step 1 완료 로그

```text
[STEP 1] 데이터 모델
- 수정 파일:
- 추가/수정 필드:
- migration 파일:
- 개인정보 최소화 확인:
- check 결과:
```

---

## 6. Step 2 — QS/JATC 알고리즘 엔진

계산 로직은 views나 templates에 흩뿌리지 말고 순수 함수로 분리합니다.

권장 파일:

- `app_name/engines.py`
- 기존 `services.py`가 있다면 그 안에 분리 가능

### QS 입력 기준

- form_accuracy: 0~100
- pain_response: 0~10
- rpe: 0~10
- planned_reps: 0 이상
- completed_reps: 0 이상
- planned_rest_seconds: 0 이상
- actual_rest_seconds: 0 이상

### QS 구성

| 항목 | 가중치 |
|---|---:|
| Form Accuracy | 0.4 |
| Rep Achievement Rate | 0.3 |
| Rest Compliance | 0.2 |
| Pain Response Score | 0.1 |

### 계산식

```python
def clamp(value, min_value=0, max_value=100):
    return max(min_value, min(max_value, value))


def calculate_rep_achievement_rate(planned_reps, completed_reps):
    if planned_reps <= 0:
        return 0
    return clamp(completed_reps / planned_reps * 100)


def calculate_rest_compliance(planned_rest_seconds, actual_rest_seconds):
    if planned_rest_seconds <= 0:
        return 100
    diff_ratio = abs(actual_rest_seconds - planned_rest_seconds) / planned_rest_seconds
    return max(0, 100 - min(diff_ratio * 100, 100))


def calculate_pain_score(pain_response):
    return clamp(100 - pain_response * 10)


def calculate_qs_score(form_accuracy, rep_achievement_rate, rest_compliance, pain_score):
    return (
        form_accuracy * 0.4
        + rep_achievement_rate * 0.3
        + rest_compliance * 0.2
        + pain_score * 0.1
    )
```

### 라우팅

```python
def determine_route(qs_score, pain_response):
    if pain_response >= 7 or qs_score < 40:
        return "BLOCK"
    if qs_score >= 80 and pain_response <= 3:
        return "AUTO"
    return "REVIEW"
```

라우팅 의미:

- AUTO: 상담 리포트 자동 생성 가능
- REVIEW: 트레이너 검토 필요
- BLOCK: 세션 진행 전 안전 확인 필요

### JATC 구성

| 영역 | 가중치 |
|---|---:|
| Pain Domain | 0.30 |
| Posture Domain | 0.25 |
| Function & Training Domain | 0.30 |
| Lifestyle Domain | 0.15 |

계산 예시:

```python
def safe_average(values):
    valid_values = [v for v in values if v is not None]
    if not valid_values:
        return 0
    return sum(valid_values) / len(valid_values)


def calculate_jatc_score(
    pain_response,
    posture_score,
    qs_score,
    form_accuracy,
    rep_achievement_rate,
    lifestyle_score,
):
    pain_domain = calculate_pain_score(pain_response)
    function_training_domain = safe_average([qs_score, form_accuracy, rep_achievement_rate])

    return (
        pain_domain * 0.30
        + posture_score * 0.25
        + function_training_domain * 0.30
        + lifestyle_score * 0.15
    )
```

README와 리포트에 아래 문구를 포함합니다.

```text
[확인필요] JATC 가중치와 임계값은 파일럿 데이터와 전문가 검토 후 조정이 필요합니다.
```

### Step 2 완료 로그

```text
[STEP 2] QS/JATC 알고리즘
- 수정 파일:
- 구현 함수:
- 라우팅 조건:
- 안전 표현 반영 여부:
- 테스트 작성 여부:
```

---

## 7. Step 3 — forms/views/urls 연결

목표는 사용자가 아래 흐름을 사용할 수 있게 만드는 것입니다.

```text
세션 입력 → QS/JATC 계산 → 대시보드 반영 → 리포트 확인
```

### Form 필수 입력

- member_name
- goal
- exercise_name
- form_accuracy
- planned_reps
- completed_reps
- planned_rest_seconds
- actual_rest_seconds
- pain_response
- rpe
- posture_score
- lifestyle_score
- memo 또는 review_note

### 폼 검증

- form_accuracy: 0~100
- posture_score: 0~100
- lifestyle_score: 0~100
- pain_response: 0~10
- rpe: 0~10
- planned_reps: 0 이상
- completed_reps: 0 이상
- planned_rest_seconds: 0 이상
- actual_rest_seconds: 0 이상

### View 흐름

1. dashboard
2. session_create
3. session_detail 또는 report_detail
4. report_detail

POST 저장 시:

1. form 검증
2. QS/JATC 계산
3. route 저장
4. review_note 생성
5. 저장 후 report_detail 또는 dashboard로 redirect

주의:

- 중복 URL을 만들지 않습니다.
- 기존 URL 이름이 있으면 그대로 유지합니다.
- 모든 화면에 안전 문구를 넣습니다.

### Step 3 완료 로그

```text
[STEP 3] forms/views/urls 연결
- 수정 파일:
- 입력 폼:
- 연결 URL:
- redirect 흐름:
- 안전 문구 반영 여부:
```

---

## 8. Step 4 — 대시보드 시각화

대시보드 필수 요소:

1. QS 추이 선 그래프
2. QS Breakdown 바 차트
3. AUTO / REVIEW / BLOCK 라우팅 카운트
4. 최근 세션 테이블
5. JATC 평균과 영역별 요약
6. 안전 문구 고정 표시

### Chart.js

- MVP에서는 CDN 사용 가능
- `dashboard.html`에서만 로드
- README에 “인터넷 연결이 없으면 Chart.js CDN이 로딩되지 않을 수 있음”을 기록

### Django 템플릿 보안

- `chart_data`는 `json_script`를 사용해 안전하게 전달
- 템플릿 안에서 복잡한 계산 금지

권장 데이터 구조:

```python
chart_data = {
    "labels": ["07-01", "07-02", "07-03"],
    "qs_scores": [82, 76, 91],
    "jatc_scores": [70, 68, 75],
    "routes": {
        "AUTO": 3,
        "REVIEW": 2,
        "BLOCK": 1
    },
    "breakdown": {
        "Form": 82,
        "Rep": 90,
        "Rest": 75,
        "Pain": 80
    }
}
```

라우팅은 색상만으로 의미를 전달하지 말고 텍스트 설명을 함께 표시합니다.

### Step 4 완료 로그

```text
[STEP 4] 대시보드 시각화
- 수정 파일:
- 구현 차트:
- 최근 세션 테이블:
- 라우팅 표시:
- 안전 문구 반영 여부:
```

---

## 9. Step 5 — Basic Report Generator

이번 MVP에서는 **HTML 리포트 우선**입니다.

PDF는 README의 향후 개발 항목으로만 남기고, 라이브러리를 추가하지 않습니다.

### 필수 구성

1. 리포트 상단 요약
2. 안전 문구
3. 회원 목표와 세션 정보
4. QS 총점
5. QS Breakdown
6. JATC 영역별 점수
7. AUTO / REVIEW / BLOCK 라우팅 의미
8. 3단계 방법론 기반 상담 요약
   - 파악
   - 회복
   - 트레이닝
9. 트레이너 검토 메모
10. print 버튼
11. 인쇄용 CSS

### 자동 생성 문장

AUTO:

```text
현재 입력된 운동 수행 기록 기준으로 기본 상담 리포트 생성이 가능합니다. 최종 상담 내용은 트레이너가 확인해 주세요.
```

REVIEW:

```text
일부 지표에서 확인이 필요한 항목이 있습니다. 트레이너가 운동 수행 기록과 회원 피드백을 함께 검토해 주세요.
```

BLOCK:

```text
높은 불편감 반응 또는 낮은 수행 품질이 기록되었습니다. 세션 진행 전 트레이너의 안전 확인이 필요하며, 불편감이 크거나 지속되면 적절한 전문가 상담을 권고할 수 있습니다.
```

### Step 5 완료 로그

```text
[STEP 5] Basic Report Generator
- 수정 파일:
- 리포트 구성:
- print 버튼:
- 인쇄용 CSS:
- 안전 문구 반영 여부:
```

---

## 10. Step 6 — Airtable 참고 스키마 문서

이번 MVP에서는 실제 Airtable API 연동을 구현하지 않습니다.  
대신 운영 데이터 설계를 문서화합니다.

생성 권장 파일:

```text
docs/airtable_schema.md
```

포함할 테이블:

1. PT 고도화 아이디어
2. 고객 인터뷰
3. 기능 요구사항
4. 버그
5. GitHub 이슈
6. 파일럿 센터
7. 리포트 템플릿
8. 법률/개인정보 확인 항목

각 테이블별 작성:

- 목적
- 필드명
- 필드 타입
- 상태값 옵션
- GitHub/Slack/Drive 연결 아이디어
- 개인정보 최소수집 원칙

주의:

- 실제 회원 이름, 전화번호, 이메일, 건강정보를 Airtable에 바로 넣는 구조로 설계하지 않습니다.
- Member ID 또는 익명 코드 기준으로 설계합니다.
- 민감 정보는 별도 보관 또는 수집 제외 원칙을 명시합니다.

### Step 6 완료 로그

```text
[STEP 6] Airtable 참고 스키마
- 생성 파일:
- 포함 테이블:
- 개인정보 최소수집 반영 여부:
```

---

## 11. Step 7 — synthetic seed/demo 데이터

초보자가 runserver 실행 후 바로 대시보드와 리포트를 확인할 수 있게 demo 데이터를 준비합니다.

기존 `seed_lightone.py`, `setup_dummy.py`, management command가 있다면 새 필드 기준으로 업데이트합니다.  
없다면 적절한 위치에 최소한의 demo 생성 방법을 추가합니다.

조건:

- 모든 데이터는 synthetic/demo 데이터
- 실제 인물처럼 보이는 개인정보 사용 금지
- 이름은 “데모회원 A”, “데모회원 B”, “DEMO-001” 형태 사용
- AUTO/REVIEW/BLOCK 데이터가 각각 최소 1개 이상 나오도록 구성

예시 메모:

```text
불편감 반응이 높게 기록되어 세션 진행 전 안전 확인이 필요합니다.
촬영/입력 조건 확인 후 트레이너 검토가 필요합니다.
기본 상담 리포트 생성 가능하나 최종 설명은 트레이너가 확인합니다.
```

### Step 7 완료 로그

```text
[STEP 7] synthetic demo 데이터
- 수정/생성 파일:
- demo 데이터 생성 방법:
- AUTO/REVIEW/BLOCK 포함 여부:
- 실제 개인정보 미사용 확인:
```

---

## 12. Step 8 — 테스트 작성

`python manage.py test`가 통과해야 합니다.

권장 파일:

- `app_name/tests/test_qs.py`
- `app_name/tests/test_models.py`
- `app_name/tests/test_views.py`

프로젝트 구조가 단순하면 `app_name/tests.py` 하나로 작성해도 됩니다.

### 필수 테스트

1. QS 계산이 가중치대로 되는지
2. pain_response 0~10 처리
3. Rep Achievement Rate 계산
4. Rest Compliance 계산
5. AUTO 라우팅 조건
6. REVIEW 라우팅 조건
7. BLOCK 라우팅 조건
8. JATC 계산
9. form validation
10. dashboard 페이지 200 응답
11. session_create POST 후 QS/JATC 계산
12. report_detail 페이지에 안전 문구 포함
13. synthetic demo 데이터가 실제 개인정보를 포함하지 않는지 기본 확인

실행:

```bash
python manage.py test
```

실패 시:

- 실패 원인 요약
- 수정한 파일
- 재실행 결과 기록

### Step 8 완료 로그

```text
[STEP 8] 테스트
- 작성 테스트:
- 실행 명령:
- 결과:
- 실패 수정 내역:
```

---

## 13. Step 9 — README 업데이트

README.md를 초보자도 10분 이내 실행할 수 있게 업데이트합니다.

포함할 내용:

1. LIGHT ONE V2 한 문장 정의
2. 비의료 PT 상담 리포트 SaaS 설명
3. 주요 기능
4. 폴더 구조
5. 설치 방법
6. venv 생성
7. requirements 설치
8. migrate
9. demo 데이터 생성
10. runserver
11. 주요 URL
12. QS 계산 방식
13. JATC 계산 방식
14. AUTO/REVIEW/BLOCK 의미
15. 안전 문구
16. Chart.js CDN 주의
17. 테스트 실행 방법
18. GitHub PR 확인 방법
19. 실제 운영 전 확인 필요 항목

반드시 포함할 문구:

```text
본 프로젝트는 비의료 운동상담 참고 자료를 생성하는 MVP입니다. 의료 진단, 치료, 처방, 재활 효과 판단을 제공하지 않으며, 최종 상담과 운동 진행 여부는 트레이너 검토가 필요합니다.
```

[확인필요] 항목:

- 개인정보보호법 검토
- 의료법 및 의료기기 오인 가능성 검토
- 실제 파일럿 데이터 기반 QS/JATC 임계값 검증
- 상용 배포 시 보안 설정 및 데이터 보관 정책 검토
- Airtable 등 외부 도구 연동 시 개인정보 처리 기준 검토

### Step 9 완료 로그

```text
[STEP 9] README
- 수정 파일:
- 실행 가이드 반영:
- 안전 문구 반영:
- [확인필요] 반영:
```

---

## 14. Step 10 — 전체 E2E 확인

최종 완료 전 아래 흐름을 확인합니다.

필수 확인:

1. `python manage.py check`
2. `python manage.py test`
3. `python manage.py migrate`
4. `python manage.py runserver` 실행 가능 여부
5. 대시보드 접속
6. 세션 입력
7. QS/JATC 자동 계산
8. AUTO/REVIEW/BLOCK 라우팅 표시
9. 최근 세션 테이블 표시
10. 리포트 상세 페이지 표시
11. print 버튼 또는 인쇄용 스타일 적용
12. 모든 주요 화면에 안전 문구 포함
13. 실제 개인정보/API 키/토큰 미사용 확인

가능하면 아래 형태로 수동 테스트 경로를 기록합니다.

```text
/ 또는 /dashboard/
/sessions/new/
/reports/<id>/
```

### Step 10 완료 로그

```text
[STEP 10] E2E 확인
- check 결과:
- test 결과:
- runserver 확인:
- 입력 → QS → 대시보드 → 리포트 흐름:
- 안전 문구 확인:
- 남은 문제:
```

---

## 15. 코드 품질 기준

- PEP8 준수
- 계산 로직은 순수 함수로 분리
- views는 orchestration 중심으로 유지
- templates에는 복잡한 계산을 넣지 않음
- 중복 코드 최소화
- 변수명은 명확하게 작성
- 주석은 필요한 곳에만 작성
- 새 dependency는 꼭 필요한 경우에만 추가
- 외부 API 연동은 이번 MVP에서 구현하지 않음
- API 키, 비밀번호, 토큰, 실제 개인정보를 코드/README/test에 넣지 않음
- 기존 기능을 깨지 않도록 작은 단위로 수정

---

## 16. GitHub PR 형태 정리

실제 PR을 만들 수 있다면 PR 설명을 작성합니다.  
PR을 만들 수 없다면 PR 본문 형태로 최종 요약을 남깁니다.

### PR 제목 예시

```text
feat: add QS/JATC engine, dashboard charts, and non-medical report MVP
```

### PR 본문 형식

```markdown
## Summary
- QS/JATC calculation engine added
- Dashboard visualization added
- HTML report generator added
- Synthetic demo data and tests added
- README updated

## Safety
- Non-medical disclaimer added
- No real member or health data used
- AUTO/REVIEW/BLOCK labels clarified
- BLOCK treated as safety check signal, not medical judgment

## Tests
- python manage.py check
- python manage.py test
- manual E2E flow checked

## Confirm Needed
- 개인정보보호법 검토
- 의료법/의료기기 오인 가능성 검토
- 파일럿 데이터 기반 임계값 검증
- 상용 배포 전 보안 설정 검토
```

---

## 17. 최종 출력 형식

모든 작업을 마친 뒤 아래 형식으로 최종 보고합니다.

```text
1. 변경 파일 목록
2. 핵심 구현 요약
3. Step별 완료 로그
4. 실행 명령어
5. 테스트 결과
6. E2E 확인 결과
7. 안전 문구 반영 여부
8. 실제 개인정보/API 키/토큰 미사용 확인
9. 남은 [확인필요] 항목
10. 다음 개발 제안 TOP 3
```

다음 개발 제안은 3개만 제시합니다.

우선순위 기준:

1. 실제 PT 현장 적용성
2. 개인정보/의료 오인 리스크 감소
3. 개발 난이도 대비 효과
