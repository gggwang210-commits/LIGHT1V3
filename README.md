# LIGHT1V3

LightOne V1 기술 자산과 LightOne V2 Django 서비스를 통합하기 위한 실전형 Django 기반 저장소입니다.

이 저장소의 목표는 기존 LIGHTONE 기술 파일을 무리하게 본체에 섞지 않고, 핵심 상담 리포트 시스템은 안정적으로 유지하면서 촬영 품질 검사(QC), QS/JATC 분석, 트레이너 검토 흐름을 단계적으로 연결하는 것입니다.

## Project Vision

LIGHT1V3는 다음 방향을 기준으로 개발됩니다.

- Django 기반 LightOne V2 서비스를 제품 본체로 유지
- V1 기술 저장소의 카메라 보정, 조명 정규화, 촬영 품질 검사 기능을 선택적으로 통합
- `lightone_qc` 어댑터 레이어를 통해 QC 기능을 Feature Flag 방식으로 연결
- QC 실패나 외부 모듈 오류가 핵심 상담 리포트 생성 흐름을 중단하지 않도록 격리
- 회원, 트레이너, 센터 단위 권한 구조를 고려한 확장형 설계
- 실제 센터 파일럿 검증을 전제로 한 MVP 완성

## Core Architecture

LIGHT1V3
├─ Django Core Service
│  ├─ accounts
│  ├─ lightone
│  ├─ reports
│  └─ dashboard
│
├─ lightone_qc
│  ├─ contracts.py
│  ├─ service.py
│  └─ backends.py
│
├─ docs
│  ├─ GAP_MATRIX.md
│  ├─ adr-001-source-of-truth.md
│  └─ lightone-qc-adapter.md
│
└─ tests
   ├─ permission tests
   ├─ report flow tests
   └─ qc adapter tests

   Integration Strategy
LIGHT1V3는 두 저장소의 역할을 분리해서 통합합니다.
Source	Role
LIGHTONE	V1 기술 파일, 촬영 QC, 카메라 보정, 조명 정규화 참고 저장소
LightOne_V2	Django 서비스 본체 후보, 화면 및 리포트 흐름 기반
LIGHT1V3	정리된 통합 개발 저장소

핵심 원칙은 다음과 같습니다.
Django 서비스 본체는 안정성을 최우선으로 유지합니다.
V1 기술 기능은 직접 종속시키지 않고 lightone_qc 어댑터를 통해 호출합니다.
QC 기능은 기본값으로 비활성화하고, 환경변수 또는 설정값으로 켭니다.
QC 호출 실패, 타임아웃, 외부 라이브러리 누락은 리포트 본체를 중단시키지 않습니다.
운영 전 센터별 데이터 격리, 접근 권한, 동의 및 보관 정책을 검증합니다.
lightone_qc Adapter
lightone_qc는 V1 기술 파일과 Django 본체 사이의 완충 레이어입니다.
Django Report Flow
      │
      ▼
Feature Flag Check
      │
      ▼
lightone_qc.run_capture_check()
      │
      ▼
V1 QC Backend / Mock Backend / Disabled Backend
      │
      ▼
PASS / CHECK / FAIL / SKIPPED / UNAVAILABLE
상 동작 방식:
QC_ENABLED=False이면 QC는 실행되지 않고 SKIPPED 상태를 반환합니다.
QC 백엔드가 없거나 오류가 발생하면 UNAVAILABLE 상태를 반환합니다.
핵심 상담 리포트 생성은 QC 결과와 분리되어 계속 진행됩니다.
QC 결과는 상담 품질 보조 지표로만 사용됩니다.
Feature Flags
예시 환경변수:
QC_ENABLED=False
QC_BACKEND=disabled
QC_TIMEOUT_SECONDS=3
QC_RULESET_VERSION=v1
운영 단계에서는 다음처럼 활성화할 수 있습니다.
QC_ENABLED=True
QC_BACKEND=lightone_v1
QC_TIMEOUT_SECONDS=3
QC_RULESET_VERSION=v1
Development Priorities
현재 우선순위는 다음과 같습니다.
Django 본체 구조 안정화
회원, 트레이너, 센터 단위 권한 구조 정리
상담 리포트 생성 흐름 고정
lightone_qc 어댑터 테스트 강화
V1 QC 모듈과 실제 연결
실제 촬영 파일 기반 파일럿 검증
운영 배포 설정 및 보안 점검
Expected MVP Flow
Member
  → Capture Session
  → Optional QC Check
  → QS / JATC Analysis
  → Trainer Review
  → Report Approval
  → Member Report View
Tech Stack
Python
Django
SQLite for local development
PostgreSQL for production target
Pytest / Django TestCase
Optional OpenCV-based QC module
GitHub Actions for CI
Local Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Test
python manage.py test
Deployment Notes
운영 배포 전 반드시 확인해야 할 항목입니다.
DEBUG=False
SECRET_KEY 환경변수 관리
ALLOWED_HOSTS 설정
HTTPS 적용
파일 업로드 보안 검토
개인정보 수집, 보관, 파기 정책 정리
센터별 데이터 접근 제한 검증
관리자 및 트레이너 권한 테스트
실제 촬영 데이터 기반 QC 임계값 검증
Current Status
LIGHT1V3는 LightOne 통합 개발을 위한 기준 저장소입니다.
현재 방향은 “기술 파일 전체를 무리하게 병합”하는 방식이 아니라, Django 서비스 본체를 먼저 안정화하고 필요한 기술 기능을 어댑터 방식으로 연결하는 구조입니다.
이 방식은 다음 장점이 있습니다.
핵심 리포트 시스템 안정성 유지
V1 기술 모듈 교체 가능
QC 기능 점진적 활성화 가능
테스트와 배포 리스크 감소
향후 상용화 구조로 확장 가능
License
Private project for LightOne development.
