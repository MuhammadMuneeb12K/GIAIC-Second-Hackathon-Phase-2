"""
Task Request and Response Schemas.

This module defines Pydantic models for task endpoints:
- Request schemas for creating and updating tasks
- Response schema for task data
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


# Request Schemas


class CreateTaskRequest(BaseModel):
    """
    Request schema for creating a task (POST /api/tasks).

    Validation:
        - title: Required, min 1 char, max 200 chars (FR-024)
        - description: Optional, max 2000 chars (FR-025)
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (optional)")

    @validator("title")
    def validate_title(cls, v):
        """Validate title is not empty after stripping whitespace."""
        if not v or v.strip() == "":
            raise ValueError("Title cannot be empty")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v.strip()

    @validator("description")
    def validate_description(cls, v):
        """Validate description length if provided."""
        if v is not None:
            if len(v) > 2000:
                raise ValueError("Description must not exceed 2000 characters")
            return v.strip() if v.strip() else None
        return v


class UpdateTaskRequest(BaseModel):
    """
    Request schema for updating a task (PUT /api/tasks/{id}).

    Validation:
        - title: Required, min 1 char, max 200 chars (FR-024)
        - description: Optional, max 2000 chars (FR-025)
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (optional)")

    @validator("title")
    def validate_title(cls, v):
        """Validate title is not empty after stripping whitespace."""
        if not v or v.strip() == "":
            raise ValueError("Title cannot be empty")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v.strip()

    @validator("description")
    def validate_description(cls, v):
        """Validate description length if provided."""
        if v is not None:
            if len(v) > 2000:
                raise ValueError("Description must not exceed 2000 characters")
            return v.strip() if v.strip() else None
        return v


# Response Schema


class TaskResponse(BaseModel):
    """
    Task data response schema.

    Used in all task endpoint responses (FR-042).

    Includes all task fields:
        - id: Task identifier
        - title: Task title
        - description: Task description (nullable)
        - completed: Completion status
        - user_id: Owner's user ID
        - created_at: Creation timestamp
        - updated_at: Last update timestamp
    """

    id: int = Field(..., description="Task unique identifier")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(..., description="Task completion status")
    user_id: int = Field(..., description="Owner's user ID")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
