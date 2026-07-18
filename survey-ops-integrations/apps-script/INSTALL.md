# Apps Script integration guide

## 적용 원칙

`ExternalIntegrations.gs`는 현재 운영 중인 `doPost()`와 PDF·이메일 코드를 대체하지 않습니다. 기존 원본 처리 결과를 정규화한 뒤 마지막 단계에서만 호출합니다.

## 호출 예시

기존 코드가 Sheet 행, PDF 파일, 이메일 상태를 만든 직후 다음과 같이 연결합니다.

```javascript
const normalizedRecord = {
  response_id: responseId,
  client_request_id: clientRequestId,
  received_at: new Date().toISOString(),
  survey_title: 'AI 기반 PT 시스템 연구 설문지',
  source_version: '2026-07',
  role: roleKey, // owner | coach | member
  contact: {
    name: respondentName || '',
    organization: organization || '',
    reply_email: replyEmail || '',
    phone: phone || ''
  },
  comment: comment || '',
  consent: consent === '동의함' || consent === true,
  answers: answers,
  answer_summary: answerSummary,
  pdf: {
    file_id: pdfFile.getId(),
    file_name: pdfFile.getName(),
    url: pdfFile.getUrl()
  },
  email_status: emailStatus,
  process_status: processStatus,
  error_message: errorMessage || '',
  retry_count: retryCount || 0,
  updated_at: new Date().toISOString()
};

const integrationResult = syncExternalSystems_(normalizedRecord);
console.log(JSON.stringify({
  responseId: responseId,
  integrations: integrationResult
}));
```

## Script Properties

Apps Script 편집기에서 **프로젝트 설정 → 스크립트 속성**에 다음 값을 저장합니다.

| 키 | 값 | 보안 |
|---|---|---|
| `INTEGRATIONS_ENABLED` | 초기 `false`, 테스트 후 `true` | 일반 |
| `AIRTABLE_PAT` | Airtable Personal Access Token | 비밀 |
| `AIRTABLE_BASE_ID` | 설문 운영 베이스 ID | 내부 |
| `AIRTABLE_RESPONSES_TABLE` | `Responses` | 일반 |
| `AIRTABLE_LOG_TABLE` | `Integration Log` | 일반 |
| `SLACK_WEBHOOK_URL` | 전용 Incoming Webhook URL | 비밀 |
| `SLACK_INCLUDE_PDF_LINK` | 기본 `false` | 일반 |

## 단계별 테스트

1. `INTEGRATIONS_ENABLED=false`로 기존 설문 제출이 그대로 완료되는지 확인합니다.
2. Airtable 테스트 베이스와 Slack 테스트 채널을 준비합니다.
3. 합성 응답으로 `syncExternalSystems_()`만 단독 실행합니다.
4. Airtable에 연락처가 없고 Slack에 이름·전화·이메일·주관식이 없는지 확인합니다.
5. Webhook 또는 PAT를 일부러 잘못 설정해도 Google Sheet 원본이 보존되는지 확인합니다.
6. 정상 설정 후 `INTEGRATIONS_ENABLED=true`로 전환합니다.

## 롤백

문제가 발생하면 `INTEGRATIONS_ENABLED=false`로 변경합니다. 기존 Google Sheet·PDF·이메일 흐름은 유지되어야 합니다.

