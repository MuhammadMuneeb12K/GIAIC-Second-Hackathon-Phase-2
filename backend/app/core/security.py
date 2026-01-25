"""
Security Utilities for Password Hashing and JWT Token Management.

This module provides functions for:
- Password hashing with bcrypt (cost factor 12)
- JWT token creation and verification
- User authentication helpers
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import settings


# Password hashing context with bcrypt (cost factor 12)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Security:
        - Uses bcrypt algorithm with cost factor 12 (NFR-001)
        - Never log or expose the hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash using constant-time comparison.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise

    Security:
        - Uses constant-time comparison to prevent timing attacks
        - Never log passwords or hashes
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode in the token (must include user_id)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string

    Token Structure:
        - Algorithm: HS256 (NFR-002)
        - Claims: user_id, exp (expiration)
        - Expiration: 15 minutes by default (FR-009)
        - Signed with BETTER_AUTH_SECRET (FR-008)
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Dictionary of claims to encode in the token (must include user_id)

    Returns:
        Encoded JWT refresh token string

    Token Structure:
        - Algorithm: HS256 (NFR-002)
        - Claims: user_id, exp (expiration)
        - Expiration: 7 days (FR-010)
        - Signed with BETTER_AUTH_SECRET (FR-008)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None if invalid or expired

    Validation:
        - Verifies signature using BETTER_AUTH_SECRET (FR-013)
        - Checks expiration timestamp (FR-013)
        - Returns None for any validation failure
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
