# API Contract: Task Endpoints

**Feature**: Backend API for Multi-User Todo Application
**Domain**: Task Management
**Base Path**: `/api/tasks`
**Date**: 2026-01-11

## Overview

This contract defines all task management endpoints for creating, reading, updating, deleting, and toggling completion status of tasks. All endpoints require authentication and enforce strict user isolation.

**Security**: All endpoints in this contract require a valid JWT access token in the Authorization header.

---

## Endpoint: GET /api/tasks

### Description

Retrieves all tasks owned by the authenticated user. Returns an array of task objects. User isolation is enforced - users can only see their own tasks.

### Specification Reference

- **User Story**: User Story 2 - Task Management with User Isolation (P2)
- **Functional Requirements**: FR-017, FR-023
- **Success Criteria**: SC-003, SC-007

### Request

**Method**: `GET`
**Path**: `/api/tasks`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Query Parameters**: None (no pagination in MVP)

### Response

**Success Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation for all endpoints",
    "completed": false,
    "user_id": 1,
    "created_at": "2026-01-11T12:00:00Z",
    "updated_at": "2026-01-11T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Review pull requests",
    "description": null,
    "completed": true,
    "user_id": 1,
    "created_at": "2026-01-11T10:00:00Z",
    "updated_at": "2026-01-11T11:30:00Z"
  }
]
```

**Empty List Response** (200 OK):
```json
[]
```

**Note**: Returns empty array (not 404) when user has no tasks (per spec edge cases)

**Response Fields**:
- `id`: Unique task identifier
- `title`: Task title (max 200 characters)
- `description`: Optional task description (max 2000 characters, null if not provided)
- `completed`: Task completion status (boolean)
- `user_id`: Owner's user ID (always matches authenticated user)
- `created_at`: ISO 8601 timestamp of task creation
- `updated_at`: ISO 8601 timestamp of last update

### Error Responses

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Performance

- **Target**: <100ms for users with up to 1000 tasks (SC-007)
- **Optimization**: user_id index on tasks table (NFR-011)

### User Isolation

- Query automatically filters by `user_id = current_user.id` (FR-023)
- User ID extracted from validated JWT token (FR-014)
- Users can only see their own tasks (SC-003)

---

## Endpoint: POST /api/tasks

### Description

Creates a new task for the authenticated user. Title is required, description is optional. Task is automatically associated with the authenticated user.

### Specification Reference

- **User Story**: User Story 2 - Task Management with User Isolation (P2)
- **Functional Requirements**: FR-015, FR-016, FR-024, FR-025, FR-026, FR-027
- **Success Criteria**: SC-003, SC-005

### Request

**Method**: `POST`
**Path**: `/api/tasks`
**Content-Type**: `application/json`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body Schema**:
```json
{
  "title": "string (required, min 1 char, max 200 chars)",
  "description": "string (optional, max 2000 chars)"
}
```

**Request Body Example**:
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for all endpoints"
}
```

**Validation Rules**:
- `title`: Required, not empty, max 200 characters (FR-024)
- `description`: Optional, max 2000 characters if provided (FR-025)
- `user_id`: Automatically set from JWT token, never accepted from request body (FR-016)
- `completed`: Automatically set to false (FR-026)

### Response

**Success Response** (201 Created):
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for all endpoints",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:00:00Z"
}
```

### Error Responses

**400 Bad Request** (Malformed JSON):
```json
{
  "detail": "Invalid JSON format"
}
```

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**422 Unprocessable Entity** (Missing Title):
```json
{
  "detail": "Title is required"
}
```

**422 Unprocessable Entity** (Title Too Long):
```json
{
  "detail": "Title must not exceed 200 characters"
}
```

**422 Unprocessable Entity** (Description Too Long):
```json
{
  "detail": "Description must not exceed 2000 characters"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Performance

- **Target**: <200ms under normal load (NFR-010)

### Security

- `user_id` extracted from JWT token, never from request body (FR-016)
- Input validation prevents XSS attacks (NFR-004)

---

## Endpoint: GET /api/tasks/{id}

### Description

Retrieves a single task by ID. User isolation is enforced - returns 404 if task doesn't exist or belongs to a different user.

### Specification Reference

- **User Story**: User Story 2 - Task Management with User Isolation (P2)
- **Functional Requirements**: FR-018, FR-019, FR-023
- **Success Criteria**: SC-003

### Request

**Method**: `GET`
**Path**: `/api/tasks/{id}`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID (integer)

### Response

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for all endpoints",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:00:00Z"
}
```

### Error Responses

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** (Task Not Found or Belongs to Different User):
```json
{
  "detail": "Task not found"
}
```

**Note**: Returns 404 for both non-existent tasks and tasks owned by other users (security best practice - don't reveal existence of other users' tasks)

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### User Isolation

- Query filters by both `id` and `user_id` (FR-019, FR-023)
- Returns 404 if task belongs to different user (security requirement)

---

## Endpoint: PUT /api/tasks/{id}

### Description

Updates an existing task's title and/or description. User isolation is enforced - returns 404 if task doesn't exist or belongs to a different user.

### Specification Reference

- **User Story**: User Story 2 - Task Management with User Isolation (P2)
- **Functional Requirements**: FR-020, FR-023, FR-024, FR-025, FR-028
- **Success Criteria**: SC-003, SC-005

### Request

**Method**: `PUT`
**Path**: `/api/tasks/{id}`
**Content-Type**: `application/json`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID (integer)

**Request Body Schema**:
```json
{
  "title": "string (required, min 1 char, max 200 chars)",
  "description": "string (optional, max 2000 chars)"
}
```

**Request Body Example**:
```json
{
  "title": "Complete project documentation (updated)",
  "description": "Write comprehensive API documentation for all endpoints and add examples"
}
```

**Validation Rules**:
- `title`: Required, not empty, max 200 characters (FR-024)
- `description`: Optional, max 2000 characters if provided (FR-025)
- `updated_at`: Automatically updated to current timestamp (FR-028)

### Response

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project documentation (updated)",
  "description": "Write comprehensive API documentation for all endpoints and add examples",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T13:30:00Z"
}
```

### Error Responses

**400 Bad Request** (Malformed JSON):
```json
{
  "detail": "Invalid JSON format"
}
```

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** (Task Not Found or Belongs to Different User):
```json
{
  "detail": "Task not found"
}
```

**422 Unprocessable Entity** (Validation Error):
```json
{
  "detail": "Title must not exceed 200 characters"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Performance

- **Target**: <200ms under normal load (NFR-010)

### User Isolation

- Query filters by both `id` and `user_id` (FR-023)
- Returns 404 if task belongs to different user (FR-019)

---

## Endpoint: PATCH /api/tasks/{id}/toggle

### Description

Toggles the completion status of a task (completed: true ↔ false). User isolation is enforced.

### Specification Reference

- **User Story**: User Story 2 - Task Management with User Isolation (P2)
- **Functional Requirements**: FR-021, FR-023, FR-028
- **Success Criteria**: SC-003

### Request

**Method**: `PATCH`
**Path**: `/api/tasks/{id}/toggle`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID (integer)

**Request Body**: Empty (no body required)

### Response

**Success Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for all endpoints",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T13:45:00Z"
}
```

**Note**: `completed` field is toggled (false → true or true → false)

### Error Responses

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** (Task Not Found or Belongs to Different User):
```json
{
  "detail": "Task not found"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Performance

- **Target**: <200ms under normal load (NFR-010)

### User Isolation

- Query filters by both `id` and `user_id` (FR-023)
- Returns 404 if task belongs to different user

---

## Endpoint: DELETE /api/tasks/{id}

### Description

Deletes a task permanently. User isolation is enforced - returns 404 if task doesn't exist or belongs to a different user.

### Specification Reference

- **User Story**: User Story 2 - Task Management with User Isolation (P2)
- **Functional Requirements**: FR-022, FR-023
- **Success Criteria**: SC-003

### Request

**Method**: `DELETE`
**Path**: `/api/tasks/{id}`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
```

**Path Parameters**:
- `id`: Task ID (integer)

### Response

**Success Response** (204 No Content):

No response body (HTTP 204 status indicates successful deletion)

### Error Responses

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** (Task Not Found or Belongs to Different User):
```json
{
  "detail": "Task not found"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Performance

- **Target**: <200ms under normal load (NFR-010)

### User Isolation

- Query filters by both `id` and `user_id` (FR-023)
- Returns 404 if task belongs to different user

---

## Common Patterns

### Authentication

**All task endpoints require**:
```
Authorization: Bearer <access_token>
```

**JWT Validation**:
- Verify signature using BETTER_AUTH_SECRET (FR-013)
- Check expiration timestamp (FR-013)
- Extract user_id from token payload (FR-014)

### User Isolation Pattern

**All queries must filter by user_id**:
```python
# Correct pattern
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == current_user.id  # User isolation
).first()

# Incorrect pattern (NEVER DO THIS)
task = db.query(Task).filter(Task.id == task_id).first()
```

### Error Response Format

**All errors follow consistent format**:
```json
{
  "detail": "Error message here"
}
```

---

## Frontend Integration

### Expected Frontend Behavior

1. **List Tasks**:
   - GET /api/tasks with Authorization header
   - Display all tasks in UI
   - Handle empty array gracefully

2. **Create Task**:
   - POST /api/tasks with title and optional description
   - Add new task to UI immediately (optimistic update)
   - Rollback on error

3. **Update Task**:
   - PUT /api/tasks/{id} with updated data
   - Update UI immediately (optimistic update)
   - Rollback on error

4. **Toggle Completion**:
   - PATCH /api/tasks/{id}/toggle
   - Toggle UI immediately (optimistic update)
   - Rollback on error

5. **Delete Task**:
   - DELETE /api/tasks/{id}
   - Remove from UI immediately (optimistic update)
   - Rollback on error

### Frontend TypeScript Types

```typescript
// Task type
interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

// Request types
interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface UpdateTaskRequest {
  title: string;
  description?: string;
}

// Response types
type TaskListResponse = Task[];
type TaskResponse = Task;

interface ErrorResponse {
  detail: string;
}
```

---

## Testing Checklist

### Functional Tests

- [ ] GET /api/tasks returns all user's tasks
- [ ] GET /api/tasks returns empty array when user has no tasks
- [ ] POST /api/tasks creates task with title only
- [ ] POST /api/tasks creates task with title and description
- [ ] POST /api/tasks returns 422 for missing title
- [ ] POST /api/tasks returns 422 for title exceeding 200 chars
- [ ] POST /api/tasks returns 422 for description exceeding 2000 chars
- [ ] GET /api/tasks/{id} returns task if owned by user
- [ ] GET /api/tasks/{id} returns 404 if task belongs to different user
- [ ] PUT /api/tasks/{id} updates task if owned by user
- [ ] PUT /api/tasks/{id} returns 404 if task belongs to different user
- [ ] PATCH /api/tasks/{id}/toggle toggles completion status
- [ ] DELETE /api/tasks/{id} deletes task if owned by user
- [ ] DELETE /api/tasks/{id} returns 404 if task belongs to different user

### Security Tests

- [ ] All endpoints require valid JWT token
- [ ] Expired JWT token is rejected with 401
- [ ] Invalid JWT signature is rejected with 401
- [ ] User cannot access another user's tasks (user isolation)
- [ ] User cannot update another user's tasks
- [ ] User cannot delete another user's tasks
- [ ] user_id is extracted from JWT, not request body

### Performance Tests

- [ ] GET /api/tasks completes in <100ms for 1000 tasks
- [ ] POST /api/tasks completes in <200ms
- [ ] PUT /api/tasks/{id} completes in <200ms
- [ ] DELETE /api/tasks/{id} completes in <200ms

---

## Summary

This contract defines 6 task management endpoints: list, create, get single, update, toggle completion, and delete. All endpoints require authentication and enforce strict user isolation. Users can only access their own tasks. Error responses follow consistent format with "detail" field. Performance targets are <100ms for list operations and <200ms for CRUD operations.
