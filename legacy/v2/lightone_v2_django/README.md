# LIGHT ONE V2 — PT 상담 판단 보조 서비스 Django MVP

> **프로의 기준, 이제는 데이터입니다.**  
> Data-Driven, Evidence-Based Personal Training

---

## 이 프로젝트는 무엇인가요?

LIGHT ONE은 PT(퍼스널 트레이닝) 현장에서 회원의 운동 기록, 불편감 반응 수치, 운동자각도(RPE), 자세 관찰 데이터를 구조화하여 트레이너의 판단을 보조하는 **데이터 기반 PT 상담 보조 서비스**입니다.

- AI가 트레이너를 대체하는 것이 아니라, **트레이너의 판단을 보조**합니다.
- 의료적 진단·치료·처방을 대체하지 않습니다.
- 현재 버전은 **가상 데이터(더미 데이터)** 기반의 MVP입니다.

---

## 처음 실행하는 분은 여기부터!

**👉 `docs/초보자_실행가이드.md` 파일을 먼저 읽어주세요!**

Python 설치부터 서버 실행까지 따라할 수 있도록 Windows 기준으로 단계별 설명이 정리되어 있습니다.

---

## 현재 기준 실행 경로

| 항목 | 최신 기준 |
|---|---|
| Django 프로젝트 폴더 | `lightone_v2_django` |
| 패키지 목록 | `requirements.txt` |
| 실행 파일 | `manage.py` |
| 더미 데이터 명령 | `python manage.py seed_lightone` |
| 접속 URL | `http://127.0.0.1:8000/lightone/` |

> 구버전 안내: 예전 문서의 `lightone_django`, `lightone_django_complete.zip`, `LIGHTONE_V2_Complete.zip`, `python setup_dummy.py`, `http://127.0.0.1:8000` 안내는 현재 기준으로는 위 표를 따르세요.

---

## 빠른 시작 (이미 Python이 설치된 분)

```bash
# 저장소 루트에서 시작했다면 Django 폴더로 이동
cd lightone_v2_django

# 1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
                            # Windows CMD: .venv\Scripts\activate.bat

# 2. 패키지 설치
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. DB 세팅 및 더미 데이터 입력
python manage.py migrate
python manage.py seed_lightone

# 선택: 비식별 합성 fixture 로드
python manage.py loaddata synthetic_step1

# 4. 서버 실행
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/lightone/` 접속

---

## 비식별 합성 fixture 로드

`lightone/fixtures/synthetic_step1.json`은 개발·검증용 합성 데이터입니다. 직접 식별정보인 이름, 전화번호, 이메일, 주소, 생년월일을 포함하지 않으며, 회원 코드는 실제 인물을 나타내지 않는 비식별 코드입니다.

포함 범위:

- 합성 회원 3명
- 회원별 세션 1~2개
- 각 세션의 QS/JATC 및 라우팅 지표 예시
- `AUTO`, `REVIEW`, `BLOCK` 라우팅 예시 전체
- `age_group`, `gender`, `goals`, 동의 여부 예시값

로드 방법:

```bash
cd lightone_v2_django
python manage.py migrate
python manage.py loaddata synthetic_step1
```

> fixture는 현재 Django 모델의 필드명에 맞춰 `route` 필드에 라우팅 값을 저장합니다. 문서와 데이터 메모에서는 새 지표 용어인 `routing_status`를 함께 표기합니다.

---

## 기본 계정 (`seed_lightone` 기준)

| 역할 | 아이디 | 비밀번호 |
|------|--------|----------|
| 관리자/트레이너 | `admin` | `admin` |
| 회원 | `member1` | `1234` |
| 회원 | `member2` | `1234` |

---


## MVP 개발 체크리스트 진행 로그 (2026-07-06)

- Step 0: 프로젝트 구조를 확인했고 Django 앱 경로는 `lightone_v2_django`입니다. `python manage.py check` 통과 상태입니다.
- Synthetic 데이터만 사용합니다. `seed_lightone` 명령은 데모 계정과 가상 회원 세션만 생성하며 실제 회원 정보 입력을 금지합니다.
- Step 1: `MemberSession`에 QS/JATC breakdown, QC 점수, 안전 문구 필드를 추가했습니다. 개인정보는 이름/목표/불편감 메모 수준의 MVP 데모 필드로 제한하고 운영 전 익명 식별자 전환이 필요합니다.
- Step 2: QS 0.4/0.3/0.2/0.1 가중 평균, JATC 종합 점수, AUTO/REVIEW/BLOCK 라우팅 함수를 구현하고 테스트를 추가했습니다.
- Step 3: 대시보드에 QS 추이 선 그래프, QS breakdown 바 차트, 라우팅 색상, 최근 세션 테이블을 추가했습니다.
- Step 4: 상세 리포트에 Basic HTML Report Generator 섹션과 필수 안전 문구를 표시합니다.
- Step 5: URL/View/Form 연결을 유지하고 세션 입력에서 QC 상태와 QC 점수를 함께 기록합니다.
- Step 6: 전체 테스트는 `python manage.py test`로 확인합니다. runserver E2E는 로컬 실행 후 `/lightone/session/new/` → `/lightone/` → `/lightone/report/<id>/` 흐름으로 확인하세요.

필수 문구: **비의료 운동상담 참고, 트레이너 검토 필요**

## 주요 기능

| 기능 | URL | 설명 |
|------|-----|------|
| 로그인 | `/accounts/login/` | 회원/트레이너 계정 분리 |
| 대시보드 | `/lightone/` | 회원 목록 및 QS 현황 |
| 세션 입력 | `/lightone/session/new/` | 운동 기록, 불편감 반응, RPE 입력 |
| 리포트 | `/lightone/report/<id>/` | 회원별 상세 리포트 |
| 관리자 | `/admin/` | Django 관리자 페이지 |

---

## 위험 라우팅 기준 (AUTO / REVIEW / BLOCK)

| 라우팅 | 조건 | 의미 |
|--------|------|------|
| **AUTO** (초록) | 불편감 반응 < 4 & QS ≥ 70 | 일반 진행 가능 |
| **REVIEW** (노랑) | 불편감 반응 4–6 또는 QS 40–70 | 트레이너 검토 필요 |
| **BLOCK** (빨강) | 불편감 반응 ≥ 7 또는 QS < 40 | 안전상 중단 권고 신호 (의료 진단 아님) |

> 현재 QS/JATC 및 AUTO/REVIEW/BLOCK 임계값은 MVP 데모용 내부 초안이며 의료 판단 기준이 아닙니다. 파일럿 데이터와 전문가 검토 후 조정이 필요하고, BLOCK은 진단이 아니라 운동 세션 중단 및 전문가 상담 권고 신호입니다.
>
> BLOCK은 의료적 진단이 아니라 안전 신호입니다. 최종 판단은 트레이너가 합니다.

---

## 포함된 문서 목록 (`docs/` 폴더)

| 문서 | 내용 |
|------|------|
| `초보자_실행가이드.md` | Python 설치부터 서버 실행까지 단계별 안내 |
| `프로젝트_구조_설명.md` | 폴더/파일 구조 및 핵심 개념 설명 |
| `기능_개발_가이드.md` | 다음 기능 추가 방법 (대시보드, PDF 리포트 등) |
| `전략서_및_인포그래픽/` | 사업 기획 문서 및 인포그래픽 Rev.5 |
| [`../docs/repository-map.md`](../docs/repository-map.md) | 저장소 루트 문서 지도 및 신규 기여자 안내 |
| [`../docs/governance/non-medical-boundary.md`](../docs/governance/non-medical-boundary.md) | 비의료 표현·기능 경계와 라우팅 문구 기준 |
| [`../docs/governance/privacy-checklist.md`](../docs/governance/privacy-checklist.md) | 개인정보·민감 기록 취급 체크리스트 |
| [`../docs/validation/pilot-validation-plan.md`](../docs/validation/pilot-validation-plan.md) | 센터 파일럿 검증 목표와 운영 절차 |
| [`../docs/submission/modu-startup-summary.md`](../docs/submission/modu-startup-summary.md) | 모두의창업 2기 제출용 요약 |
| [`../docs/execution-guide/windows-run-guide.md`](../docs/execution-guide/windows-run-guide.md) | 저장소 루트 기준 Windows 실행 가이드 |

---

## 기술 스택

- **Backend:** Python 3.11 + Django 4.2
- **Database:** SQLite (개발용) / PostgreSQL (배포용)
- **Frontend:** HTML/CSS/JavaScript + Chart.js
- **인증:** Django 커스텀 유저 모델 + 로그인 미들웨어
- **배포:** GCP + Nginx + Gunicorn (`deploy.sh` 참고)

---

## 주의사항

- 본 서비스는 비의료 운동상담 보조 도구입니다.
- 현재 버전의 QS 점수 산식은 내부 규칙 기반이며, 실제 센터 데이터로 검증이 필요합니다.
- 개인정보보호법, 의료법 관련 사항은 서비스 출시 전 전문가 확인이 필요합니다. [확인필요]

---

추가로, 전체 사업 방향은 [루트 README](../README.md), Windows 간단 실행은 [RUN_WINDOWS.md](RUN_WINDOWS.md)를 참고하세요.

**LIGHT ONE V2 · Rev.05 · 2026.07.01**
