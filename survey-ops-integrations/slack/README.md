# Slack notification policy

Slack은 응답 원문 저장소가 아니라 처리 상태를 빠르게 확인하는 알림 채널로만 사용합니다.

## 전송 허용

- 응답 ID
- 응답자 역할
- 처리 상태와 이메일 상태
- 업데이트 시각
- 개인정보가 제거된 짧은 오류 요약

## 전송 금지

- 이름, 센터명, 이메일, 전화번호
- 자유서술 원문
- 개별 답변 15개 전체
- PDF 파일 자체 또는 공개 공유 링크
- Airtable PAT, Slack Webhook, Apps Script 설정값

`SLACK_INCLUDE_PDF_LINK` 기본값은 `false`입니다. 링크가 꼭 필요한 경우에도 Drive 접근권한을 제한하고 내부 채널에서만 사용합니다.

