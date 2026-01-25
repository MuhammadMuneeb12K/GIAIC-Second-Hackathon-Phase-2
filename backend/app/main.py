"""
FastAPI Application Entry Point.

This module creates and configures the FastAPI application with:
- CORS middleware for frontend integration
- Global exception handlers for consistent error responses
- API routers with /api prefix
- Health check endpoint
- Logging configuration
"""

import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from json import JSONDecodeError

from app.config import settings
from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
)
from app.database import create_db_and_tables


from contextlib import asynccontextmanager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # Add file handler for production
        # logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)


# Lifespan event handler (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.

    Startup: Creates database tables if they don't exist.
    Shutdown: Cleanup operations (if needed).
    """
    # Startup
    create_db_and_tables()
    logger.info("Database tables created/verified")
    yield
    # Shutdown (cleanup if needed)
    logger.info("Application shutting down")


# Create FastAPI application instance
app = FastAPI(
    title="Todo API",
    description="Multi-user todo application with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Frontend origin from environment
    allow_credentials=True,  # Allow cookies and Authorization header
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# Global Exception Handlers


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.

    Returns 422 Unprocessable Entity with validation error details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc.errors()[0]["msg"]) if exc.errors() else "Validation error"},
    )


@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    """
    Handle authentication errors.

    Returns 401 Unauthorized with error message.
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


@app.exception_handler(AuthorizationError)
async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    """
    Handle authorization errors.

    Returns 403 Forbidden with error message.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    """
    Handle not found errors.

    Returns 404 Not Found with error message.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(ConflictError)
async def conflict_exception_handler(request: Request, exc: ConflictError):
    """
    Handle conflict errors (e.g., duplicate email).

    Returns 409 Conflict with error message.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (e.g., unique constraint violations).

    Returns 409 Conflict with generic error message.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Data integrity error"},
    )


@app.exception_handler(JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: JSONDecodeError):
    """
    Handle JSON parsing errors.

    Returns 400 Bad Request with error message.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid JSON format"},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors.

    Returns 500 Internal Server Error without exposing sensitive details.
    Logs the full error for debugging.
    """
    # Log error with context (NFR-015)
    logger.error(
        f"Unexpected error: {type(exc).__name__}: {str(exc)}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
        }
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Health Check Endpoint


@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns API status and version information.
    """
    return {
        "status": "healthy",
        "service": "Todo API",
        "version": "1.0.0",
    }


# API Routers
from app.api.routes import auth, tasks

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
