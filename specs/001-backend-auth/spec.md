```markdown
# Feature Specification: Backend Foundation & Authentication

**Feature Branch**: `001-backend-auth`  
**Created**: 2026-02-25  
**Status**: Draft  
**Input**: User description: "Backend Foundation & Authentication: FastAPI project structure; SQLite; SQLAlchemy; User model (id, email, hashed_password, role); JWT authentication; Password hashing; Register endpoint; Login endpoint; Role-based access dependency"

## Clarifications

### Session 2026-02-25

- Q: Token expiration and refresh strategy → A: Short-lived access token (15 minutes) + refresh token (7 days) with rotation and server-side revocation support.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Register and receive credentials (Priority: P1)

As a new user, I want to register with an email and password so I can authenticate and access protected resources.

**Why this priority**: Core onboarding flow required to use the system.

**Independent Test**: POST to `/api/auth/register` with email and password creates a user record and returns success (no UI needed).

**Acceptance Scenarios**:

1. **Given** no existing account for `user@example.com`, **When** the client POSTs email and password to `/api/auth/register`, **Then** the system creates a user, returns HTTP 201, and does not return the raw password.
2. **Given** an existing account for `user@example.com`, **When** the client attempts to register again with the same email, **Then** the system returns HTTP 400 with a clear error about duplicate email.

---

### User Story 2 - Login and receive access token (Priority: P1)

As a registered user, I want to log in with my email and password so I can receive an access token for authenticated requests.

**Why this priority**: Authentication is required for protected APIs.

**Independent Test**: POST to `/api/auth/login` with valid credentials returns an access token and HTTP 200.

**Acceptance Scenarios**:

1. **Given** a valid user and password, **When** the client POSTs credentials to `/api/auth/login`, **Then** the system returns HTTP 200 and a JSON body containing an access token and its expiry.
2. **Given** invalid credentials, **When** the client attempts to log in, **Then** the system returns HTTP 401 with a generic authentication error (no user enumeration).

---

### User Story 3 - Role-protected endpoint (Priority: P2)

As an admin user, I want to access admin-only endpoints so I can perform privileged operations.

**Why this priority**: Authorization primitives are required for access control and future features.

**Independent Test**: Call a protected endpoint that requires role `admin` with and without an admin token and verify access/denial.

**Acceptance Scenarios**:

1. **Given** a valid access token for a user with role `admin`, **When** the client calls `GET /api/admin/status`, **Then** the system returns HTTP 200.
2. **Given** a valid access token for a user with role `user`, **When** the client calls `GET /api/admin/status`, **Then** the system returns HTTP 403.

---

-### Edge Cases

- Password below minimum strength → HTTP 400 with guidance.
- Login attempts rate-limited after configurable failures (detect brute force).
- Expired or malformed JWT → HTTP 401.
- Attempt to register with very long email/password fields → HTTP 400 (validation limits).
- Login attempts rate-limited after configurable failures (detect brute force).
- Expired or malformed JWT → HTTP 401.
- Attempt to register with very long email/password fields → HTTP 400 (validation limits).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a minimal FastAPI project structure with a clear entrypoint for the backend.
- **FR-002**: The system MUST persist data to a local SQLite database in development and support configuration for other environments.
- **FR-003**: The system MUST use SQLAlchemy for ORM models and migrations-friendly layout.
- **FR-004**: The system MUST expose a `User` model with fields: `id` (integer, primary key), `email` (string, unique), `hashed_password` (string), `role` (string; e.g., `user`|`admin`).
- **FR-005**: The system MUST securely hash passwords before storing them.
- **FR-006**: The system MUST provide a `/api/auth/register` endpoint that validates input (excluding strict email format validation), creates a new user, and returns appropriate HTTP status codes.
- **FR-007**: The system MUST provide a `/api/auth/login` endpoint that validates credentials and returns an access token (JWT) and expiry information on success.
- **FR-008**: The system MUST issue signed JWTs that encode the user id and role and that can be validated by the backend. Access tokens MUST be short-lived (default 15 minutes). The system MUST also issue refresh tokens (default 7 days) with rotation support and server-side revocation capability.
- **FR-009**: The system MUST provide an authorization dependency that enforces role-based access control for endpoints (e.g., `require_role('admin')`).
- **FR-010**: The system MUST never return plaintext passwords or hashed passwords in API responses.
- **FR-011**: The system MUST include basic input validation and clear error messages for client errors.

### Key Entities *(include if feature involves data)*

- **User**: Represents an application user.
  - `id`: integer, primary key
  - `email`: string, unique, validated
  - `hashed_password`: string, password hash
  - `role`: string enum (`user`, `admin`)
  - `created_at`: datetime (implicit)
  - `updated_at`: datetime (implicit)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can set up the project locally and run migrations/start the server following README steps within 10 minutes.
- **SC-002**: A user can register and receive a success response and be able to log in using the registered credentials (end-to-end) in a test run.
- **SC-003**: Login attempts with valid credentials return an access token in 95% of attempts and within 1 second under a local development environment.
- **SC-004**: Role-protected endpoint returns HTTP 200 for an `admin` token and HTTP 403 for a non-admin token in automated acceptance tests.
- **SC-005**: All functional requirements FR-001 through FR-011 have at least one automated test or manual acceptance scenario documented.

## Assumptions

- Roles: The system will start with two roles: `user` and `admin`.
- Password hashing: Use a modern, adaptive hashing algorithm (bcrypt/argon2) with sensible defaults; store only the hash.
- JWT signing: Tokens are signed with a secret kept out of source control; default expiry will be short-lived (e.g., 1 hour) and configurable.
- Token strategy: Access tokens default to 15 minutes; refresh tokens default to 7 days with rotation and revocation supported.
- No email verification is required for initial MVP (can be added later).
- Migrations: While SQLite is required for development, the project structure should be compatible with migration tools.

## Non-Goals (out of scope)

- Social login / OAuth integrations.
- Email sending, password resets, or multi-factor authentication in this initial feature.

## Deliverables

- Minimal FastAPI app scaffold with entrypoint (e.g., `app/main.py`).
- SQLAlchemy `User` model and database setup for SQLite.
- Authentication module implementing password hashing, JWT issuance and verification.
- Endpoints: `POST /api/auth/register`, `POST /api/auth/login`.
- Authorization dependency `require_role(role)` and example protected route `GET /api/admin/status`.
- README with local setup and basic test instructions.

## Testing Notes

- Include integration tests that:
  - Register a new user and assert the user exists in the DB.
  - Log in with valid credentials and assert a JWT is returned and decodable.
  - Call a role-protected endpoint with admin and non-admin tokens.

---
```
