"""
Task Management API Endpoints.

This module implements task CRUD endpoints with user isolation:
- GET /api/tasks - List all user's tasks
- POST /api/tasks - Create new task
- GET /api/tasks/{id} - Get single task
- PUT /api/tasks/{id} - Update task
- PATCH /api/tasks/{id}/toggle - Toggle completion status
- DELETE /api/tasks/{id} - Delete task
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from app.services.task_service import (
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    toggle_task_completion,
    delete_task,
)
from app.core.exceptions import NotFoundError


router = APIRouter()


@router.get("", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all tasks for authenticated user (GET /api/tasks).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Retrieves all tasks owned by authenticated user
    3. Returns array of task objects (empty array if no tasks)

    Headers:
        - Authorization: Bearer <access_token>

    Response (200 OK):
        - Array of task objects with all fields
        - Empty array if user has no tasks (not 404)

    Errors:
        - 401: Missing or invalid token

    User Isolation:
        - Only returns tasks where user_id matches authenticated user (FR-023)
        - Users cannot see other users' tasks (SC-003)

    Performance:
        - Target: <100ms for users with up to 1000 tasks (SC-007)
        - Optimized with user_id index (NFR-011)
    """
    user_id = current_user["user_id"]
    tasks = get_user_tasks(db, user_id)
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    request: CreateTaskRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task (POST /api/tasks).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Validates request data (title required, description optional)
    3. Creates task owned by authenticated user
    4. Returns created task object

    Headers:
        - Authorization: Bearer <access_token>

    Request Body:
        - title: Task title (required, max 200 characters)
        - description: Task description (optional, max 2000 characters)

    Response (201 Created):
        - Task object with all fields
        - completed defaults to false (FR-026)
        - user_id set from authenticated user (FR-016)

    Errors:
        - 400: Malformed JSON
        - 401: Missing or invalid token
        - 422: Validation error (missing title, title too long, etc.)

    Security:
        - user_id extracted from JWT, never from request body (FR-016)
    """
    user_id = current_user["user_id"]
    task = create_task(
        db=db,
        title=request.title,
        description=request.description,
        user_id=user_id,
    )
    return task


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single task by ID (GET /api/tasks/{id}).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Retrieves task by ID with user isolation
    3. Returns task object if owned by authenticated user

    Headers:
        - Authorization: Bearer <access_token>

    Path Parameters:
        - task_id: Task ID to retrieve

    Response (200 OK):
        - Task object with all fields

    Errors:
        - 401: Missing or invalid token
        - 404: Task not found or belongs to different user (FR-019)

    User Isolation:
        - Returns 404 for tasks owned by other users (FR-019)
        - Doesn't reveal existence of other users' tasks (security)
    """
    user_id = current_user["user_id"]
    task = get_task_by_id(db, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_existing_task(
    task_id: int,
    request: UpdateTaskRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task (PUT /api/tasks/{id}).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Validates request data (title and description)
    3. Updates task if owned by authenticated user
    4. Updates updated_at timestamp (FR-028)

    Headers:
        - Authorization: Bearer <access_token>

    Path Parameters:
        - task_id: Task ID to update

    Request Body:
        - title: New task title (required, max 200 characters)
        - description: New task description (optional, max 2000 characters)

    Response (200 OK):
        - Updated task object with all fields
        - updated_at timestamp is updated

    Errors:
        - 400: Malformed JSON
        - 401: Missing or invalid token
        - 404: Task not found or belongs to different user (FR-019)
        - 422: Validation error

    User Isolation:
        - Only updates tasks owned by authenticated user (FR-023)
    """
    user_id = current_user["user_id"]

    try:
        task = update_task(
            db=db,
            task_id=task_id,
            user_id=user_id,
            title=request.title,
            description=request.description,
        )
        return task
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{task_id}/toggle", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def toggle_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle task completion status (PATCH /api/tasks/{id}/toggle).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Toggles completed status (true ↔ false)
    3. Updates updated_at timestamp (FR-028)

    Headers:
        - Authorization: Bearer <access_token>

    Path Parameters:
        - task_id: Task ID to toggle

    Request Body: None (empty)

    Response (200 OK):
        - Updated task object with toggled completion status
        - updated_at timestamp is updated

    Errors:
        - 401: Missing or invalid token
        - 404: Task not found or belongs to different user

    User Isolation:
        - Only toggles tasks owned by authenticated user (FR-023)
    """
    user_id = current_user["user_id"]

    try:
        task = toggle_task_completion(db=db, task_id=task_id, user_id=user_id)
        return task
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task (DELETE /api/tasks/{id}).

    This endpoint:
    1. Validates JWT token (requires authentication)
    2. Deletes task if owned by authenticated user
    3. Returns 204 No Content on success

    Headers:
        - Authorization: Bearer <access_token>

    Path Parameters:
        - task_id: Task ID to delete

    Response (204 No Content):
        - No response body (successful deletion)

    Errors:
        - 401: Missing or invalid token
        - 404: Task not found or belongs to different user

    User Isolation:
        - Only deletes tasks owned by authenticated user (FR-023)
    """
    user_id = current_user["user_id"]

    try:
        delete_task(db=db, task_id=task_id, user_id=user_id)
        return None  # 204 No Content
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
