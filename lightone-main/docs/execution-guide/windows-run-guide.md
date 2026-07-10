# Windows PowerShell Run Guide

This repository currently contains Python quality-check modules and a static landing page. A Django MVP entry point (`manage.py`) is not present.

## Static landing page

```powershell
python -m http.server 8000
```

Open `http://localhost:8000/index.html`.

## Python checks

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pytest
pytest
```

## Django MVP status

- `manage.py`: not present
- Django routes for login, dashboard, session, and report pages: not present
- Dummy-data management command: not present
- `.env` is ignored by `.gitignore`; use `.env.example` for non-secret examples only.
