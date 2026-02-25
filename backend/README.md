# Backend Foundation & Authentication

This is the FastAPI backend service with JWT-based authentication and role-based authorization.

## Features

- **User Registration**: Register new users with email and password
- **User Login**: Authenticate users and receive JWT access tokens
- **Refresh Tokens**: Long-lived refresh tokens with rotation and revocation support
- **Role-Based Access Control**: Protect endpoints with role requirements
- **Secure Password Hashing**: Bcrypt-based password hashing via passlib
- **SQLAlchemy ORM**: SQL database abstraction with Alembic migrations
- **Comprehensive Testing**: Integration tests with pytest

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── core/
│   │   └── settings.py      # Configuration loader
│   ├── db/
│   │   └── database.py      # Database setup and session management
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── refresh_token.py # RefreshToken model
│   ├── schemas/
│   │   └── auth.py          # Pydantic schemas
│   ├── auth/
│   │   ├── security.py      # Password hashing
│   │   ├── tokens.py        # JWT token creation/validation
│   │   ├── deps.py          # Dependency injection
│   │   └── service.py       # Business logic
│   └── api/
│       ├── auth.py          # Authentication routes
│       └── admin.py         # Admin routes (example)
├── tests/
│   ├── conftest.py          # Pytest configuration
│   ├── integration/
│   │   ├── test_auth_register.py
│   │   ├── test_auth_login.py
│   │   └── test_auth_authorize.py
│   └── unit/
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure as needed:

```bash
cp .env.example .env
```

Default values are suitable for local development.

### 3. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs` (Swagger UI)

## API Endpoints

### Authentication

- **POST** `/api/auth/register` - Register a new user
  - Request: `{"email": "user@example.com", "password": "securepassword123"}`
  - Response: `{"message": "user created"}` (HTTP 201)

- **POST** `/api/auth/login` - Login and receive tokens
  - Request: `{"email": "user@example.com", "password": "securepassword123"}`
  - Response: `{"access_token": "...", "refresh_token": "...", "token_type": "bearer", "expires_in": 900}`

### Admin (Role Protected)

- **GET** `/api/admin/status` - Admin-only endpoint
  - Headers: `Authorization: Bearer <access_token>`
  - Response: `{"status": "ok"}` (HTTP 200 for admins, 403 for users)

## Running Tests

Run all integration tests:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

## Testing Scenarios

### User Registration
- ✅ Successful registration with valid email/password
- ✅ Duplicate email rejection
- ✅ Invalid email format rejection
- ✅ Weak password rejection

### User Login
- ✅ Successful login returns valid JWT tokens
- ✅ Invalid credentials return 401
- ✅ Nonexistent user returns 401 (no user enumeration)
- ✅ JWT tokens contain user ID and role claims

### Role-Based Authorization
- ✅ Admin endpoint accessible with admin token
- ✅ Admin endpoint returns 403 with user token
- ✅ Missing token returns 401
- ✅ Invalid/malformed JWT returns 401

## Security Features

- **Password Hashing**: Bcrypt with adaptive rounds via passlib
- **JWT Tokens**: HS256 signed with secret from environment
- **Token Expiry**: 
  - Access tokens: 15 minutes (configurable)
  - Refresh tokens: 7 days (configurable)
- **Refresh Token Rotation**: Server-side storage with revocation support
- **Role-Based Access**: Dependency injection for authorization checks
- **Secrets Management**: All secrets loaded from `.env` (not committed to git)

## Database

- **Development**: SQLite (file-based, minimal setup)
- **Production**: PostgreSQL compatible (configure DATABASE_URL)

### Models

- **User**: Stores user account information with role and timestamps
- **RefreshToken**: Tracks issued refresh tokens for revocation and rotation

### Initialization

The database is automatically initialized on application startup via `init_db()`.

For migrations, use Alembic (included in requirements):

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Development Notes

- Debug logging can be enabled in `.env` with `ENVIRONMENT=debug`
- CORS is currently open for development (restrict in production)
- Health check endpoint available at `/health`
- All endpoints require HTTPS in production (use HTTPS proxy)

## Next Steps

1. ✅ User registration and login
2. ✅ Role-based authorization
3. 📋 Password reset workflow
4. 📋 Email verification
5. 📋 Refresh token rotation on use
6. 📋 Session management and logout
7. 📋 Multi-factor authentication (MFA)
