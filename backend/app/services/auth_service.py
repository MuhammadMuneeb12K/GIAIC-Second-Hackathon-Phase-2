"""
Authentication Service - Business Logic Layer.

This module implements authentication business logic:
- User registration with email uniqueness validation
- User authentication with password verification
- Password hashing and verification
"""

from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.exceptions import ConflictError, AuthenticationError


def create_user(db: Session, email: str, password: str, name: str) -> User:
    """
    Create a new user account.

    This function:
    1. Validates email uniqueness (FR-005)
    2. Hashes password with bcrypt cost factor 12 (FR-004, NFR-001)
    3. Creates user record in database
    4. Returns created user object

    Args:
        db: Database session
        email: User's email address (must be unique)
        password: Plain text password (will be hashed)
        name: User's display name

    Returns:
        User: Created user object

    Raises:
        ConflictError: If email already exists (FR-032)

    Security:
        - Password is hashed before storage (FR-004)
        - Email uniqueness enforced at database level (FR-005)
    """
    # Check if email already exists
    existing_user = db.exec(select(User).where(User.email == email.lower())).first()
    if existing_user:
        raise ConflictError("Email already registered")

    # Hash password with bcrypt (cost factor 12)
    hashed_password = hash_password(password)

    # Create user object
    user = User(
        email=email.lower(),  # Normalize email to lowercase
        password_hash=hashed_password,
        name=name.strip(),
    )

    # Save to database
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ConflictError("Email already registered")


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password.

    This function:
    1. Looks up user by email
    2. Verifies password using constant-time comparison
    3. Returns user object if authentication succeeds

    Args:
        db: Database session
        email: User's email address
        password: Plain text password to verify

    Returns:
        User: User object if authentication succeeds
        None: If email doesn't exist or password is incorrect

    Raises:
        AuthenticationError: If credentials are invalid

    Security:
        - Uses constant-time password comparison to prevent timing attacks
        - Returns generic error message (doesn't reveal if email exists)
        - Never logs passwords or hashes
    """
    # Look up user by email
    user = db.exec(select(User).where(User.email == email.lower())).first()

    if not user:
        # Return generic error (don't reveal if email exists)
        raise AuthenticationError("Invalid email or password")

    # Verify password using constant-time comparison
    if not verify_password(password, user.password_hash):
        # Return generic error (don't reveal if email exists)
        raise AuthenticationError("Invalid email or password")

    return user
