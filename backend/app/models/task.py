"""
Task SQLModel for Database.

This module defines the Task model representing todo items owned by users.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey


class Task(SQLModel, table=True):
    """
    Task model representing a todo item owned by a user.

    Attributes:
        id: Unique task identifier (auto-generated)
        title: Task title (required, max 200 characters)
        description: Optional task description (max 2000 characters)
        completed: Task completion status (default: false)
        user_id: Foreign key to user who owns this task (indexed)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        user: Relationship to task owner (many-to-one)

    Constraints:
        - title must not be null
        - user_id must reference valid user
        - user_id indexed for efficient user-scoped queries

    User Isolation:
        - All queries MUST filter by user_id (FR-023)
        - Tasks owned by different users return 404 (FR-019)
        - CASCADE delete when user is deleted

    Validation:
        - title: max 200 characters (FR-024)
        - description: max 2000 characters (FR-025)
        - completed: default false (FR-026)
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, nullable=False)
    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to user (many-to-one)
    user: Optional["User"] = Relationship(back_populates="tasks")
