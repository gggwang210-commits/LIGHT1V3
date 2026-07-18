# Architecture and operating decisions

## 1. Source of truth

Google Sheet와 Google Drive PDF를 운영 원본으로 유지합니다. Airtable과 Slack은 원본 저장소가 아니라 운영 조회와 알림을 위한 보조 계층입니다.

## 2. Delivery sequence

1. 요청 형식과 동의 여부 확인
2. `CLIENT_REQUEST_ID` 또는 `RESPONSE_ID`로 중복 제출 방지
3. Google Sheet 원본 기록
4. PDF 생성
5. 대표 이메일 전달
6. Airtable 비식별 운영 레코드 동기화
7. Slack 비식별 상태 알림
8. 각 목적지의 성공/실패를 Integration Log에 기록

Airtable 또는 Slack 실패가 Google Sheet 원본 저장을 롤백해서는 안 됩니다.

## 3. Idempotency

- `RESPONSE_ID`를 Airtable의 고유 운영 키로 사용합니다.
- 외부 연동 재시도 시 같은 응답 ID를 새 레코드로 계속 생성하지 않습니다.
- Slack 알림은 `response_id + process_status + updated_at` 조합을 이벤트 키로 기록합니다.
- 최대 3회, 1초·2초·4초 간격의 지수 백오프를 사용합니다.

## 4. Public analysis export

Hugging Face 등 분석 저장소로 내보내기 전 다음을 모두 수행합니다.

- 이름, 기관, 이메일, 전화번호, 자유서술 제거
- 응답 ID를 무작위 `anonymous_id`로 교체
- 날짜를 일 단위가 아닌 월 단위로 축소
- 소수 집단 조합에 대한 재식별 위험 검토
- 원본과 비식별 내보내기의 접근권한 분리

## 5. Failure policy

| 실패 지점 | 원본 보존 | 사용자 제출 결과 | 운영 조치 |
|---|---|---|---|
| Sheet 저장 | 실패 | 제출 실패 처리 | 즉시 확인, 자동 재시도 제한 |
| PDF 생성 | Sheet 보존 | 접수 완료/후속 처리 | PDF 재생성 작업 등록 |
| 이메일 | Sheet·PDF 보존 | 접수 완료 | 이메일 재시도 |
| Airtable | Sheet·PDF 보존 | 영향 없음 | 통합 로그에 실패 기록 |
| Slack | Sheet·PDF 보존 | 영향 없음 | 로그 기록, 반복 알림 제한 |

