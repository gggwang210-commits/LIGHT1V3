# LIGHT ONE VS Code 안정화 프로젝트 v1.2.1

`index.html` 설문과 `admin.html` 관리자 집계 화면을 VS Code에서 검토하기 위한 패키지입니다. 설문 역할 코드, 문항 `name/value`, 조건부 분기, 동의 처리와 서버 엔드포인트 계약은 원본 v1.2.1과 같게 유지했습니다.

## 빠른 시작

1. `LIGHTONE.code-workspace`를 VS Code로 엽니다.
2. 터미널에서 `python scripts/verify_project.py`를 실행합니다.
3. VS Code 작업 `LIGHT ONE: 로컬 미리보기`를 실행하고 `http://localhost:5500/index.html`을 엽니다.
4. 관리자 화면은 `http://localhost:5500/admin.html`에서 확인합니다. 로컬 정적 서버에는 Netlify Functions가 없으므로 실제 집계 로그인은 동작하지 않습니다.

로컬·파일 미리보기의 설문 제출은 운영 서버로 전송하지 않습니다. 연락정보를 제외한 테스트 payload만 브라우저 `localStorage`에 최대 20건 보관합니다. 운영 저장, 실제 이메일, Airtable 변경 및 배포는 이 패키지 제작 과정에서 수행하지 않았습니다.

## 보존한 계약

- 역할: `owner`, `trainer`, `member`
- 설문 버전: `1.2.1`
- 제출: `POST /.netlify/functions/submit-survey`
- 관리자 집계: `POST /.netlify/functions/admin-summary`
- 이메일: `POST /.netlify/functions/send-report`
- 관리자 헤더: `X-Admin-Password`
- 기간: `7d`, `30d`, `90d`, `all`
- 인쇄/PDF: `window.print()`

`qa/data_contract_snapshot.json`은 원본 HTML에서 추출한 폼·문항 계약입니다. 검증 스크립트가 현재 파일과 이 스냅샷을 비교합니다.

## 반영한 안정화 항목

- JavaScript 비활성 안내와 대시보드 예시 화면 표기
- 필수·선택·복수 제한 안내 보강
- 제출 시간초과를 성공으로 처리하지 않고 저장 여부 확인 안내
- 관리자 요청 경쟁상태, 중복 실행, 로그아웃 뒤 지연 응답 차단
- 인증·HTTP·네트워크·JSON 오류 구분
- 누락된 집계값을 `0`이 아닌 `확인 불가`로 표시
- 기능 선택률의 0~100% 기준과 복수응답 합계 안내
- A4 인쇄 시 표 머리글 반복

## 배포 전 필수 확인

이 ZIP에는 서버 함수 구현이 포함되어 있지 않습니다. 검증된 운영 원본을 준비하고 [`netlify/functions/README_REQUIRED.md`](netlify/functions/README_REQUIRED.md)와 [`docs/DEPLOY_CHECKLIST.md`](docs/DEPLOY_CHECKLIST.md)를 확인하세요. `.env`와 실제 비밀값은 ZIP에 넣지 마세요.
