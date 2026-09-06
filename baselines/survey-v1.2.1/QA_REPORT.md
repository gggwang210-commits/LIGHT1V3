# LIGHT ONE v1.2.1 QA 보고서

## 결론

정적 검사와 로컬 브라우저·합성 API 회귀검증은 PASS입니다. 설문 데이터 계약 스냅샷과 현재 `index.html`의 폼 action, 문항 `name/value`, 조건 필드가 일치합니다.

## 원본

- `LIGHTONE_v1.2.1_NETLIFY_DEPLOY.zip`
- ZIP SHA-256: `b46ce40c3ab831034773b980dcdc9b5e99c9bb672bc80f9811c39951386098df`
- 설문 버전: `1.2.1`

## 검증 결과

- 필수 파일, UTF-8, meta charset, viewport, 중복 id, 엔드포인트·헤더·기간·역할·버전 계약: PASS
- 원본 데이터 계약 비교: PASS
- inline JavaScript `node --check`: PASS
- ZIP `testzip()`과 단일 프로젝트 루트 검사: PASS
- 320/375/390/768/1024/1440px 가로 넘침: 모두 0px
- 첫 오류 포커스 이동: PASS
- 연락 미동의 미리보기 payload·localStorage의 연락정보 제외: PASS
- 관리자 누락값 `확인 불가`, 선택률 0~100% 제한: PASS
- 기간 요청 경쟁상태와 로그아웃 뒤 지연 응답 차단: PASS
- 이메일 요청 중 버튼 비활성 및 두 번째 요청 0건: PASS
- 인증·HTTP·JSON·네트워크 오류별 안내: PASS
- A4 인쇄 CSS의 조작 버튼 제외·표 머리글 반복: 정적 PASS

세부 결과는 `qa/validation_results.json`, `qa/browser_regression.json`과 `screenshots/`에서 확인할 수 있습니다.

## 보안·개인정보

- 실제 관리자 비밀번호, API 키, 토큰, `.env`, 응답자 개인정보는 포함하지 않았습니다.
- 공개 여부를 확인하지 못한 원본 담당자 이메일은 `[비밀값 제거]`로 바꿨습니다. 운영 공개 전 검토된 문의 연락처를 넣어야 합니다.
- 관리자 화면에는 합계·비율·분포만 표시하며 개인 응답자 필드를 추가하지 않았습니다.

## [확인필요] 미검증 범위

- 실제 Netlify 저장과 중복 처리
- 실제 운영 데이터 집계
- 실제 이메일 발송
- 실제 Airtable 변경
- 운영 도메인·환경변수·보안 헤더
- 실제 브라우저 인쇄 대화상자의 최종 PDF 출력물

운영 함수와 비밀값을 넣은 스테이징 환경에서 `docs/DEPLOY_CHECKLIST.md`를 따라 재검증해야 합니다.
