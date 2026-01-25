"""
Authentication Request and Response Schemas.

This module defines Pydantic models for authentication endpoints:
- Request schemas for signup, signin, refresh, signout
- Response schemas for user data and tokens
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


# Request Schemas


class SignupRequest(BaseModel):
    """
    Request schema for user registration (POST /api/auth/signup).

    Validation:
        - email: Must be valid email format (FR-002)
        - password: Minimum 8 characters (FR-003)
        - name: Required, max 100 characters
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (minimum 8 characters)")
    name: str = Field(..., min_length=1, max_length=100, description="User's display name")

    @validator("email")
    def validate_email_format(cls, v):
        """Validate email format using regex (FR-002)."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v.lower()  # Normalize to lowercase

    @validator("password")
    def validate_password_length(cls, v):
        """
        Validate password length constraints (FR-003).

        Enforces:
        - Minimum 8 characters
        - Maximum 72 bytes (bcrypt limit)
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        # Check byte length for bcrypt compatibility (72-byte limit)
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError(
                "Password is too long. Maximum length is 72 bytes "
                f"(your password is {len(password_bytes)} bytes)"
            )

        return v

    @validator("name")
    def validate_name(cls, v):
        """Validate name is not empty."""
        if not v or v.strip() == "":
            raise ValueError("Name cannot be empty")
        return v.strip()


class SigninRequest(BaseModel):
    """
    Request schema for user authentication (POST /api/auth/signin).

    Validation:
        - email: Must be valid email format
        - password: Required
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    @validator("email")
    def normalize_email(cls, v):
        """Normalize email to lowercase."""
        return v.lower()


class RefreshRequest(BaseModel):
    """
    Request schema for token refresh (POST /api/auth/refresh).

    Validation:
        - refresh_token: Required JWT token string
    """

    refresh_token: str = Field(..., description="Refresh token to exchange for new access token")


# Response Schemas


class UserResponse(BaseModel):
    """
    User data response schema (excludes password_hash for security).

    Used in signup and signin responses (FR-040).
    """

    id: int = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's display name")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility


class AuthResponse(BaseModel):
    """
    Authentication response schema with user data and tokens.

    Used in signup and signin responses (FR-041).

    Includes:
        - user: User data (id, email, name, created_at)
        - access_token: JWT access token (expires in 15 minutes)
        - refresh_token: JWT refresh token (expires in 7 days)
        - token_type: Always "bearer"
    """

    user: UserResponse = Field(..., description="User data")
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class RefreshResponse(BaseModel):
    """
    Token refresh response schema.

    Used in refresh endpoint response.

    Includes:
        - access_token: New JWT access token
        - token_type: Always "bearer"
    """

    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class MessageResponse(BaseModel):
    """
    Generic message response schema.

    Used for signout and other simple success responses.
    """

    detail: str = Field(..., description="Response message")
