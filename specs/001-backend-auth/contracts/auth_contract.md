# Contracts — Authentication API

1) POST /api/auth/register
- Request JSON:
  - `email`: string
  - `password`: string
- Responses:
  - `201 Created` — body `{ "message": "user created" }`
  - `400 Bad Request` — input validation or duplicate email

2) POST /api/auth/login
- Request JSON:
  - `email`: string
  - `password`: string
- Responses:
  - `200 OK` — body `{ "access_token": "<jwt>", "token_type": "bearer", "expires_in": 900, "refresh_token": "<refresh>" }`
  - `401 Unauthorized` — invalid credentials (generic message)

3) Authorization header
- Protected endpoints require: `Authorization: Bearer <access_token>`

4) GET /api/admin/status (example)
- Requires role: `admin`
- Responses:
  - `200 OK` — `{ "status": "ok" }` for admin
  - `403 Forbidden` — valid token but insufficient role
  - `401 Unauthorized` — missing/invalid/expired token

5) Token semantics
- Access token: short-lived (~15 minutes), contains claims: `sub` (user id), `role`, `exp`, `jti` optional. Signed with HS256 using `JWT_SECRET`.
- Refresh token: long-lived (~7 days), rotated on use. Server stores refresh tokens in `refresh_tokens` table keyed by `jti` for revocation.
