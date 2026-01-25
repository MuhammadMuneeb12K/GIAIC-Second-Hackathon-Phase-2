# Quickstart Guide: Backend API Testing

**Feature**: Backend API for Multi-User Todo Application
**Branch**: 002-backend-api
**Date**: 2026-01-11
**Purpose**: Manual verification flows for testing backend implementation

## Overview

This guide provides step-by-step instructions for manually testing the backend API after implementation. These flows verify that all user stories are working correctly and that user isolation is properly enforced.

**Prerequisites**:
- Backend API is running (e.g., `http://localhost:8000`)
- API documentation is accessible at `/docs`
- Tool for making HTTP requests (curl, Postman, or browser)

---

## Test Flow 1: User Authentication (User Story 1 - P1)

### Objective

Verify that users can create accounts, sign in, and access protected endpoints with JWT tokens.

### Steps

**1. Create a new user account (Signup)**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "securepass123",
    "name": "Test User"
  }'
```

**Expected Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "name": "Test User",
    "created_at": "2026-01-11T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Verification**:
- ✅ Status code is 201
- ✅ Response includes user object (id, email, name, created_at)
- ✅ Response includes access_token and refresh_token
- ✅ password_hash is NOT included in response

**Save the access_token for subsequent requests**

---

**2. Attempt duplicate signup (should fail)**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "anotherpass456",
    "name": "Another User"
  }'
```

**Expected Response** (409 Conflict):
```json
{
  "detail": "Email already registered"
}
```

**Verification**:
- ✅ Status code is 409
- ✅ Error message indicates duplicate email

---

**3. Sign in with valid credentials**

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "securepass123"
  }'
```

**Expected Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "name": "Test User",
    "created_at": "2026-01-11T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ Response includes user object and tokens
- ✅ Tokens are different from signup tokens (new tokens issued)

---

**4. Attempt to access protected endpoint without token (should fail)**

```bash
curl -X GET http://localhost:8000/api/tasks
```

**Expected Response** (401 Unauthorized):
```json
{
  "detail": "Not authenticated"
}
```

**Verification**:
- ✅ Status code is 401
- ✅ Error message indicates missing authentication

---

**5. Access protected endpoint with valid token (should succeed)**

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (200 OK):
```json
[]
```

**Verification**:
- ✅ Status code is 200
- ✅ Response is empty array (user has no tasks yet)

---

**6. Refresh access token**

```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ New access_token is returned
- ✅ New token is different from previous token

---

**7. Sign out**

```bash
curl -X POST http://localhost:8000/api/auth/signout \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (200 OK):
```json
{
  "detail": "Successfully signed out"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ Success message returned

---

## Test Flow 2: Task Management (User Story 2 - P2)

### Objective

Verify that authenticated users can create, read, update, delete, and toggle completion of their tasks.

### Prerequisites

- User is signed in (use access_token from Test Flow 1)

### Steps

**1. Create a task with title only**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries"
  }'
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": null,
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:00:00Z"
}
```

**Verification**:
- ✅ Status code is 201
- ✅ Task has auto-generated id
- ✅ description is null
- ✅ completed is false (default)
- ✅ user_id matches authenticated user

---

**2. Create a task with title and description**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation for all endpoints"
  }'
```

**Expected Response** (201 Created):
```json
{
  "id": 2,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation for all endpoints",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:05:00Z",
  "updated_at": "2026-01-11T12:05:00Z"
}
```

**Verification**:
- ✅ Status code is 201
- ✅ description is included
- ✅ All fields are present

---

**3. List all tasks**

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": null,
    "completed": false,
    "user_id": 1,
    "created_at": "2026-01-11T12:00:00Z",
    "updated_at": "2026-01-11T12:00:00Z"
  },
  {
    "id": 2,
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation for all endpoints",
    "completed": false,
    "user_id": 1,
    "created_at": "2026-01-11T12:05:00Z",
    "updated_at": "2026-01-11T12:05:00Z"
  }
]
```

**Verification**:
- ✅ Status code is 200
- ✅ Array contains both tasks
- ✅ All tasks belong to authenticated user

---

**4. Get a single task**

```bash
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": null,
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:00:00Z"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ Correct task is returned

---

**5. Update a task**

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries (updated)",
    "description": "Milk, eggs, bread, and vegetables"
  }'
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, and vegetables",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:10:00Z"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ Title and description are updated
- ✅ updated_at timestamp is newer than created_at

---

**6. Toggle task completion**

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/toggle \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, and vegetables",
  "completed": true,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:15:00Z"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ completed is now true
- ✅ updated_at timestamp is updated

---

**7. Toggle task completion again (back to incomplete)**

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/toggle \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "title": "Buy groceries (updated)",
  "description": "Milk, eggs, bread, and vegetables",
  "completed": false,
  "user_id": 1,
  "created_at": "2026-01-11T12:00:00Z",
  "updated_at": "2026-01-11T12:16:00Z"
}
```

**Verification**:
- ✅ Status code is 200
- ✅ completed is now false (toggled back)

---

**8. Delete a task**

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (204 No Content):

No response body

**Verification**:
- ✅ Status code is 204
- ✅ No response body

---

**9. Verify task is deleted**

```bash
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <access_token>"
```

**Expected Response** (404 Not Found):
```json
{
  "detail": "Task not found"
}
```

**Verification**:
- ✅ Status code is 404
- ✅ Task no longer exists

---

## Test Flow 3: User Isolation (Security Verification)

### Objective

Verify that users can only access their own tasks and cannot access other users' tasks.

### Steps

**1. Create a second user**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user2@example.com",
    "password": "password456",
    "name": "User Two"
  }'
```

**Save the access_token for User 2**

---

**2. User 1 creates a task**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <user1_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "User 1 private task"
  }'
```

**Note the task ID (e.g., id: 3)**

---

**3. User 2 attempts to access User 1's task (should fail)**

```bash
curl -X GET http://localhost:8000/api/tasks/3 \
  -H "Authorization: Bearer <user2_access_token>"
```

**Expected Response** (404 Not Found):
```json
{
  "detail": "Task not found"
}
```

**Verification**:
- ✅ Status code is 404
- ✅ User 2 cannot see User 1's task (user isolation enforced)

---

**4. User 2 attempts to update User 1's task (should fail)**

```bash
curl -X PUT http://localhost:8000/api/tasks/3 \
  -H "Authorization: Bearer <user2_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hacked task"
  }'
```

**Expected Response** (404 Not Found):
```json
{
  "detail": "Task not found"
}
```

**Verification**:
- ✅ Status code is 404
- ✅ User 2 cannot update User 1's task

---

**5. User 2 attempts to delete User 1's task (should fail)**

```bash
curl -X DELETE http://localhost:8000/api/tasks/3 \
  -H "Authorization: Bearer <user2_access_token>"
```

**Expected Response** (404 Not Found):
```json
{
  "detail": "Task not found"
}
```

**Verification**:
- ✅ Status code is 404
- ✅ User 2 cannot delete User 1's task

---

**6. User 2 lists their tasks (should be empty)**

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <user2_access_token>"
```

**Expected Response** (200 OK):
```json
[]
```

**Verification**:
- ✅ Status code is 200
- ✅ User 2 sees empty array (no access to User 1's tasks)

---

## Test Flow 4: Validation and Error Handling (User Story 3 - P3)

### Objective

Verify that the API properly validates input and returns appropriate error responses.

### Steps

**1. Signup with invalid email format**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "password": "password123",
    "name": "Test User"
  }'
```

**Expected Response** (422 Unprocessable Entity):
```json
{
  "detail": "Invalid email format"
}
```

**Verification**:
- ✅ Status code is 422
- ✅ Error message indicates invalid email

---

**2. Signup with short password**

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "short",
    "name": "Test User"
  }'
```

**Expected Response** (422 Unprocessable Entity):
```json
{
  "detail": "Password must be at least 8 characters"
}
```

**Verification**:
- ✅ Status code is 422
- ✅ Error message indicates password too short

---

**3. Create task with missing title**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Task without title"
  }'
```

**Expected Response** (422 Unprocessable Entity):
```json
{
  "detail": "Title is required"
}
```

**Verification**:
- ✅ Status code is 422
- ✅ Error message indicates missing title

---

**4. Create task with title exceeding 200 characters**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "This is a very long title that exceeds the maximum allowed length of 200 characters. This is a very long title that exceeds the maximum allowed length of 200 characters. This is a very long title that exceeds the maximum allowed length of 200 characters."
  }'
```

**Expected Response** (422 Unprocessable Entity):
```json
{
  "detail": "Title must not exceed 200 characters"
}
```

**Verification**:
- ✅ Status code is 422
- ✅ Error message indicates title too long

---

**5. Send malformed JSON**

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Invalid JSON"'
```

**Expected Response** (400 Bad Request):
```json
{
  "detail": "Invalid JSON format"
}
```

**Verification**:
- ✅ Status code is 400
- ✅ Error message indicates malformed JSON

---

## Success Criteria Verification

### User Story 1: Authentication (P1)

- ✅ Users can create accounts (signup)
- ✅ Users can sign in with valid credentials
- ✅ JWT tokens are issued on signup and signin
- ✅ Protected endpoints require valid JWT token
- ✅ Expired/invalid tokens are rejected with 401
- ✅ Refresh tokens can be used to get new access tokens
- ✅ Users can sign out

### User Story 2: Task Management (P2)

- ✅ Users can create tasks with title only
- ✅ Users can create tasks with title and description
- ✅ Users can list all their tasks
- ✅ Users can get a single task by ID
- ✅ Users can update task title and description
- ✅ Users can toggle task completion status
- ✅ Users can delete tasks
- ✅ Empty task list returns empty array (not 404)

### User Story 3: Error Handling (P3)

- ✅ Invalid email format returns 422
- ✅ Short password returns 422
- ✅ Duplicate email returns 409
- ✅ Missing title returns 422
- ✅ Title too long returns 422
- ✅ Malformed JSON returns 400
- ✅ Missing authentication returns 401
- ✅ Non-existent task returns 404

### Security: User Isolation

- ✅ Users can only see their own tasks
- ✅ Users cannot access other users' tasks (404)
- ✅ Users cannot update other users' tasks (404)
- ✅ Users cannot delete other users' tasks (404)
- ✅ user_id is extracted from JWT, not request body

---

## Performance Verification

### Response Time Targets

**Authentication Endpoints** (NFR-009):
- Signup: <500ms
- Signin: <500ms

**Task Endpoints** (NFR-010):
- List tasks: <200ms (or <100ms for ≤1000 tasks per SC-007)
- Create task: <200ms
- Update task: <200ms
- Delete task: <200ms

**Verification Method**:
- Use curl with `-w "\nTime: %{time_total}s\n"` flag
- Or use Postman's response time display
- Or use API load testing tools (e.g., Apache Bench, wrk)

---

## Summary

This quickstart guide provides comprehensive manual testing flows for all three user stories:
1. User Authentication (P1) - 7 steps
2. Task Management (P2) - 9 steps
3. User Isolation (Security) - 6 steps
4. Validation and Error Handling (P3) - 5 steps

All tests verify specification compliance, user isolation enforcement, and proper error handling. Use this guide to manually verify the backend implementation before integration with the frontend.
