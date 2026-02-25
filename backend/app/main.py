"""
FastAPI application entrypoint for Backend Foundation & Authentication.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.db import init_db
from app.api import auth, admin


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Innovation Portal Backend",
        description="Backend API with authentication and authorization",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

    # Startup event
    @app.on_event("startup")
    def startup_event():
        """Initialize database on startup."""
        init_db()

    # Health check endpoint
    @app.get("/health")
    def health_check():
        """Basic health check endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
