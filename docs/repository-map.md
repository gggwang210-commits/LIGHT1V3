# LIGHT ONE V3 저장소 맵

이 문서는 저장소 루트에서 어떤 문서를 먼저 읽고, 어떤 폴더가 어떤 역할을 하는지 빠르게 파악하기 위한 안내서입니다. 첫 번째 사업 방향은 [business_direction](business_direction.md), 전체 소개는 [루트 README](../README.md), Django MVP 실행과 기능은 [Django README](../lightone_v2_django/README.md), Windows 실행 절차는 [기존 RUN_WINDOWS](../lightone_v2_django/RUN_WINDOWS.md)와 [Windows 실행 가이드](execution-guide/windows-run-guide.md)를 함께 확인합니다.

## 1. 최상위 문서

| 경로 | 역할 | 먼저 볼 사람 |
|------|------|--------------|
| [`README.md`](../README.md) | LIGHT ONE V3의 사업 전략, 제품 포지셔닝, 비의료 경계, 시장 진출 계획 | 심사자, 사업 검토자, 신규 기여자 |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | 개발 절차, 검증 명령, 데이터·표현 규칙 | 개발자, 리뷰어 |
| [`CHANGELOG.md`](../CHANGELOG.md) | 주요 저장소 변경 이력과 미출시 변경 | 개발자, 채용 검토자 |
| [`docs/README.md`](README.md) | 루트 `docs/`의 canonical documents와 reference / legacy materials를 구분하는 문서 허브 | 모든 신규 참여자 |
| [`docs/repository-map.md`](repository-map.md) | 문서와 코드 위치를 연결하는 저장소 지도 | 모든 신규 참여자 |
| [`docs/architecture.md`](architecture.md) | 활성 컴포넌트, 데이터 흐름, 설정·신뢰 경계 | 기술 검토자, 개발자 |
| [`docs/release-checklist.md`](release-checklist.md) | 로컬 데모와 운영 준비 상태를 구분하는 게이트 | 보안, 운영, PM |
| [`docs/business_direction.md`](business_direction.md) | 트레이너·회원 컨디셔닝 대시보드 SaaS라는 첫 번째 사업 목표 | 대표, PM, 기획, 개발, 디자인 |
| [`docs/governance/non-medical-boundary.md`](governance/non-medical-boundary.md) | 의료 오인 방지를 위한 표현·기능 경계 | 기획, 디자인, 개발, 영업 |
| [`docs/governance/privacy-checklist.md`](governance/privacy-checklist.md) | 개인정보·민감정보 취급 점검표 | 운영, 개발, 파일럿 담당 |
| [`docs/validation/pilot-validation-plan.md`](validation/pilot-validation-plan.md) | 파일럿 검증 목표, 지표, 절차 | 대표, PM, 파일럿 센터 담당 |
| [`docs/submission/modu-startup-summary.md`](submission/modu-startup-summary.md) | 모두의창업 2기 제출용 요약 | 심사 대응, 제안서 작성자 |
| [`docs/execution-guide/windows-run-guide.md`](execution-guide/windows-run-guide.md) | 루트 기준 Windows 실행 안내 | 비개발자, Windows 사용자 |

## 2. Canonical documents

최신 사업/제품 포지셔닝은 루트 `docs/`의 canonical documents를 기준으로 합니다. 오래된 문서나 다른 폴더의 자료는 현재 포지셔닝과 다를 수 있으므로 참고 자료로만 사용합니다.

| 경로 | 역할 | 상태 |
|------|------|------|
| [`docs/business_direction.md`](business_direction.md) | 첫 번째 사업 목표와 제품 방향 기준 문서 | canonical |
| [`docs/LIGHT_ONE_final_business_plan_v1_2026-07-07.md`](LIGHT_ONE_final_business_plan_v1_2026-07-07.md) | 최종 사업계획서 기준본 | canonical |
| [`docs/product_positioning.md`](product_positioning.md) | 제품 포지셔닝 기준 문서 | canonical |
| [`docs/mvp_scope.md`](mvp_scope.md) | MVP 범위와 제외 범위 기준 문서 | canonical |
| [`docs/safety_and_privacy_policy.md`](safety_and_privacy_policy.md) | 안전·개인정보 정책 기준 문서 | canonical |
| [`docs/technical_roadmap.md`](technical_roadmap.md) | 기술 개발 로드맵 기준 문서 | canonical |
| [`docs/customer_validation_plan.md`](customer_validation_plan.md) | 고객 검증 계획 기준 문서 | canonical |
| [`docs/pitch_summary.md`](pitch_summary.md) | 발표·피치 요약 기준 문서 | canonical |
| [`docs/judge_risk_review.md`](judge_risk_review.md) | 심사 리스크와 G0~G4 실행 게이트 기준 문서 | canonical |

> 일부 canonical 문서는 아직 작성 예정일 수 있습니다. 작성 시 위 경로와 파일명을 유지합니다.

## 3. Reference / legacy materials

아래 자료는 과거 구현, 검토 과정, 아이디어 흐름을 보존하기 위한 참고/레거시 자료입니다. 현재 포지셔닝과 다른 내용이 포함될 수 있지만, 히스토리 추적을 위해 삭제하지 않습니다.

| 경로 | 상태 | 사용 원칙 |
|------|------|-----------|
| [`lightone_v2_django/docs/`](../lightone_v2_django/docs/) | reference / legacy | Django MVP 구현·운영 참고 자료로 사용 |
| [`2/repo_lightoneV2/`](../2/repo_lightoneV2/) | reference / legacy | 이전 V2 자산과 작업물 확인용으로 보존 |
| [`아이디어-구상/`](../아이디어-구상/) | reference / legacy | 초기 아이디어와 문제 정의 히스토리 확인용으로 보존 |
| [`legacy/`](../legacy/) | archive | 이전 구현·복제 자산을 회귀 조사 목적으로만 보존 |
| [`legacy-docs/`](../legacy-docs/) | archive | 이전 기준 문서의 히스토리 보존 |
| [`lightone-main/`](../lightone-main/) | archive | 과거 저장소 스냅샷 참고 |
| [`lightone_django/`](../lightone_django/) | archive | 이전 Django 구현 참고 |

## 4. Django MVP 영역

| 경로 | 역할 |
|------|------|
| [`lightone_v2_django/README.md`](../lightone_v2_django/README.md) | MVP 소개, 빠른 시작, 계정, 기능 URL, 위험 라우팅 기준 |
| [`lightone_v2_django/RUN_WINDOWS.md`](../lightone_v2_django/RUN_WINDOWS.md) | Django 폴더 내부에서 실행하는 간단한 Windows 명령 |
| `lightone_v2_django/manage.py` | Django 관리 명령 진입점 |
| `lightone_v2_django/requirements.txt` | Python 패키지 의존성 |
| `lightone_v2_django/lightone/` | LIGHTONE 앱의 모델, 뷰, 템플릿, 관리 명령 영역 |

## 5. 문서 사용 순서

1. 사업 방향과 규제 경계를 이해하려면 [루트 README](../README.md)와 [docs README](README.md)를 먼저 읽습니다. 최신 사업/제품 포지셔닝은 루트 `docs/`의 canonical documents를 기준으로 합니다.
2. 의료 표현을 만들기 전에 [비의료 경계 문서](governance/non-medical-boundary.md)를 확인합니다.
3. 회원 데이터, 이미지, 상담 기록을 다루기 전에 [개인정보 체크리스트](governance/privacy-checklist.md)를 적용합니다.
4. 센터 파일럿을 시작하기 전에 [심사 리스크 검토](judge_risk_review.md)와 [파일럿 검증 계획](validation/pilot-validation-plan.md)의 동의, 지표, 중단 기준을 확정합니다.
5. Windows에서 MVP를 실행할 때는 [Windows 실행 가이드](execution-guide/windows-run-guide.md)를 사용하고, 세부 앱 설명은 [Django README](../lightone_v2_django/README.md)를 참조합니다.

## 6. 문서 관리 원칙

- 최신 사업/제품 포지셔닝은 루트 `docs/`의 canonical documents를 기준으로 합니다.
- 루트 `README.md`는 사업 전략의 입문 문서입니다.
- `docs/governance/`는 서비스 표현, 개인정보, 운영 리스크의 기준 문서입니다.
- `docs/validation/`은 가설 검증과 파일럿 결과를 기록하는 영역입니다.
- `docs/submission/`은 외부 제출용 요약 문서를 보관하는 영역입니다.
- reference / legacy materials는 현재 포지셔닝과 다를 수 있음을 표시하고, 히스토리 보존을 위해 삭제하지 않습니다.
- 실행 방법이 바뀌면 `lightone_v2_django/README.md`, `lightone_v2_django/RUN_WINDOWS.md`, `docs/execution-guide/windows-run-guide.md`를 함께 갱신합니다.
- 과거 구현은 `legacy/README.md`의 원칙을 따르며 새 기능을 복제하지 않습니다.
