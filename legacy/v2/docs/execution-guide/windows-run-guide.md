# Windows 실행 가이드

이 문서는 저장소 루트에서 Windows 사용자가 Django MVP를 실행하는 방법을 안내합니다. 앱 설명과 계정 정보는 [Django README](../../lightone_v2_django/README.md), Django 폴더 내부 기준의 짧은 실행 명령은 [기존 RUN_WINDOWS](../../lightone_v2_django/RUN_WINDOWS.md), 사업 배경은 [루트 README](../../README.md)를 함께 확인합니다.

## 1. 준비물

- Windows 10 이상
- Python 3.11 권장 또는 Anaconda Python
- PowerShell 또는 Windows Terminal
- Git으로 받은 `LightOne_V2` 저장소

## 2. 루트에서 Django 폴더로 이동

PowerShell에서 저장소 루트로 이동한 뒤 Django 프로젝트 폴더로 들어갑니다.

```powershell
cd LightOne_V2
cd lightone_v2_django
```

현재 위치에 `manage.py`와 `requirements.txt`가 보여야 합니다.

```powershell
dir
```

## 3. 가상환경 사용 방식

일반 Python을 사용하는 경우 가상환경을 권장합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

PowerShell 실행 정책 오류가 나면 현재 터미널에서만 다음 명령을 실행한 뒤 다시 활성화합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Anaconda를 이미 사용하는 경우

Anaconda Python이 정상 동작한다면 가상환경 없이도 빠른 실행 확인이 가능합니다. 이 방식은 [기존 RUN_WINDOWS](../../lightone_v2_django/RUN_WINDOWS.md)의 절차와 같습니다.

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_lightone
python manage.py runserver
```

## 5. 일반 Python 가상환경 실행

```powershell
python manage.py migrate
python manage.py seed_lightone
python manage.py runserver
```

브라우저에서 다음 주소를 엽니다.

```text
http://127.0.0.1:8000/lightone/
```

기본 계정은 [Django README의 기본 계정 표](../../lightone_v2_django/README.md#기본-계정-더미-데이터-기준)를 확인합니다.

## 6. 실행 확인 체크리스트

- [ ] `/accounts/login/` 로그인 화면이 열리는가?
- [ ] `/lightone/` 대시보드에서 회원 목록이 보이는가?
- [ ] 세션 입력 화면에서 RPE와 통증 반응을 입력할 수 있는가?
- [ ] 리포트 화면에서 AUTO / REVIEW / BLOCK 상태가 표시되는가?
- [ ] 실제 회원 데이터가 아니라 더미 데이터로만 테스트했는가?

## 7. 주의사항

이 MVP는 비의료 운동 상담 보조 도구입니다. 의료 진단, 치료, 처방을 대체하지 않으며, 통증 관련 입력은 트레이너 검토를 위한 참고 정보입니다. 표현 기준은 [비의료 경계 정책](../governance/non-medical-boundary.md), 데이터 취급 기준은 [개인정보 보호 체크리스트](../governance/privacy-checklist.md)를 따릅니다.
