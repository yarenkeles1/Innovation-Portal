
# Implementation Plan: Backend Foundation & Authentication

**Branch**: `001-backend-auth` | **Date**: 2026-02-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-backend-auth/spec.md`

## Summary

Implement a minimal FastAPI backend scaffold with SQLite (dev), SQLAlchemy models, Alembic-compatible migrations, secure password hashing, JWT access+refresh tokens (15m / 7d with rotation + server-side revocation), and a role-based authorization dependency. Deliver endpoints for `POST /api/auth/register`, `POST /api/auth/login`, and an example role-protected `GET /api/admin/status`, plus pytest integration tests validating register, login, and authorization behavior.

## Technical Context

**Language/Version**: Python 3.11 (or 3.10+)  
**Primary Dependencies**: FastAPI, SQLAlchemy (1.4+/2.0 style), Alembic, python-jose (JWT), passlib (bcrypt), pydantic, pytest, httpx/testclient.  
**Storage**: SQLite for local development; design compatible with PostgreSQL for production.  
**Testing**: `pytest` (unit & integration) with FastAPI TestClient and fixtures for test DB.  
**Target Platform**: Local development on Windows / POSIX for developer runs.  
**Project Type**: Web service (backend API).  
**Performance Goals**: Local dev responsive (<1s auth flows); no production SLA required for initial feature.  
**Constraints**: Keep secrets out of source control (use `.env` or environment variables). Use adaptive hashing (bcrypt) and minimal dependency set to meet constitution security requirements.  
**Scale/Scope**: MVP user auth and role checks for small developer/test usage.

## Constitution Check

Gates derived from the Innovation-Portal constitution are satisfied by this plan as follows:

- Authentication & Authorization: JWT-based flows and `require_role()` will be implemented; roles `user` and `admin` included and mapped to constitution roles. (See `contracts/auth_contract.md` and `src/auth/deps.py` contract.)
- Testing: `pytest` test suite will include failing tests (red) before implementing the code, then integration tests for register/login/admin access. (See `tests/integration/test_auth.py` fixtures.)
- Data model & migrations: SQLAlchemy models plus Alembic-compatible layout will be provided; migrations are supported. (See `data-model.md`.)
- Attachment handling and idea lifecycle are out of scope for this specific feature's implementation but the DB layout and conventions will stay compatible with the constitution's attachment and status fields.
- Security basics: Password hashing via `passlib`/bcrypt and JWT secret via env variable are required by the plan.

Each gate will be linked to concrete tests under `tests/` before Phase 1 sign-off.

## Project Structure

Selected layout (backend-only service):

```text
backend/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── core/                # config, settings, secrets loader
│   ├── db/                  # database init, session, migrations helper
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── auth/                # auth logic: hashing, tokens, deps
│   └── api/                 # routers (api/auth.py, api/admin.py)
├── alembic/                 # migrations (optional initial revision)
├── tests/
│   ├── integration/
│   └── unit/
├── requirements.txt
└── README.md
```

Files created in this plan (phase outputs): `research.md`, `data-model.md`, `quickstart.md`, `contracts/auth_contract.md` (in the spec folder).

## Complexity Tracking

No constitution violations introduced. All security and test-first gates are respected.

