"""
Task Service - Business Logic Layer.

This module implements task management business logic with user isolation:
- Task creation with user ownership
- Task retrieval with user isolation
- Task updates with ownership validation
- Task deletion with ownership validation
- Task completion toggling
"""

from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.models.task import Task
from app.core.exceptions import NotFoundError


def create_task(
    db: Session,
    title: str,
    description: Optional[str],
    user_id: int
) -> Task:
    """
    Create a new task for the authenticated user.

    This function:
    1. Creates task with user_id from authenticated user (FR-016)
    2. Sets completed to false by default (FR-026)
    3. Sets created_at and updated_at timestamps (FR-027)

    Args:
        db: Database session
        title: Task title (max 200 characters)
        description: Optional task description (max 2000 characters)
        user_id: ID of user who owns this task (from JWT token)

    Returns:
        Task: Created task object

    Security:
        - user_id extracted from JWT, never from request body (FR-016)
        - Task automatically associated with authenticated user
    """
    task = Task(
        title=title.strip(),
        description=description.strip() if description else None,
        completed=False,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_user_tasks(db: Session, user_id: int) -> List[Task]:
    """
    Retrieve all tasks owned by the authenticated user.

    This function:
    1. Queries tasks filtered by user_id (FR-023)
    2. Returns empty list if user has no tasks (not 404)

    Args:
        db: Database session
        user_id: ID of authenticated user (from JWT token)

    Returns:
        List[Task]: List of tasks owned by user (empty list if none)

    User Isolation:
        - Only returns tasks where user_id matches authenticated user (FR-023)
        - Users cannot see other users' tasks (SC-003)
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db.exec(statement).all()
    return list(tasks)


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Retrieve a single task by ID with user isolation.

    This function:
    1. Queries task by id AND user_id (FR-019, FR-023)
    2. Returns None if task doesn't exist or belongs to different user

    Args:
        db: Database session
        task_id: Task ID to retrieve
        user_id: ID of authenticated user (from JWT token)

    Returns:
        Task: Task object if found and owned by user
        None: If task doesn't exist or belongs to different user

    User Isolation:
        - Returns None for tasks owned by other users (FR-019)
        - Endpoint will return 404 for security (don't reveal existence)
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # User isolation enforced
    )
    task = db.exec(statement).first()
    return task


def update_task(
    db: Session,
    task_id: int,
    user_id: int,
    title: str,
    description: Optional[str]
) -> Task:
    """
    Update a task's title and/or description.

    This function:
    1. Validates task ownership via user_id filter (FR-023)
    2. Updates title and description
    3. Updates updated_at timestamp (FR-028)

    Args:
        db: Database session
        task_id: Task ID to update
        user_id: ID of authenticated user (from JWT token)
        title: New task title
        description: New task description (optional)

    Returns:
        Task: Updated task object

    Raises:
        NotFoundError: If task doesn't exist or belongs to different user

    User Isolation:
        - Only updates tasks owned by authenticated user (FR-023)
        - Returns 404 for tasks owned by other users (FR-019)
    """
    task = get_task_by_id(db, task_id, user_id)

    if not task:
        raise NotFoundError("Task not found")

    task.title = title.strip()
    task.description = description.strip() if description else None
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def toggle_task_completion(db: Session, task_id: int, user_id: int) -> Task:
    """
    Toggle a task's completion status.

    This function:
    1. Validates task ownership via user_id filter (FR-023)
    2. Toggles completed boolean (true ↔ false)
    3. Updates updated_at timestamp (FR-028)

    Args:
        db: Database session
        task_id: Task ID to toggle
        user_id: ID of authenticated user (from JWT token)

    Returns:
        Task: Updated task object with toggled completion status

    Raises:
        NotFoundError: If task doesn't exist or belongs to different user

    User Isolation:
        - Only toggles tasks owned by authenticated user (FR-023)
    """
    task = get_task_by_id(db, task_id, user_id)

    if not task:
        raise NotFoundError("Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    """
    Delete a task permanently.

    This function:
    1. Validates task ownership via user_id filter (FR-023)
    2. Deletes task from database

    Args:
        db: Database session
        task_id: Task ID to delete
        user_id: ID of authenticated user (from JWT token)

    Raises:
        NotFoundError: If task doesn't exist or belongs to different user

    User Isolation:
        - Only deletes tasks owned by authenticated user (FR-023)
        - Returns 404 for tasks owned by other users
    """
    task = get_task_by_id(db, task_id, user_id)

    if not task:
        raise NotFoundError("Task not found")

    db.delete(task)
    db.commit()
