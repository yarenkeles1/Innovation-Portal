---
description: "Task list for Backend Foundation & Authentication implementation"
---

# Tasks: Backend Foundation & Authentication

**Input**: Design documents from `/specs/001-backend-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/auth_contract.md
**Project Root**: Backend service located in `backend/` directory
**Testing**: Integration and unit tests included per spec requirements (FR-005, SC-002, SC-004, SC-005)

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Task can run in parallel (independent files, no blocking dependencies)
- **[Story]**: User story label (US1, US2, US3) - ONLY on user story phase tasks
- **File paths**: Exact locations for each task output

## Dependency Graph

```
Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phase 3-5 parallel) → Polish (Phase 6)
                                            ├─ US1: Register (P1)
                                            ├─ US2: Login (P1)
                                            └─ US3: Role-Based Access (P2)
```

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md

- [x] T001 Create backend project directory structure per plan.md in `backend/`
- [x] T002 [P] Create Python requirements.txt with FastAPI, SQLAlchemy, Alembic, passlib, python-jose, pydantic, pytest, httpx in `backend/requirements.txt`
- [x] T003 [P] Create FastAPI main application entrypoint in `backend/app/main.py` with basic app initialization
- [x] T004 [P] Create `.env.example` template with JWT_SECRET, ACCESS_TOKEN_EXPIRES_MIN, REFRESH_TOKEN_EXPIRES_DAYS, DATABASE_URL in `backend/.env.example`
- [x] T005 Create `__init__.py` in `backend/app/` to initialize app package

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create database engine, SessionLocal, and Base in `backend/app/db.py` using SQLAlchemy (per data-model.md: SQLite for dev, PostgreSQL-compatible)
- [x] T007 [P] Create Pydantic settings loader in `backend/app/core/settings.py` loading JWT_SECRET, token expiry, and DATABASE_URL from env
- [x] T008 [P] Create models package with `__init__.py` in `backend/app/models/` with Base metadata import
- [x] T009 [P] Create schemas package with `__init__.py` in `backend/app/schemas/` 
- [x] T010 [P] Create auth package with `__init__.py` in `backend/app/auth/`
- [x] T011 [P] Create API routers package with `__init__.py` in `backend/app/api/`
- [x] T012 Create `init_db()` helper function in `backend/app/db.py` to create all tables (per research.md: supports dev initialization)
- [x] T013 Create database session dependency in `backend/app/db.py` for FastAPI injection

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Register and receive credentials (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register with email and password, creating a user record in the database

**Independent Test**: POST to `/api/auth/register` with email and password creates a user record and returns HTTP 201

**Acceptance Criteria** (from spec.md):
1. Valid registration creates user and returns HTTP 201 without exposing password
2. Duplicate email attempt returns HTTP 400 with clear error message

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T014 [P] [US1] Create test fixtures for database and test client in `backend/tests/conftest.py`
- [x] T015 [P] [US1] Write integration test for successful user registration in `backend/tests/integration/test_auth_register.py` - test POST /api/auth/register with valid email/password returns 201
- [x] T016 [P] [US1] Write integration test for duplicate email rejection in `backend/tests/integration/test_auth_register.py` - test POST /api/auth/register with existing email returns 400

### Implementation for User Story 1

- [x] T017 [P] [US1] Create User SQLAlchemy model in `backend/app/models/user.py` with id, email, hashed_password, role, created_at, updated_at (per data-model.md)
- [x] T018 [P] [US1] Create password hashing utilities in `backend/app/auth/security.py` with hash_password() and verify_password() using bcrypt (per research.md)
- [x] T019 [P] [US1] Create Pydantic schemas for register request/response in `backend/app/schemas/auth.py` (email, password in request; user data in response without password hash)
- [x] T020 [US1] Implement registration service function in `backend/app/auth/service.py` or embed in endpoint (create user, hash password, store in DB) - depends on T017, T018
- [x] T021 [US1] Create register endpoint in `backend/app/api/auth.py` POST /api/auth/register with input validation and error handling (per contracts/auth_contract.md: 201 Created or 400 Bad Request)
- [x] T022 [US1] Add user creation validation (email format basics, password strength validation per plan.md) in `backend/app/api/auth.py`
- [x] T023 [US1] Wire register endpoint into FastAPI app in `backend/app/main.py` (include auth router)

**Checkpoint**: User Story 1 complete - registration endpoint functional and independently testable

---

## Phase 4: User Story 2 - Login and receive access token (Priority: P1)

**Goal**: Enable registered users to authenticate with email/password and receive JWT access tokens for protected endpoints

**Independent Test**: POST to `/api/auth/login` with valid credentials returns HTTP 200 with access_token, refresh_token, and expiry information

**Acceptance Criteria** (from spec.md):
1. Valid credentials return HTTP 200 with access_token and expiry (per contracts: expires_in in seconds)
2. Invalid credentials return HTTP 401 with generic error (no user enumeration)
3. Access tokens are short-lived (15 min default per plan.md)
4. Refresh tokens are long-lived (7 days default) with rotation and server-side revocation support

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T024 [P] [US2] Write integration test for successful login in `backend/tests/integration/test_auth_login.py` - test POST /api/auth/login with valid credentials returns 200 with access_token
- [x] T025 [P] [US2] Write integration test for invalid login in `backend/tests/integration/test_auth_login.py` - test POST /api/auth/login with invalid password returns 401
- [x] T026 [P] [US2] Write integration test for nonexistent user in `backend/tests/integration/test_auth_login.py` - test POST /api/auth/login with unknown email returns 401
- [x] T027 [P] [US2] Write token validation test in `backend/tests/integration/test_auth_login.py` - decode JWT and validate it contains user id and role

### Implementation for User Story 2

- [x] T028 [P] [US2] Create RefreshToken SQLAlchemy model in `backend/app/models/refresh_token.py` with jti, user_id, revoked, created_at, expires_at (per data-model.md)
- [x] T029 [P] [US2] Create JWT token utility functions in `backend/app/auth/tokens.py`: create_access_token(), create_refresh_token() with HS256 signing and expiry (per contracts/auth_contract.md and research.md)
- [x] T030 [P] [US2] Create token decoding/validation utilities in `backend/app/auth/tokens.py`: decode_token(), validate_token_expiry() (per contracts: token semantics with exp claim)
- [x] T031 [P] [US2] Create Pydantic schemas for login request/response in `backend/app/schemas/auth.py` (email/password request; access_token/refresh_token/expires_in response)
- [x] T032 [US2] Create login service function in `backend/app/auth/service.py` (validate credentials, generate tokens, store refresh token jti in DB) - depends on T017, T018, T028, T029
- [x] T033 [US2] Create login endpoint in `backend/app/api/auth.py` POST /api/auth/login with credential validation (per contracts: 200 OK or 401 Unauthorized)
- [x] T034 [US2] Implement get_current_user() dependency in `backend/app/auth/deps.py` to decode JWT from Authorization header and load user from DB (per research.md)
- [x] T035 [US2] Wire login endpoint and update routers in `backend/app/main.py` to include current implementation

**Checkpoint**: User Story 2 complete - authentication flow functional, users can register and login

---

## Phase 5: User Story 3 - Role-protected endpoint (Priority: P2)

**Goal**: Enable role-based access control using JWT tokens to restrict endpoints to specific roles

**Independent Test**: Call GET /api/admin/status with admin token returns 200; with user token returns 403

**Acceptance Criteria** (from spec.md):
1. Admin users can access /api/admin/status and receive HTTP 200
2. Non-admin users receive HTTP 403 with valid token
3. Missing/invalid/expired JWT returns HTTP 401

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T036 [P] [US3] Write authorization test in `backend/tests/integration/test_auth_authorize.py` - test GET /api/admin/status with admin role returns 200
- [x] T037 [P] [US3] Write role rejection test in `backend/tests/integration/test_auth_authorize.py` - test GET /api/admin/status with user role returns 403
- [x] T038 [P] [US3] Write missing token test in `backend/tests/integration/test_auth_authorize.py` - test GET /api/admin/status without token returns 401
- [x] T039 [P] [US3] Write invalid token test in `backend/tests/integration/test_auth_authorize.py` - test GET /api/admin/status with malformed JWT returns 401

### Implementation for User Story 3

- [x] T040 [P] [US3] Create require_role() dependency in `backend/app/auth/deps.py` for role-based authorization (per research.md: checks current_user.role against allowed roles)
- [x] T041 [P] [US3] Create admin status endpoint in `backend/app/api/admin.py` GET /api/admin/status protected by require_role('admin') - returns status: ok (per contracts/auth_contract.md)
- [x] T042 [US3] Create error handling/responses for 403 Forbidden in `backend/app/api/admin.py` when role insufficient (per contracts)
- [x] T043 [US3] Wire admin router into FastAPI app in `backend/app/main.py`
- [x] T044 [US3] Implement token expiration and refresh token rotation flow in `backend/app/auth/tokens.py` - support server-side revocation via jti (per research.md)

**Checkpoint**: User Story 3 complete - role-based access control functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Complete test suite, documentation, error handling, and production readiness

- [ ] T045 Create comprehensive error handler middleware in `backend/app/core/exceptions.py` with HTTPException mappings for 400/401/403/422 responses
- [ ] T046 [P] Add input validation error responses in register/login endpoints per spec.md FR-011 (clear error messages for client errors)
- [ ] T047 [P] Create basic logging setup in `backend/app/core/logging.py` for auth events (registration, login, authorization failures)
- [ ] T048 Configure Alembic for database migrations in `backend/alembic/` with initial revision for User and RefreshToken models
- [ ] T049 Create README.md in `backend/` with: local setup instructions (venv, pip install), .env template, initialization steps (alembic upgrade or init_db), server start command (uvicorn), and test run command (pytest) - per quickstart.md and SC-001
- [ ] T050 [P] Create unit test for password hashing security in `backend/tests/unit/test_security.py` (verify hashes are not reversible)
- [ ] T051 [P] Create unit test for JWT claim validation in `backend/tests/unit/test_tokens.py` (verify sub and role claims present and correct)
- [ ] T052 Create integration test suite runner script in `backend/tests/run_tests.sh` for CI/CD readiness
- [ ] T053 Add rate limiting configuration stub in `backend/app/core/settings.py` for login attempts (per spec.md edge case: brute force detection)
- [ ] T054 Create database migration for User and RefreshToken in `backend/alembic/versions/` with proper timestamps and schema
- [ ] T055 Document API contract compliance mapping in `backend/API_CONTRACTS.md` validating all contracts/ endpoints match implementation
- [ ] T056 Create example `.env` file in `backend/.env.example` with safe dev defaults
- [ ] T057 Verify all FR-001 through FR-011 requirements covered and tested via checklist in `backend/REQUIREMENTS_COVERAGE.md`

**Checkpoint**: All features complete, tested, documented, and production-ready

---

## Implementation Strategy

**MVP Scope** (deliver first for fastest user feedback):
- Phase 1: Setup (T001-T005)
- Phase 2: Foundational (T006-T013)
- Phase 3: User Story 1 Register (T014-T023)
- Result: Users can register and create accounts

**Phase 2 Expansion** (add authentication):
- Phase 4: User Story 2 Login (T024-T035)
- Result: Users can register and log in, receive JWT tokens

**Phase 3 Expansion** (add authorization):
- Phase 5: User Story 3 Role-Based Access (T036-T044)
- Result: Admin-only endpoints protected, role-based access control active

**Phase 4 Polish** (production readiness):
- Phase 6: Polish & Tests (T045-T057)
- Result: Complete documented API with full test coverage

## Parallel Execution Examples

**Parallel setup** (Phase 1):
```
T001 (structure) → [T002, T003, T004, T005 in parallel] → Phase 2
```

**Parallel foundation** (Phase 2):
```
[T006, T007, T008, T009, T010, T011 can run in parallel] → [T012, T013 depend on T006] → User Stories
```

**Parallel user stories** (Phase 3, 4, 5):
```
Phase 3 Tests [T014, T015, T016 in parallel] → Implementation [T017, T018, T019 in parallel] → [T020, T021, ...] (some sequential)
Phase 4 Tests [T024, T025, T026, T027 in parallel] → Implementation [T028, T029, T030, T031 in parallel] → [T032, T033, ...]
Phase 5 Tests [T036, T037, T038, T039 in parallel] → Implementation [T040, T041 in parallel] → [T042, T043, T044]
```

## Test Coverage Alignment with Success Criteria

- **SC-002**: Tests T015-T016 (US1), T024-T026 (US2) verify end-to-end registration and login flows
- **SC-004**: Tests T036-T039 (US3) validate role-protected endpoint returns 200 for admin, 403 for user
- **SC-005**: All FR-001 through FR-011 covered by tasks and tests; checklist in T057

## Files Requiring the Checklist Reference

The following tasks should reference specific checklist items from `/specs/001-backend-auth/checklists/requirements.md`:

- T023, T035: Ensure all FR requirements (FR-001 through FR-011) are met
- T049: README completeness per SC-001 (setup within 10 minutes)
- T057: Final compliance verification of all functional requirements

---

**Total Tasks**: 57  
**Tasks per User Story**: US1: 10 | US2: 12 | US3: 9 | Setup/Foundational/Polish: 26  
**Parallelizable Tasks**: 32 [P] marked  
**MVP Delivery**: T001-T023 (register feature only) = 23 tasks  
**Full Feature Delivery**: All 57 tasks
