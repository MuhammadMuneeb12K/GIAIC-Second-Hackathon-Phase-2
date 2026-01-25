"""
User SQLModel for Database.

This module defines the User model representing registered user accounts.
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    """
    User model representing a registered user account.

    Attributes:
        id: Unique user identifier (auto-generated)
        email: User's email address (unique, indexed for login queries)
        password_hash: Bcrypt-hashed password (never exposed in API responses)
        name: User's display name
        created_at: Timestamp when account was created
        updated_at: Timestamp when account was last updated
        tasks: Relationship to user's tasks (one-to-many)

    Constraints:
        - email must be unique (enforced at database level)
        - password_hash must not be null
        - name must not be null

    Indexes:
        - email (for efficient login queries)

    Security:
        - password_hash is never included in API responses (FR-040)
        - User isolation enforced via foreign key relationships
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to tasks (one-to-many)
    tasks: List["Task"] = Relationship(back_populates="user")
