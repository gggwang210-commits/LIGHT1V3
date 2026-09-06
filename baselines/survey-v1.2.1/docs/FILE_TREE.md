# 파일 구조

```text
LIGHTONE_VSCODE_STABLE_v1.2.1/
├─ .vscode/                 VS Code 권장 확장·설정·작업
├─ docs/                    제작 프롬프트와 배포·보안 문서
├─ netlify/functions/       필요한 서버 원본 안내
├─ qa/                      데이터 계약과 자동·브라우저 검증 결과
├─ screenshots/             검증 화면 캡처
├─ scripts/                 재실행 가능한 검증 스크립트
├─ index.html               역할별 설문
├─ admin.html               관리자 집계 화면
├─ BUILD_INFO.json          원본과 빌드 정보
├─ MANIFEST.sha256          파일 무결성 목록
├─ QA_REPORT.md             검증 결론과 미검증 범위
└─ README.md                시작 안내
```

`netlify/functions`에는 실행 코드가 없습니다. 운영 함수는 별도 검증 후 추가해야 합니다.
