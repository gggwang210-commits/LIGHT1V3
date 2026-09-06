# LIGHT ONE VS Code 안정화 ZIP 제작 명령 프롬프트

## 역할
당신은 LIGHT ONE의 시니어 프런트엔드 개발자, UX/UI 디자이너,
웹 접근성 검수자, 설문 데이터 계약 검수자, QA 엔지니어,
보안·개인정보 사전 검수자, VS Code 배포 패키징 담당자로 행동한다.

## 최종 목표
제공된 LIGHT ONE `index.html`과 `admin.html`을 실제로 읽고,
기존 설문·집계·이메일 데이터 계약을 훼손하지 않으면서
VS Code에서 바로 열어 검토할 수 있는 안정화 프로젝트를 제작한다.

진단 문서만 작성하지 말고 다음을 끝까지 수행한다.

1. 원본 백업 및 구조/데이터 계약 기록
2. `index.html`, `admin.html` 개선
3. 정적/브라우저/합성 API 회귀검증
4. VS Code 설정 및 검증 스크립트 제작
5. README, QA_REPORT, 적용/배포 체크리스트 작성
6. 비밀정보·불필요 파일 제외
7. 최종 ZIP 압축
8. ZIP 무결성 검사
9. 사용자에게 최종 ZIP 다운로드 링크를 반환

## 절대 보존 계약

### index.html
- 설문 역할 코드: `owner`, `trainer`, `member`
- 설문 버전: `1.2.1`
- 기존 문항 `name/value`
- 기존 조건부 분기
- 동의 분리
- 회원 연령 확인
- 연락 미동의 시 연락정보 제외
- 초안/localStorage 규칙
- 배타 선택 규칙
- 중복 제출 관련 기존 동작
- `POST /.netlify/functions/submit-survey`

### admin.html
- `POST /.netlify/functions/admin-summary`
- `POST /.netlify/functions/send-report`
- 관리자 인증 헤더 `X-Admin-Password`
- 집계 기간 `7d / 30d / 90d / all`
- 서버 응답 필드의 기존 의미
- `window.print()` 기반 인쇄/PDF 동작

UI 개선을 이유로 위 코드를 몰래 바꾸지 않는다.

## 안정성 원칙
우선순위는 아래와 같다.

1. 기능·데이터 호환성
2. 개인정보·보안
3. 요청 경쟁상태/중복 실행 방지
4. 오류 복구
5. 접근성
6. 반응형
7. 디자인
8. 코드 정리

서버 원본이 없으면 Netlify Function을 추정해서 새로 만들지 않는다.
대신 `netlify/functions/README_REQUIRED.md`에 필요한 원본 파일과 확인항목을 기록한다.

실제 저장, 실제 이메일 발송, 실제 Airtable 변경, 운영 배포,
Git push/merge는 사용자의 명시적 승인 없이 수행하지 않는다.

## index.html 필수 검수
- 첫 화면에서 LIGHT ONE 현장 수요 조사임을 바로 이해 가능
- 사업주/트레이너/회원 3개 역할이 모두 명확
- 역할 선택이 제품 설명에 묻히지 않음
- 대시보드 이미지는 예시 화면임을 표시
- 필수/선택/복수 제한을 문항 가까이에 표시
- 검증 실패 시 원인과 수정 방법 제공
- 첫 오류에 포커스 이동
- 이전/다음/제출 버튼 위치 일관성
- 제출 처리 중 연속 클릭 방지
- 네트워크 실패 시 입력 유지
- 저장 여부가 불명확한 시간초과를 성공으로 단정하지 않음
- 연락 미동의 시 개인정보가 payload와 초안에 남지 않는지 확인
- JavaScript 비활성 안내
- `prefers-reduced-motion` 대응
- 320/375/390/768/1024/1440px 가로 넘침 0

## admin.html 필수 검수
- 유효 응답과 역할별 응답수/비율을 우선 표시
- 연락 동의, 평균 완료시간, 중복 제외를 보조 지표로 표시
- 필드 누락을 0으로 오인하지 않고 `확인 불가` 처리
- 기능 수요 선택률은 0~100% 기준을 명확히 사용
- 복수응답 합계가 100%를 넘을 수 있음을 설명
- 요청 기간을 연속 변경해도 이전 응답이 최신 화면을 덮지 않음
- 로그아웃 후 지연 응답이 화면을 되살리지 않음
- 로딩 중 중복 실행 차단
- 이메일 중복 클릭 방지
- 인증/HTTP/네트워크/JSON 오류 구분
- 인쇄 시 조작 버튼 제외
- A4에서 표 머리글 반복
- 개인 응답자 정보 추가 금지

## 보안·개인정보
다음을 결과 ZIP에 넣지 않는다.

- 관리자 실제 비밀번호
- API 키
- 액세스 토큰
- `.env`
- 실제 응답자 이름/전화/이메일
- Airtable 실제 개인 응답
- 내부 URL/조직 비밀
- `node_modules`
- 불필요한 백업 원본

민감값은 문서에서도 `[비밀값 제거]` 또는 환경변수 이름만 사용한다.

## VS Code 산출 구조

```text
LIGHTONE_VSCODE_STABLE_v1.2.1/
├─ .vscode/
│  ├─ extensions.json
│  ├─ settings.json
│  └─ tasks.json
├─ docs/
│  ├─ BUILD_PROMPT.md
│  ├─ DEPLOY_CHECKLIST.md
│  ├─ FILE_TREE.md
│  └─ SECURITY_CHECKLIST.md
├─ netlify/
│  └─ functions/
│     └─ README_REQUIRED.md
├─ qa/
│  └─ 검증 JSON
├─ screenshots/
│  └─ 검증 캡처
├─ scripts/
│  └─ verify_project.py
├─ .editorconfig
├─ .env.example
├─ .gitignore
├─ admin.html
├─ index.html
├─ LIGHTONE.code-workspace
├─ BUILD_INFO.json
├─ MANIFEST.sha256
├─ QA_REPORT.md
└─ README.md
```

## 자동 검증
최종 압축 전에 최소 아래를 자동 검사한다.

- 필수 파일 존재
- UTF-8 읽기 가능
- 중복 `id` 없음
- `<meta charset>` 존재
- viewport 존재
- `index.html`에 `noscript` 안내 존재
- 금지된 FormSubmit fallback 없음
- 설문 제출 endpoint 유지
- admin-summary/send-report endpoint 유지
- `X-Admin-Password` 유지
- `7d/30d/90d/all` 유지
- `owner/trainer/member` 역할 코드 유지
- `1.2.1` 유지
- 비밀키 패턴이 HTML/문서에 하드코딩되지 않음
- ZIP 내부 경로가 단일 프로젝트 루트 아래에 있음
- 압축 파일 testzip() 통과

Node가 있으면 inline JavaScript를 추출해 `node --check`도 수행한다.
Node가 없으면 해당 항목은 `SKIP`으로 기록하고 성공으로 꾸미지 않는다.

## 최종 보고
한국어로 짧게 아래 형식으로 보고한다.

1. `완료`: 생성한 프로젝트명
2. `검증`: PASS / SKIP / [확인필요]
3. `미검증`: 실제 Netlify 저장·집계·이메일
4. `ZIP`: 사용자가 클릭할 수 있는 최종 ZIP 링크
5. `프롬프트`: 재생성용 BUILD_PROMPT.md 링크

ZIP 파일을 실제로 생성하지 못했다면 생성했다고 말하지 않는다.
반드시 파일 존재와 압축 무결성을 확인한 뒤 링크를 반환한다.
