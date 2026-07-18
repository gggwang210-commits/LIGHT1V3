# LIGHT ONE Survey Operations Integration Pack

LIGHT ONE의 **AI 기반 PT 시스템 연구 설문지**를 기존 Google Apps Script 운영 흐름과 분리하지 않고, Google Drive·Airtable·Slack·GitHub·Hugging Face용 구조로 안전하게 확장하는 운영 자료입니다.

## 현재 확인된 운영 구조

- 공개 설문: Google Apps Script 웹 앱
- 응답자 유형: 센터장·원장, 트레이너, 회원
- 문항 수: 역할별 15개, 총 45개
- 기존 처리: Google Sheet 저장 → PDF 생성 → 대표 이메일 전달
- 본 패키지: 기존 처리 성공 후 Airtable 동기화와 비식별 Slack 알림을 선택적으로 추가

> 이 저장소에는 실제 이름, 전화번호, 이메일, 응답 PDF, 운영 토큰을 포함하지 않습니다. `data/sample_response.json`은 합성 데이터입니다.

## 권장 아키텍처

```text
설문 제출
  -> Apps Script 기존 검증/중복방지
  -> Google Sheet 원본 저장
  -> PDF 생성 및 이메일 전달
  -> ExternalIntegrations.gs
       -> Airtable 운영 레코드(연락처 제외)
       -> Slack 상태 알림(연락처/주관식 제외)
       -> 통합 로그

비식별 분석이 필요할 때만
  -> public-export.schema.json 기준으로 별도 내보내기
  -> 비공개 Hugging Face Dataset 저장소에서 검토
```

## 폴더 구성

| 경로 | 용도 |
|---|---|
| `apps-script/` | 기존 Apps Script에 추가하는 외부 연동 어댑터 |
| `schemas/` | 내부 응답 및 비식별 공개용 JSON Schema |
| `data/` | 역할별 45문항 카탈로그와 합성 예시 |
| `airtable/` | Airtable 테이블 설계 및 필드 매핑 |
| `slack/` | 비식별 알림 템플릿과 운영 규칙 |
| `huggingface/` | 비공개 Dataset용 데이터 카드 초안 |
| `scripts/` | 문항 수, JSON, 비밀정보 패턴을 점검하는 검증 스크립트 |
| `docs/` | 설치, 개인정보, 장애 대응 기준 |

## 빠른 적용

1. Airtable에 `Responses`, `Question Catalog`, `Integration Log`, `Config` 테이블을 준비합니다.
2. Apps Script의 **프로젝트 설정 → 스크립트 속성**에 필요한 값을 저장합니다.
3. `apps-script/ExternalIntegrations.gs`를 프로젝트에 추가합니다.
4. 기존 제출 처리의 Sheet/PDF/이메일 성공 직후 `syncExternalSystems_(normalizedRecord)`를 호출합니다.
5. 실제 응답이 아닌 합성 데이터로 Airtable과 Slack 전송을 먼저 확인합니다.

필수 스크립트 속성:

```text
AIRTABLE_PAT
AIRTABLE_BASE_ID
AIRTABLE_RESPONSES_TABLE
AIRTABLE_LOG_TABLE
SLACK_WEBHOOK_URL
INTEGRATIONS_ENABLED=true
```

`AIRTABLE_PAT`와 `SLACK_WEBHOOK_URL`은 절대 코드·GitHub·Sheet 셀에 저장하지 않습니다.

## 로컬 검증

Node.js 20 이상에서 다음 명령을 실행합니다.

```bash
npm run validate
```

검증 항목:

- 역할별 문항 15개와 전체 45개 여부
- 질문 키의 중복 여부
- JSON 파일 구문
- 합성 응답에 실제 연락처가 포함되지 않았는지 여부
- 저장소 내 토큰·웹훅 형태의 문자열 여부

## 데이터 경계

| 저장소 | 허용 데이터 | 금지 데이터 |
|---|---|---|
| Google Drive/Sheet | 동의받은 운영 원본, PDF, 연락처 | 계정 비밀번호, 주민등록번호, 의료 진단자료 |
| Airtable | 응답 ID, 역할, 상태, 비식별 요약, PDF 접근 URL | 이름·전화·이메일 기본 동기화 |
| Slack | 응답 ID, 역할, 처리 상태, 오류 요약 | 연락처, 자유서술 원문, 건강 관련 상세내용 |
| GitHub | 코드, 스키마, 합성 예시 | 실제 응답, `.env`, 토큰, 운영 PDF |
| Hugging Face | 비식별 집계/합성 데이터, 비공개 검토본 | 원본 연락처, 재식별 가능한 자유서술 |

## 비의료 안내

본 설문과 통합 자료는 PT 상담 운영 및 서비스 고도화 연구용입니다. 의료 진단, 치료, 처방, 재활 판정 또는 질병 위험 예측을 제공하지 않습니다.

