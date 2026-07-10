# LIGHT ONE V3

> PT 센터와 트레이너를 위한 비의료 운동상담 리포트 SaaS MVP

**Status:** Pilot MVP · Development  
**Default branch:** `Main-ONE`  
**Primary app:** `lightone_v2_django/`

---

## Overview

**LIGHT ONE V3**는 PT 센터와 트레이너가 회원의 운동상담 기록을 구조화하고, 세션별 검토 우선순위와 상담 리포트 초안을 관리할 수 있도록 지원하는 Django 기반 SaaS MVP입니다.

운동 목표, 수행 기록, 운동자각도(RPE), 불편 반응, 촬영 품질(QC), 트레이너 메모를 한곳에 정리하여 상담 준비와 회원 관리의 일관성을 높이는 것을 목표로 합니다.

현재 버전은 상용 서비스가 아니라 **센터 파일럿과 사용자 검증을 위한 개발 단계 MVP**입니다.

> **비의료 서비스 안내**  
> LIGHT ONE은 의료 진단, 치료, 처방, 재활 판정 또는 질병 위험 예측을 제공하지 않습니다.  
> 모든 점수와 리포트는 담당 트레이너의 검토를 전제로 하는 운동상담 참고 자료입니다.

---

## Problem and Solution

### 현장의 문제

- 회원 기록이 메신저, 메모, 문서 등에 분산됨
- 상담 전 과거 운동 반응을 다시 찾는 데 시간이 소요됨
- 트레이너별 기록 방식과 설명 수준이 일관되지 않음
- 추가 검토가 필요한 세션을 빠르게 구분하기 어려움

### LIGHT ONE의 접근

```text
회원·세션 기록
→ 입력값 및 촬영 QC 확인
→ 내부 참고 지표 계산
→ 검토 우선순위 분류
→ 상담 리포트 초안
→ 담당 트레이너 검토
→ 회원 상담 활용
```

AI와 점수 계산 로직은 트레이너의 판단을 대체하지 않습니다.

---

## Core Features

| 기능 | 설명 |
|---|---|
| 회원 관리 | 회원별 운동 목표와 상담 정보 관리 |
| 세션 기록 | 운동 수행, RPE, 불편 반응, 메모 기록 |
| 트레이너 대시보드 | 주요 세션과 검토 상태 요약 |
| QS·JATC 참고 지표 | 운동 관련 입력값을 조합한 내부 MVP 지표 |
| 검토 라우팅 | `AUTO`, `REVIEW`, `BLOCK` 우선순위 분류 |
| 상담 리포트 | 트레이너 검토용 상담 자료 초안 |
| 촬영 QC | 촬영 조건과 입력 신뢰도 확인 |
| 합성 데이터 | 실제 고객정보를 사용하지 않는 데모 데이터 |

---

## Routing Policy

| 상태 | 운영상 의미 |
|---|---|
| `AUTO` | 일반적인 트레이너 검토 절차로 진행 가능 |
| `REVIEW` | 불편 반응, 점수 또는 QC 항목의 추가 확인 필요 |
| `BLOCK` | 트레이너 확인 전 리포트 진행 보류 |

`AUTO`는 운동의 의학적 안전성을 보증하지 않습니다.

`BLOCK`은 질병, 응급 상태, 운동 금기 또는 치료 필요 판정이 아니라 **운영상 검토 보류 상태**입니다.

---

## Human-in-the-loop

LIGHT ONE의 결과 처리 원칙은 다음과 같습니다.

1. 시스템이 입력값을 정리합니다.
2. 내부 참고 점수와 검토 상태를 생성합니다.
3. 담당 트레이너가 원본 기록과 회원 상황을 확인합니다.
4. 필요한 내용을 수정하거나 제외합니다.
5. 검토된 내용만 상담 자료로 사용합니다.

회원에게 AI 결과가 자동으로 전달되는 구조를 지향하지 않습니다.

---

## Tech Stack

| 영역 | 기술 |
|---|---|
| Backend | Python, Django |
| Database | SQLite — 개발·파일럿 기준 |
| Frontend | Django Templates, HTML, CSS, JavaScript |
| Configuration | python-decouple |
| Test | Django Test, pytest, pytest-django |
| CI | GitHub Actions |
| Version Control | Git, GitHub |

### 주요 의존성

```text
Django>=5.0,<7.0
python-decouple>=3.8
pytest>=8.0
pytest-django>=4.8
```

Python 3.11 환경을 권장합니다.

---

## Repository Structure

```text
LIGHT1V3/
├── README.md
├── requirements.txt
├── docs/
├── tests/
├── sample_data/
├── assets/
├── lightone_v2_django/
│   ├── manage.py
│   ├── requirements.txt
│   ├── accounts/
│   ├── dashboard/
│   ├── lightone/
│   ├── mysite/
│   ├── static/
│   └── templates/
└── .github/
    └── workflows/
```

저장소 버전은 V3이지만 기존 코드와 경로 호환성을 위해 Django 디렉터리명은 `lightone_v2_django`를 유지하고 있습니다.

상세 기술·사업·검증 문서는 [`docs/`](docs/)에서 관리합니다.

---

## Quick Start

### 1. 저장소 복제

```bash
git clone https://github.com/gggwang210-commits/LIGHT1V3.git
cd LIGHT1V3
git checkout Main-ONE
```

### 2. 가상환경 생성

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 패키지 설치

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Django 실행 준비

```bash
cd lightone_v2_django
python manage.py migrate
python manage.py seed_lightone
```

`seed_lightone`은 로컬 데모 데이터와 테스트 계정을 생성합니다.

> 생성되는 계정은 로컬 개발 전용입니다.  
> 외부 배포 전 반드시 삭제하거나 환경변수 기반으로 변경해야 합니다.

### 5. 개발 서버 실행

```bash
python manage.py runserver
```

접속 주소:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/lightone/
http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/admin/
```

`runserver`는 개발용이며 운영 서버로 사용하지 않습니다.

---

## Validation

다음 명령으로 기본 상태를 확인합니다.

```bash
python manage.py check
python manage.py test
pytest
```

운영 배포 전에는 운영 설정을 적용한 상태에서 다음 검사를 수행해야 합니다.

```bash
python manage.py check --deploy
```

현재 저장소는 통합 리팩터링 단계이므로 모든 테스트 통과 상태를 보증하지 않습니다.

---

## Current Verification Status

| 항목 | 상태 |
|---|---|
| 제품 포지셔닝 | 비의료 PT 상담 리포트 SaaS |
| Django MVP 코드 | 구현 중 |
| 합성 데모 데이터 | 포함 |
| 실제 고객 데이터 사용 | 금지 |
| QS·JATC 임계값 검증 | `[검증필요]` |
| 전체 Django 테스트 | `[검증필요]` |
| 운영 배포 | 준비 전 |
| 개인정보·법률 검토 | `[검증필요]` |

### 우선 수정 항목

- `INSTALLED_APPS` 중복 등록 정리
- 모델 중복 정의와 필드 참조 검수
- migration 일관성 확인
- QS·JATC·라우팅 함수 인터페이스 통일
- GitHub Actions 대상 브랜치를 `Main-ONE`으로 수정
- 데모 계정과 비밀번호의 환경변수화
- 전체 테스트와 `check --deploy` 검증

---

## Privacy and Data Safety

개발과 데모 단계에서는 실제 회원정보 대신 합성 데이터를 사용합니다.

저장소에 포함하지 않아야 하는 항목:

```text
.env
API Key
SECRET_KEY
운영 데이터베이스
실제 회원 연락처
실제 건강정보
동의받지 않은 신체 이미지
상담 녹취 원본
인증정보와 비밀번호
```

실제 데이터 사용 전 다음 절차가 필요합니다.

- 개인정보 수집·이용 동의
- 데이터 최소 수집
- 역할별 접근권한
- 보유기간과 파기 기준
- 열람·수정·삭제 요청 처리
- 이미지 저장·삭제 정책
- 로그 및 관리자 작업 기록
- 외부 API와 위탁처리 검토

---

## Deployment Safety

운영 배포 전 최소 요구사항:

```text
DEBUG=False
SECRET_KEY 환경변수 주입
ALLOWED_HOSTS 제한
HTTPS 적용
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
개발 DB와 운영 DB 분리
정적·미디어 파일 정책 분리
로그·백업·오류 모니터링 적용
```

SQLite와 Django 개발 서버는 현재 로컬 MVP 검증 기준입니다.

---

## Non-medical Boundary

LIGHT ONE은 다음 기능을 제공하지 않습니다.

- 의료 진단
- 질병 분류 또는 위험 예측
- 통증 원인 확정
- 치료 또는 재활 처방
- 운동 금기 판정
- 응급 상태 판단
- AI 단독 의사결정
- 의료 전문가의 판단 대체

제공 범위는 다음으로 제한합니다.

- 운동상담 기록 구조화
- 운동 수행 흐름 확인
- 불편 반응 기록
- 입력 및 촬영 품질 확인
- 트레이너 검토 우선순위 지원
- 상담 리포트 초안 생성

---

## Pilot Validation

파일럿 단계에서 다음 지표를 검증합니다.

| 검증 영역 | 측정 항목 |
|---|---|
| 사용성 | 회원 1명 입력 시간 |
| 효율성 | 상담 준비 시간 변화 |
| 품질 | 리포트 수정 횟수 |
| 이해도 | 트레이너·회원 이해도 |
| 신뢰성 | 잘못된 라우팅 사례 |
| 지속성 | 재사용 의향 |
| 사업성 | 센터 월 구독 지불의사 |
| 안전성 | 개인정보·비의료 표현 오류 |

파일럿 데이터와 인터뷰 결과가 확보되기 전에는 성능, 효율 또는 수익성을 확정적으로 주장하지 않습니다.

---

## Roadmap

### P0 — 실행 안정화

- Django 설정과 모델 구조 정리
- migration 재구성
- 점수·라우팅 로직 단일화
- 기본 테스트 복구

### P1 — 검증 자동화

- `Main-ONE` 기준 CI 수정
- 경계값 단위 테스트
- 비의료 표현 검사
- 보안 설정 검사

### P2 — 파일럿

- 트레이너 1~2명 사용성 테스트
- 입력·상담 시간 측정
- 리포트 이해도 검증
- 가격 지불의사 인터뷰

### P3 — 운영 준비

- PostgreSQL 전환
- 역할 기반 접근제어
- 감사 로그
- 데이터 삭제 기능
- 배포 환경 분리
- 모니터링과 백업

---

## Documentation Policy

문서 간 내용이 충돌하는 경우 다음 순서를 우선합니다.

1. 루트 `README.md`
2. `docs/`의 최신 기준 문서
3. Django 앱 내부 문서
4. 이전 버전 및 보관 문서

오래된 문서에는 V1 또는 V2 명칭과 이전 제품 가정이 포함될 수 있습니다.

---

## License and Assets

프로젝트 코드, 디자인 자산, 폰트, 이미지 및 외부 라이브러리의 배포 조건은 `[검증필요]`입니다.

공개 또는 상용 배포 전 다음 문서 추가를 권장합니다.

```text
LICENSE
SECURITY.md
CONTRIBUTING.md
THIRD_PARTY_NOTICES.md
ASSET_LICENSE.md
```

---

## Project Principle

> LIGHT ONE V3는 트레이너를 대체하는 시스템이 아닙니다.  
> 회원의 운동상담 기록을 구조화하고, 트레이너가 더 일관되고 설명 가능한 상담을 수행하도록 지원하는 비의료 업무 보조 도구입니다.
