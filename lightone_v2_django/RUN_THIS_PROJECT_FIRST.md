# 실행 방법

압축을 푼 뒤 PowerShell에서 이 폴더로 이동하고 아래 순서대로 실행한다.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_lightone
python manage.py runserver
```

접속 주소:

```text
http://127.0.0.1:8000/lightone/
```

이미지가 안 보이면 브라우저에서 `Ctrl + F5`로 강력 새로고침한다.
