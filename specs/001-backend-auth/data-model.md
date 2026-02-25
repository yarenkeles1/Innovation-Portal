# Phase 1 — Data Model

Entities and models for Backend Foundation & Authentication.

1) User
- SQLAlchemy model: `User`  
- Fields:
  - `id`: Integer, primary key, autoincrement
  - `email`: String, unique, index, max length 320
  - `hashed_password`: String
  - `role`: String, default `user`, allowed values `user`|`admin`
  - `created_at`: DateTime, default now
  - `updated_at`: DateTime, auto-updated

- Validation rules:
  - `email` required, trimmed, length limit; de-duplication enforced at DB layer
  - `password` not stored; validate min length (e.g., 8 chars) and basic strength in API layer

2) RefreshToken
- SQLAlchemy model: `RefreshToken`  
- Fields:
  - `id`: Integer, primary key
  - `jti`: String (UUID), unique
  - `user_id`: ForeignKey -> `users.id`
  - `revoked`: Boolean, default False
  - `created_at`: DateTime
  - `expires_at`: DateTime

- Purpose: store active refresh tokens for rotation and revocation checks.

3) (Notes) Idea/Attachment compatibility
- While this feature does not implement attachments, the DB design should keep a separate `ideas` table (with `attachment_path`, `attachment_checksum`) and allow migrations later.

4) SQLAlchemy structure (recommended files)
- `backend/app/models/__init__.py` — model imports and Base metadata
- `backend/app/models/user.py` — `User` model
- `backend/app/models/refresh_token.py` — `RefreshToken` model
- `backend/app/db.py` — engine, sessionmaker, Base metadata, and `init_db()`

5) Example SQLAlchemy model sketch (declarative)

```py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(320), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(32), nullable=False, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    user = relationship("User")
```
