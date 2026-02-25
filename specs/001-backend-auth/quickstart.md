# Quickstart — Backend Foundation & Authentication

1) Setup (recommended)

Install Python (3.10+ / 3.11), create a virtualenv, install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

2) Environment

Create `.env` or set environment variables (example):

```text
JWT_SECRET=dev-secret-please-change
ACCESS_TOKEN_EXPIRES_MIN=15
REFRESH_TOKEN_EXPIRES_DAYS=7
DATABASE_URL=sqlite:///./dev.db
```

3) Initialize DB (dev)

Run Alembic migrations if available, or create tables for quick dev:

```powershell
cd backend
alembic upgrade head   # if alembic configured
python -c "from app.db import init_db; init_db()"  # helper fallback
```

4) Run server

```powershell
uvicorn app.main:app --reload --port 8000
```

5) Run tests

```powershell
pytest -q
```

6) API endpoints (examples)

- `POST /api/auth/register` — register user
- `POST /api/auth/login` — login, returns `access_token` and (rotating) `refresh_token`
- `GET /api/admin/status` — example protected route requiring `admin` role
