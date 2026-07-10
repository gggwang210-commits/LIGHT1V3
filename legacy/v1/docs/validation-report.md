# LIGHT ONE 파일 분석·검증·정보화 리포트

작성일: 2026-06-29
대상 ZIP: files (3).zip
대상 프로젝트: LIGHT ONE

## 1. 결론

첨부 ZIP은 코드 실행 파일이 아니라 LIGHT ONE의 기술 문서 패키지입니다. GitHub 반영 우선순위는 `docs/technical-framework.md`, `docs/data-schema.md`, `docs/roadmap.md`, `docs/validation-report.md` 순서가 적절합니다.

현재 문서는 MVP 기획·심사·협업 공유용으로는 사용 가능하지만, 실제 회원 데이터 수집, 의료적 표현, 기준 수치, 논문·버전 출처는 일부 [확인필요] 상태로 표시해야 합니다.

## 2. 파일 인벤토리

| 파일 | 성격 | 중요도 | 판단 |
|---|---|---:|---|
| docs_technical-framework.md | QS/JATC 기술 프레임워크 | 높음 | 핵심 설명 문서. 심사·기획·README 연결에 적합 |
| docs_data-schema.md | Django 모델·CSV 스키마 | 높음 | 구현 전환용 기준 문서. 개인정보 경계 포함 |
| docs_roadmap.md | 1~3단계 기술 로드맵 | 높음 | 발표·지원사업용 계획 문서. 일부 수치 근거 확인 필요 |
| github_push_commands.sh | 로컬 Git push 안내 스크립트 | 중간 | 자동 실행보다는 참고용. 직접 실행 전 레포 상태 확인 필요 |

## 3. 핵심 정보화 요약

### 3.1 제품 정의

LIGHT ONE은 비의료 운동상담 보조 SaaS입니다. 트레이너가 입력한 운동 수행, 통증 자기보고, 자세 관찰, 생활습관 정보를 바탕으로 상담 리포트를 자동 생성하고, 위험 신호는 Human-in-the-loop 방식으로 트레이너 검토에 넘기는 구조입니다.

### 3.2 핵심 지표

| 지표 | 의미 | 주요 입력 | 산출/활용 |
|---|---|---|---|
| QS | Quality Score, 수행 품질지수 | 폼 정확도, 반복수 달성률, 휴식 준수, 통증 반응 | 세트·세션 단위 수행 품질 평가 |
| JATC | Joint Achievement & Tracking Composite, 통합 상태지수 | 통증, 자세, 근기능, 생활습관 | 회원 상태 변화 추적 및 상담 리포트 요약 |
| Routing | AUTO/REVIEW/BLOCK | QS, JATC, 통증 변화, 자세 변화 | 자동 진행, 트레이너 검토, 부하 조정/중단 판단 보조 |

### 3.3 단계별 로드맵

| 단계 | 기간 | 목표 | 핵심 산출물 |
|---|---|---|---|
| Phase 1 | 현재~2개월 | 규칙 기반 MVP | Django 상담 입력폼, 리포트 자동 생성, 더미데이터 데모 |
| Phase 2 | 3~6개월 | ML 기반 패턴 분석 | XGBoost/LightGBM, MediaPipe/OpenPose 연동 검토, 데이터 검증 |
| Phase 3 | 6~12개월 | 개인화 AI 추천 | 다음 세션 제안, 통증 위험 신호 탐지, 대시보드 고도화 |

## 4. 검증 결과

### 4.1 사용 가능 판단

- MVP 문서 구조는 적절합니다.
- 실제 고객 데이터가 아닌 더미 데이터 기반이라는 경계가 명시되어 있습니다.
- 의료 진단이 아닌 트레이너 상담 보조라는 표현은 방향성이 안전합니다.
- GitHub `docs/` 폴더에 넣어 프로젝트 기술 문서로 관리하기 좋습니다.

### 4.2 수정 또는 보완 필요

| 항목 | 현재 위험 | 권장 수정 |
|---|---|---|
| 의료 표현 | 통증 위험 신호, 전문가 상담 권고가 의료 판단처럼 보일 수 있음 | “의료 진단·치료 판단 아님”, “운동 상담 참고용” 반복 표기 |
| 개인정보 | 실제 회원 데이터 수집 시 민감정보 가능성 있음 | 수집 전 동의서, 보관기간, 접근권한, 삭제절차 문서화 |
| IRB | 연구·논문화·외부 검증 시 필요 가능성 | 사업용 MVP와 연구용 데이터 수집을 분리 |
| 기준 수치 | 2.5m, 500lux, ICC ≥ 0.75, 파일럿 1,440세션 등 | 내부 가정값으로 표시하거나 공식/논문 근거 추가 |
| ACSM 2025 | 문서 내 12판 표기 확인 필요 | 공식 출판 정보 재확인 전 [확인필요] 유지 |
| OpenPose v1.7.0 | GitHub 릴리스는 확인 가능 | 단, 실제 적용성은 설치환경·라이선스·성능 테스트 필요 |
| GitHub push 스크립트 | main에 직접 push하는 구조 | 별도 브랜치 + PR 방식 권장 |

## 5. GitHub 반영 권장 구조

```text
docs/
  technical-framework.md
  data-schema.md
  roadmap.md
  validation-report.md
```

권장 브랜치명:

```text
docs/lightone-qs-jatc-framework
```

권장 커밋 메시지:

```text
docs: add LIGHT ONE QS/JATC framework and validation report
```

## 6. Airtable 정보화 권장 테이블

| 테이블 | 목적 |
|---|---|
| Document Inventory | 파일명, 분류, 중요도, 상태 관리 |
| Validation Issues | 확인필요 항목, 위험도, 조치 상태 관리 |
| Roadmap Tasks | Phase별 실행 과제 관리 |

## 7. Slack 공유용 요약

LIGHT ONE 문서 ZIP 검토 결과, 기술 프레임워크·데이터 스키마·로드맵 3개 핵심 문서와 GitHub push 참고 스크립트로 구성되어 있습니다. MVP 기획 문서로는 사용 가능하지만, 실제 회원 데이터 수집, 의료적 표현, IRB, 개인정보, 기준 수치 근거는 [확인필요] 상태로 관리해야 합니다. GitHub에는 `docs/` 폴더로 반영하고, main 직접 push보다 브랜치 생성 후 PR 방식이 안전합니다.

## 8. 즉시 실행 권장 순서

1. GitHub `docs/` 폴더에 문서 3개와 검증 리포트 추가
2. Google Drive에 검증 리포트 보관
3. Slack Canvas에 요약본 공유
4. Airtable에 파일 인벤토리·검증 이슈·로드맵 태스크를 구조화
5. 이후 Codex에는 “문서 기반으로 Django MVP 입력폼·리포트 생성 기능을 구현하라”는 작업 프롬프트 전달
