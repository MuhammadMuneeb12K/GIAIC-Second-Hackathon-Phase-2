"""
Dependency Injection Functions for FastAPI.

This module provides reusable dependencies for:
- Database session management
- User authentication and authorization
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from app.database import get_db
from app.core.security import verify_token
from app.core.exceptions import AuthenticationError


# HTTP Bearer token security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Authentication dependency that validates JWT and extracts user.

    This dependency:
    1. Extracts JWT token from Authorization header
    2. Validates token signature and expiration (FR-013)
    3. Extracts user_id from token payload (FR-014)
    4. Returns user_id for use in endpoints

    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session

    Returns:
        dict: Dictionary containing user_id and other user info

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or expired

    Usage:
        @app.get("/protected")
        def protected_endpoint(current_user = Depends(get_current_user)):
            user_id = current_user["user_id"]
            # Use user_id for user isolation
    """
    token = credentials.credentials

    # Verify token signature and expiration
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from token payload
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return user information for use in endpoints
    return {"user_id": user_id}
