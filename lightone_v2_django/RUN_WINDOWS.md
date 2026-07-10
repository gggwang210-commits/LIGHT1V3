# Windows 실행 가이드

> 저장소 루트 기준의 자세한 Windows 안내는 [`../docs/execution-guide/windows-run-guide.md`](../docs/execution-guide/windows-run-guide.md)를 참고하세요. 전체 사업 방향은 [`../README.md`](../README.md), MVP 기능과 계정 정보는 [`README.md`](README.md)에 정리되어 있습니다.

이미 Anaconda Python이 정상 작동하고 있다면 가상환경 없이도 실행 확인이 가능합니다.

> 구버전 안내: `lightone_django`, `lightone_django_complete.zip`, `LIGHTONE_V2_Complete.zip` 같은 이름이 보이는 예전 안내는 현재 `lightone_v2_django` 기준으로 바꿔 실행하세요.

## 1단계: 프로젝트 폴더로 이동

저장소 루트에서 실행하는 경우:

```powershell
cd lightone_v2_django
```

현재 위치 확인:

```powershell
dir manage.py, requirements.txt
```

## 2단계: 가상환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

PowerShell 보안 오류가 나면 CMD에서 아래처럼 실행하세요.

```cmd
.venv\Scripts\activate.bat
```

## 3단계: 설치 및 DB 준비

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_lightone
```

## 4단계: 서버 실행

```powershell
python manage.py runserver
```

브라우저 주소:

```text
http://127.0.0.1:8000/lightone/
```

## 로그인 정보

| 역할 | 아이디 | 비밀번호 |
|---|---|---|
| 관리자/트레이너 | `admin` | `admin` |
| 회원 | `member1` | `1234` |
| 회원 | `member2` | `1234` |
