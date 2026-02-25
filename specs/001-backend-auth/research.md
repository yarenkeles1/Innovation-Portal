# Phase 0 — Research: Backend Foundation & Authentication

Decisions and rationale for the feature implementation.

1) Language & Framework
- Decision: Python 3.11+, FastAPI.  
- Rationale: FastAPI provides an ergonomic, async-ready web framework with strong Pydantic integration and Fast development cycles. Python 3.11 is recommended for performance and typing improvements.

2) ORM, Migrations & DB
- Decision: SQLAlchemy (1.4+/2.0 style) + Alembic for migrations. SQLite for local development; configuration supports PostgreSQL for production.  
- Rationale: SQLAlchemy is required by the spec and is compatible with Alembic for migrations. SQLite meets the constitution's local-first constraint.

3) Password Hashing
- Decision: `passlib` CryptContext using `bcrypt` (bcrypt with appropriate rounds).  
- Rationale: Constitution requires bcrypt; `passlib` wraps bcrypt and simplifies migration to other algorithms later. Alternatives: `argon2` (stronger but not required by constitution); rejected to keep alignment with constitution.

4) JWT library & token strategy
- Decision: `python-jose` for JWT handling (HS256 by default, secret from env). Access tokens 15 minutes, refresh tokens 7 days. Refresh tokens stored in DB (RefreshToken model) and support rotation + server-side revocation via `jti` (unique id).  
- Rationale: `python-jose` is widely used with FastAPI; server-side refresh token storage enables rotation and revocation; HS256 is simplest for local dev with env secret. Alternatives: asymmetric keys (RS256) — deferred until production secrets management in place.

5) Token rotation & revocation
- Decision: Each refresh token has a `jti` UUID stored in DB with `revoked` flag and expiry. On using a refresh token, validate existence & not revoked, then revoke the used token and issue a new refresh token (rotation). Store the new token record and return it to the client.  
- Rationale: Prevents reuse of stolen refresh tokens; supports server-side invalidation on logout.

6) Auth flow & dependency injection
- Decision: Implement `get_current_user()` dependency that decodes access token, loads user from DB and attaches to the request. Implement `require_role(role)` dependency that checks `current_user.role == role` or role in allowed set.  
- Rationale: Matches FastAPI dependency pattern and spec requirement for role-based access.

7) Testing strategy
- Decision: `pytest` with FastAPI `TestClient` + test fixtures to create a temporary SQLite DB per test session. Integration tests for register/login and role-protected endpoints.  
- Rationale: Matches constitution's Test-First requirement.

8) DB initialization strategy
- Decision: Provide `backend/app/db.py` which exposes `engine`, `SessionLocal`, and `init_db()` helper to run Alembic migrations or create tables for dev. Use Alembic as canonical migration mechanism.  
- Rationale: Alembic adds migration tracking; `init_db()` eases local dev startup.

9) Security & configuration
- Decision: All secrets (JWT secret, bcrypt rounds) loaded from environment or `.env` via a settings loader (Pydantic `BaseSettings`). Defaults set for dev.  

10) Alternatives considered
- Use of `SQLModel`: simpler mapping but adds dependency and slightly different migration patterns — rejected to stick with plain SQLAlchemy as requested by spec.
- Use `argon2` for hashing: stronger but constitution mandates bcrypt; can be added later.

Outcome: All open clarifications in the spec are resolved. Proceed to Phase 1: data model and contracts.
