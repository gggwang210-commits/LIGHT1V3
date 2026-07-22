# Contributing to LIGHT ONE V3

LIGHT ONE V3는 로컬 파일럿 단계의 비의료 운동상담 보조 MVP입니다. 변경은 실행 가능성뿐 아니라 개인정보 최소화, 의료 오인 방지, 트레이너 검토 원칙을 함께 지켜야 합니다.

## 기준 경로

- 활성 애플리케이션: `lightone_v2_django/`
- 기준 문서: `docs/`
- 저장소 검증: `tests/`
- 과거 구현과 자산: `legacy/`, `legacy-docs/`, `lightone-main/`, `lightone_django/`

보관 영역은 회귀 조사 목적 외에는 수정하지 않습니다. 새 기능을 과거 구현 폴더에 복제하지 마세요.

## 개발 절차

1. `Main-ONE`에서 목적이 드러나는 짧은 브랜치를 만듭니다.
2. `.env.example`을 복사해 개인 로컬 설정을 준비하고 비밀값은 커밋하지 않습니다.
3. 활성 앱과 기준 문서만 최소 범위로 변경합니다.
4. 아래 검증 명령을 실행합니다.
5. Pull Request 템플릿의 보안·개인정보·비의료 항목을 확인합니다.

권장 브랜치 접두사는 `feat/`, `fix/`, `docs/`, `security/`, `chore/`입니다. 커밋 메시지는 `type: summary` 형식을 권장합니다.

## 로컬 검증

Python 3.12 이상을 사용합니다.

```bash
python -m pip install -r requirements-dev.txt

cd lightone_v2_django
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test

cd ..
python -m pytest tests -q
python -m flake8 lightone_v2_django --select=E9,F63,F7,F82
```

실행을 위해 `SECRET_KEY`가 필요합니다. 로컬 설정 방법은 `lightone_v2_django/.env.example`과 앱 README를 따릅니다.

## 공개 데이터 규칙

- 실제 회원 이름, 연락처, 이메일, 생년월일, 상담 원문, 신체 이미지와 건강정보를 추가하지 않습니다.
- 예시는 `SYN-*`, `데모회원-*` 형식의 합성 식별자만 사용합니다.
- `.env`, SQLite DB, API 키, 토큰, 비밀번호, 개인 미디어를 커밋하지 않습니다.
- 재현 데이터가 필요하면 최소한의 합성 fixture를 만들고 합성임을 문서화합니다.

## 제품 표현 규칙

- 진단, 치료, 처방, 재활 판정, 질병 위험 예측을 기능이나 효과로 주장하지 않습니다.
- `AUTO`, `REVIEW`, `BLOCK`은 의료적 안전 판정이 아닌 운영상 검토 우선순위입니다.
- 자동 산출물은 담당 트레이너의 검토 전제로 설명합니다.
- 성능, 매출, 시간 절감 수치는 검증 근거가 없으면 확정적으로 표현하지 않습니다.

## Pull Request 범위

PR에는 변경 목적, 실행 영향, 검증 결과, 남은 위험을 적습니다. 운영 배포나 실제 데이터 처리가 검증되지 않았다면 이를 명시합니다. 보안 취약점이나 민감정보는 공개 이슈와 PR 본문에 작성하지 말고 `SECURITY.md`를 따르세요.
