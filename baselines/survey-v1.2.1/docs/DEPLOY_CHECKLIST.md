# 적용·배포 체크리스트

## 적용 전

- [ ] `python scripts/verify_project.py`가 PASS인지 확인
- [ ] `MANIFEST.sha256`과 배포 대상 파일의 해시 확인
- [ ] 원본 `submit-survey.js`, `admin-summary.js`, `send-report.js`, `_lib/report.js` 확보
- [ ] 서버 함수가 설문 v1.2.1과 같은 허용 필드·조건부 분기·중복 처리 계약을 사용하는지 확인
- [ ] `[비밀값 제거]` 상태인 개인정보 문의 연락처를 검토된 공개 연락처로 교체
- [ ] OG 이미지·페이지 URL 자리표시자를 운영 절대주소로 교체

## 환경변수

- [ ] `ADMIN_REPORT_PASSWORD`
- [ ] `NETLIFY_API_TOKEN`
- [ ] `NETLIFY_SITE_ID`
- [ ] `RESEND_API_KEY`, `REPORT_FROM_EMAIL`, `REPORT_TO_EMAIL`(이메일 사용 시)
- [ ] `ALLOWED_ORIGINS` 또는 동일 출처 제한값

## 스테이징 회귀검증

- [ ] `owner`, `trainer`, `member` 정상 제출
- [ ] 회원 만 14세 미만 제출 차단
- [ ] 연락 미동의 payload와 저장 데이터에 연락정보 없음
- [ ] 네트워크 실패·15초 시간초과 시 입력 유지 및 성공 화면 미표시
- [ ] 동일 응답 ID 중복 제출의 기존 처리 확인
- [ ] `7d`, `30d`, `90d`, `all` 집계 확인
- [ ] 관리자 요청 순서를 바꿔도 최신 선택 기간만 표시
- [ ] 로그아웃 뒤 지연 응답이 화면을 다시 열지 않음
- [ ] 이메일 버튼 연속 클릭 시 한 번만 요청
- [ ] A4 인쇄/PDF에서 조작 버튼 제외·표 머리글 반복

## 배포 후

- [ ] 실제 저장 건과 집계 수 대조
- [ ] 실제 이메일 수신·본문·개인정보 제외 확인
- [ ] 오류 로그에 비밀번호·연락정보가 기록되지 않는지 확인
- [ ] 롤백 대상 ZIP과 배포 시각 기록
