# LIGHT ONE V2 Django 설치 및 실행 가이드

이 문서는 현재 저장소 구조를 기준으로 LIGHT ONE V2 Django 앱을 Windows에서 실행하는 최신 기준 안내입니다.

## 현재 기준 경로

| 항목 | 최신 기준 |
|---|---|
| Django 프로젝트 폴더 | `lightone_v2_django` |
| 패키지 목록 | `lightone_v2_django/requirements.txt` |
| 실행 파일 | `lightone_v2_django/manage.py` |
| 더미 데이터 명령 | `python manage.py seed_lightone` |
| 접속 URL | `http://127.0.0.1:8000/lightone/` |

> 구버전 안내: 예전 문서나 압축 파일에 `lightone_django_complete.zip`, `lightone_django`, `LIGHTONE_V2_Complete.zip` 같은 이름이 보이면 현재는 `lightone_v2_django` 폴더로 이동해서 실행하면 됩니다.

---

## 1. 사전 준비

- Python 3.10 이상 권장
- Windows PowerShell 또는 CMD
- VS Code 선택 사항

Python 설치 시 **Add Python to PATH** 옵션을 반드시 체크하세요.

---

## 2. 프로젝트 폴더로 이동

저장소 루트에서 Django 폴더로 이동합니다.

```powershell
cd lightone_v2_django
```

이 위치에서 아래 파일이 보여야 합니다.

```powershell
dir manage.py, requirements.txt
```

---

## 3. 가상환경 생성 및 활성화

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

PowerShell 실행 정책 오류가 나면 CMD를 사용하세요.

### CMD

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

---

## 4. 패키지 설치

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 5. 데이터베이스 준비 및 더미 데이터 생성

```powershell
python manage.py migrate
python manage.py seed_lightone
```

`seed_lightone` 명령은 데모 회원/세션/전략 데이터와 로그인 계정을 함께 생성합니다.

---

## 6. 서버 실행

```powershell
python manage.py runserver
```

브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:8000/lightone/
```

---

## 로그인 정보

`python manage.py seed_lightone` 실행 후 사용할 수 있는 계정입니다.

| 역할 | 아이디 | 비밀번호 | URL |
|---|---|---|---|
| 관리자/트레이너 | `admin` | `admin` | `/accounts/login/`, `/admin/` |
| 회원 | `member1` | `1234` | `/accounts/login/` |
| 회원 | `member2` | `1234` | `/accounts/login/` |

---

## 주요 URL

| 기능 | URL |
|---|---|
| LIGHT ONE 대시보드 | `http://127.0.0.1:8000/lightone/` |
| 로그인 | `http://127.0.0.1:8000/accounts/login/` |
| Django 관리자 | `http://127.0.0.1:8000/admin/` |

---

## 트러블슈팅

### `ModuleNotFoundError: No module named 'django'`

가상환경을 활성화하고 패키지를 다시 설치하세요.

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### `Port 8000 is already in use`

다른 포트로 실행합니다.

```powershell
python manage.py runserver 8001
```

이 경우 접속 주소는 `http://127.0.0.1:8001/lightone/` 입니다.

### 로그인 계정이 맞지 않는 경우

더미 데이터 명령을 다시 실행하면 위 표의 비밀번호로 재설정됩니다.

```powershell
python manage.py seed_lightone
```
