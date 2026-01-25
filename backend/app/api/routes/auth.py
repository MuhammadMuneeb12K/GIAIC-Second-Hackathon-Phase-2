"""
Authentication API Endpoints.

This module implements authentication endpoints:
- POST /api/auth/signup - User registration
- POST /api/auth/signin - User authentication
- POST /api/auth/refresh - Token refresh
- POST /api/auth/signout - User signout
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.schemas.auth import (
    SignupRequest,
    SigninRequest,
    RefreshRequest,
    AuthResponse,
    RefreshResponse,
    MessageResponse,
    UserResponse,
)
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.core.exceptions import ConflictError, AuthenticationError


router = APIRouter()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Create a new user account (POST /api/auth/signup).

    This endpoint:
    1. Validates request data (email format, password length, name)
    2. Creates user account with hashed password
    3. Generates JWT access and refresh tokens
    4. Returns user data and tokens

    Request Body:
        - email: Valid email address (unique)
        - password: Minimum 8 characters
        - name: User's display name (max 100 characters)

    Response (201 Created):
        - user: User object (id, email, name, created_at)
        - access_token: JWT access token (expires in 15 minutes)
        - refresh_token: JWT refresh token (expires in 7 days)
        - token_type: "bearer"

    Errors:
        - 400: Malformed JSON
        - 409: Email already registered (FR-032)
        - 422: Validation error (invalid email, short password, etc.)

    Security:
        - Password hashed with bcrypt cost factor 12 (FR-004, NFR-001)
        - Email uniqueness enforced (FR-005)
        - password_hash never exposed in response (FR-040)
    """
    try:
        # Create user account
        user = create_user(
            db=db,
            email=request.email,
            password=request.password,
            name=request.name,
        )

        # Generate JWT tokens
        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_refresh_token(data={"user_id": user.id})

        # Return user data and tokens
        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at,
            ),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/signin", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def signin(request: SigninRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and issue tokens (POST /api/auth/signin).

    This endpoint:
    1. Validates credentials (email and password)
    2. Generates JWT access and refresh tokens
    3. Returns user data and tokens

    Request Body:
        - email: User's email address
        - password: User's password

    Response (200 OK):
        - user: User object (id, email, name, created_at)
        - access_token: JWT access token (expires in 15 minutes)
        - refresh_token: JWT refresh token (expires in 7 days)
        - token_type: "bearer"

    Errors:
        - 400: Malformed JSON
        - 401: Invalid credentials (generic message for security)
        - 422: Validation error

    Security:
        - Generic error message for failed authentication (security best practice)
        - Constant-time password comparison
        - JWT tokens signed with BETTER_AUTH_SECRET (FR-008)
    """
    try:
        # Authenticate user
        user = authenticate_user(
            db=db,
            email=request.email,
            password=request.password,
        )

        # Generate JWT tokens
        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_refresh_token(data={"user_id": user.id})

        # Return user data and tokens
        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at,
            ),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/refresh", response_model=RefreshResponse, status_code=status.HTTP_200_OK)
def refresh(request: RefreshRequest):
    """
    Refresh access token using refresh token (POST /api/auth/refresh).

    This endpoint:
    1. Validates refresh token signature and expiration
    2. Extracts user_id from token payload
    3. Generates new access token
    4. Returns new access token

    Request Body:
        - refresh_token: Valid JWT refresh token

    Response (200 OK):
        - access_token: New JWT access token (expires in 15 minutes)
        - token_type: "bearer"

    Errors:
        - 400: Malformed JSON
        - 401: Invalid or expired refresh token
        - 422: Validation error

    Security:
        - Validates token signature and expiration (FR-013)
        - Refresh token not rotated in this implementation
    """
    # Verify refresh token
    payload = verify_token(request.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # Extract user_id from token
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Generate new access token
    access_token = create_access_token(data={"user_id": user_id})

    return RefreshResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/signout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def signout(current_user: dict = Depends(get_current_user)):
    """
    Sign out user (POST /api/auth/signout).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Returns success message

    Note: In stateless JWT implementation, signout is primarily client-side.
    The client should discard tokens from storage.

    Headers:
        - Authorization: Bearer <access_token>

    Response (200 OK):
        - detail: "Successfully signed out"

    Errors:
        - 401: Missing or invalid token

    Implementation Note:
        - Server-side token blacklist not implemented (optional enhancement)
        - Client must clear tokens from localStorage/memory
    """
    return MessageResponse(detail="Successfully signed out")
