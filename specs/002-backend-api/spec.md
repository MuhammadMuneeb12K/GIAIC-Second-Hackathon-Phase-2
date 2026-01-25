# Feature Specification: Backend API for Multi-User Todo Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-11
**Status**: Draft
**Input**: User description: "Create complete, secure, frontend-compatible backend specification for Full-Stack Todo Web Application using FastAPI, SQLModel, Neon PostgreSQL, and Better Auth (JWT)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication and Account Management (Priority: P1) 🎯 MVP

Users need to create accounts, sign in securely, and maintain authenticated sessions to access their personal todo lists. The system must provide JWT-based authentication that integrates seamlessly with the existing Next.js frontend.

**Why this priority**: Authentication is the foundation of the entire application. Without secure user authentication, no other features can function. This is the absolute minimum viable product - users must be able to create accounts and sign in before they can manage tasks.

**Independent Test**: Can be fully tested by creating a new user account via POST /api/auth/signup, signing in via POST /api/auth/signin to receive a JWT token, and using that token to access a protected endpoint. Delivers immediate value by securing the application and enabling user-specific data isolation.

**Acceptance Scenarios**:

1. **Given** no existing account, **When** user submits valid signup data (email, password, name) to POST /api/auth/signup, **Then** system creates user account, returns 201 status with user object (id, email, name, created_at) and JWT tokens (access_token, refresh_token)

2. **Given** existing user account, **When** user submits valid credentials to POST /api/auth/signin, **Then** system validates credentials, returns 200 status with user object and JWT tokens

3. **Given** authenticated user with valid JWT, **When** user makes request to protected endpoint with Authorization header, **Then** system validates token, extracts user_id, and allows access to user-specific resources

4. **Given** authenticated user, **When** user submits signout request to POST /api/auth/signout, **Then** system invalidates tokens and returns 200 status

5. **Given** expired access token and valid refresh token, **When** user submits refresh request to POST /api/auth/refresh, **Then** system validates refresh token and issues new access token

6. **Given** invalid or missing JWT, **When** user attempts to access protected endpoint, **Then** system returns 401 Unauthorized with clear error message

---

### User Story 2 - Task Management with User Isolation (Priority: P2)

Authenticated users need to create, read, update, delete, and toggle completion status of their personal tasks. All task operations must enforce strict user isolation - users can only access their own tasks.

**Why this priority**: Task management is the core business functionality of the application. Once users can authenticate (P1), they need to be able to manage their tasks. This delivers the primary value proposition of the todo application.

**Independent Test**: Can be fully tested by authenticating a user, creating multiple tasks via POST /api/tasks, retrieving them via GET /api/tasks, updating a task via PUT /api/tasks/{id}, toggling completion via PATCH /api/tasks/{id}/toggle, and deleting a task via DELETE /api/tasks/{id}. Verify that tasks created by one user are not accessible to another user.

**Acceptance Scenarios**:

1. **Given** authenticated user, **When** user submits POST /api/tasks with title and optional description, **Then** system creates task owned by user, returns 201 status with task object (id, title, description, completed, created_at, updated_at, user_id)

2. **Given** authenticated user with existing tasks, **When** user requests GET /api/tasks, **Then** system returns 200 status with array of tasks owned by user only (user isolation enforced)

3. **Given** authenticated user and existing task owned by user, **When** user requests GET /api/tasks/{id}, **Then** system returns 200 status with task details

4. **Given** authenticated user and task owned by different user, **When** user requests GET /api/tasks/{id}, **Then** system returns 404 Not Found (user isolation enforced)

5. **Given** authenticated user and existing task owned by user, **When** user submits PUT /api/tasks/{id} with updated title/description, **Then** system updates task, returns 200 status with updated task object

6. **Given** authenticated user and existing task owned by user, **When** user submits PATCH /api/tasks/{id}/toggle, **Then** system toggles completed status, returns 200 status with updated task object

7. **Given** authenticated user and existing task owned by user, **When** user submits DELETE /api/tasks/{id}, **Then** system deletes task, returns 204 No Content

8. **Given** authenticated user and task owned by different user, **When** user attempts to update/delete task, **Then** system returns 404 Not Found (user isolation enforced)

---

### User Story 3 - API Error Handling and Data Validation (Priority: P3)

The API must provide consistent, user-friendly error responses and validate all input data to ensure data integrity and security. This includes validation errors, authentication errors, authorization errors, and server errors.

**Why this priority**: While authentication and task management are functional, production-ready APIs require robust error handling and validation. This ensures a professional user experience and prevents invalid data from entering the system.

**Independent Test**: Can be fully tested by submitting invalid data to various endpoints (missing required fields, invalid email format, password too short, invalid task ID, malformed JSON) and verifying that appropriate error responses are returned with clear error messages and correct HTTP status codes.

**Acceptance Scenarios**:

1. **Given** signup request with invalid email format, **When** user submits POST /api/auth/signup, **Then** system returns 422 Unprocessable Entity with validation error details

2. **Given** signup request with password shorter than 8 characters, **When** user submits POST /api/auth/signup, **Then** system returns 422 Unprocessable Entity with password validation error

3. **Given** signup request with existing email, **When** user submits POST /api/auth/signup, **Then** system returns 409 Conflict with clear error message

4. **Given** signin request with incorrect password, **When** user submits POST /api/auth/signin, **Then** system returns 401 Unauthorized with generic error message (security best practice)

5. **Given** task creation request with missing title, **When** user submits POST /api/tasks, **Then** system returns 422 Unprocessable Entity with validation error

6. **Given** task creation request with title exceeding 200 characters, **When** user submits POST /api/tasks, **Then** system returns 422 Unprocessable Entity with validation error

7. **Given** request to non-existent task ID, **When** user submits GET /api/tasks/{invalid_id}, **Then** system returns 404 Not Found with clear error message

8. **Given** malformed JSON in request body, **When** user submits POST request, **Then** system returns 400 Bad Request with parsing error details

9. **Given** internal server error occurs, **When** user makes any request, **Then** system returns 500 Internal Server Error with generic error message (no sensitive details exposed)

---

### Edge Cases

- **Concurrent task updates**: What happens when two clients attempt to update the same task simultaneously? System should use database-level constraints and return appropriate conflict errors.

- **Token expiration during request**: What happens when JWT expires mid-request? System should validate token at request start and return 401 if expired.

- **Database connection failure**: How does system handle database unavailability? System should return 503 Service Unavailable and log error for monitoring.

- **Duplicate email registration**: What happens when two users attempt to register with same email simultaneously? Database unique constraint should prevent duplicates, return 409 Conflict.

- **Very long task descriptions**: What happens when user submits task description exceeding reasonable length? System should enforce maximum length (e.g., 2000 characters) and return validation error.

- **Special characters in task data**: How does system handle special characters, emojis, and Unicode in task titles/descriptions? System should properly encode/decode UTF-8 and store safely in PostgreSQL.

- **Deleted user's tasks**: What happens to tasks when user account is deleted? System should cascade delete all user's tasks or implement soft delete strategy.

- **Invalid JWT signature**: What happens when JWT is tampered with? System should detect invalid signature and return 401 Unauthorized.

- **Refresh token reuse**: What happens when refresh token is used multiple times? System should implement token rotation or single-use refresh tokens for security.

- **Empty task list**: What happens when user has no tasks? System should return 200 OK with empty array, not 404.

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Authorization

- **FR-001**: System MUST provide POST /api/auth/signup endpoint accepting email, password, and name to create new user accounts
- **FR-002**: System MUST validate email format using standard email regex pattern
- **FR-003**: System MUST enforce minimum password length of 8 characters
- **FR-004**: System MUST hash passwords using bcrypt or argon2 before storing in database
- **FR-005**: System MUST prevent duplicate email registration by enforcing unique constraint on email field
- **FR-006**: System MUST provide POST /api/auth/signin endpoint accepting email and password to authenticate users
- **FR-007**: System MUST generate JWT access tokens containing user_id and exp (expiration) claims
- **FR-008**: System MUST sign JWT tokens using BETTER_AUTH_SECRET from environment variables
- **FR-009**: System MUST set access token expiration to 15 minutes
- **FR-010**: System MUST generate refresh tokens with 7-day expiration
- **FR-011**: System MUST provide POST /api/auth/refresh endpoint accepting refresh token to issue new access token
- **FR-012**: System MUST provide POST /api/auth/signout endpoint to invalidate user session
- **FR-013**: System MUST validate JWT on all protected endpoints by verifying signature and expiration
- **FR-014**: System MUST extract user_id from validated JWT and use for user isolation

#### Task Management

- **FR-015**: System MUST provide POST /api/tasks endpoint accepting title (required) and description (optional) to create tasks
- **FR-016**: System MUST automatically associate created tasks with authenticated user's user_id
- **FR-017**: System MUST provide GET /api/tasks endpoint returning array of tasks owned by authenticated user only
- **FR-018**: System MUST provide GET /api/tasks/{id} endpoint returning single task if owned by authenticated user
- **FR-019**: System MUST return 404 Not Found when user attempts to access task owned by different user
- **FR-020**: System MUST provide PUT /api/tasks/{id} endpoint accepting title and description to update task
- **FR-021**: System MUST provide PATCH /api/tasks/{id}/toggle endpoint to toggle task completion status
- **FR-022**: System MUST provide DELETE /api/tasks/{id} endpoint to delete task
- **FR-023**: System MUST enforce user isolation on all task operations (update, delete, read)
- **FR-024**: System MUST validate task title is not empty and does not exceed 200 characters
- **FR-025**: System MUST validate task description does not exceed 2000 characters if provided
- **FR-026**: System MUST set completed field to false by default when creating new tasks
- **FR-027**: System MUST automatically set created_at timestamp when creating tasks
- **FR-028**: System MUST automatically update updated_at timestamp when modifying tasks

#### Data Validation & Error Handling

- **FR-029**: System MUST return 422 Unprocessable Entity for validation errors with detailed error messages
- **FR-030**: System MUST return 401 Unauthorized for missing or invalid JWT tokens
- **FR-031**: System MUST return 404 Not Found for non-existent resources or unauthorized access attempts
- **FR-032**: System MUST return 409 Conflict for duplicate email registration attempts
- **FR-033**: System MUST return 400 Bad Request for malformed JSON or invalid request format
- **FR-034**: System MUST return 500 Internal Server Error for unexpected server errors without exposing sensitive details
- **FR-035**: System MUST return consistent error response format with "detail" field containing error message
- **FR-036**: System MUST validate all request bodies against defined schemas before processing

#### API Contract & Frontend Integration

- **FR-037**: System MUST accept JWT tokens in Authorization header with "Bearer {token}" format
- **FR-038**: System MUST return JSON responses with appropriate Content-Type header
- **FR-039**: System MUST enable CORS for frontend origin (configurable via environment variable)
- **FR-040**: System MUST return user object (id, email, name, created_at) in signup and signin responses
- **FR-041**: System MUST return both access_token and refresh_token in authentication responses
- **FR-042**: System MUST return task objects with all fields (id, title, description, completed, created_at, updated_at, user_id)

### Key Entities

- **User**: Represents a registered user account with authentication credentials
  - Attributes: id (UUID/integer), email (unique, indexed), password_hash, name, created_at, updated_at
  - Relationships: One user has many tasks (one-to-many)
  - Constraints: Email must be unique, password_hash must not be null

- **Task**: Represents a todo item owned by a specific user
  - Attributes: id (UUID/integer), title (required, max 200 chars), description (optional, max 2000 chars), completed (boolean, default false), user_id (foreign key), created_at, updated_at
  - Relationships: Many tasks belong to one user (many-to-one)
  - Constraints: user_id must reference valid user, title must not be empty, user_id must be indexed for query performance

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully create accounts and sign in, receiving valid JWT tokens that work with frontend application
- **SC-002**: All protected endpoints correctly validate JWT tokens and reject invalid/expired tokens with 401 status
- **SC-003**: User isolation is enforced - users can only access their own tasks, never tasks belonging to other users
- **SC-004**: API returns consistent error responses with appropriate HTTP status codes and clear error messages
- **SC-005**: All validation rules are enforced - invalid data is rejected with 422 status and detailed validation errors
- **SC-006**: API handles at least 100 concurrent requests without errors or significant performance degradation
- **SC-007**: Database queries for task retrieval complete in under 100ms for users with up to 1000 tasks
- **SC-008**: Frontend can successfully integrate with all API endpoints without CORS errors or authentication issues
- **SC-009**: API documentation (OpenAPI/Swagger) is automatically generated and accessible at /docs endpoint
- **SC-010**: All database operations use transactions to ensure data consistency and prevent partial updates

### Technical Success Criteria

- **SC-011**: FastAPI application starts successfully and serves requests on configured port
- **SC-012**: SQLModel models correctly map to PostgreSQL database schema with proper constraints
- **SC-013**: Database migrations can be applied and rolled back without data loss
- **SC-014**: Environment variables are properly loaded and validated at application startup
- **SC-015**: JWT tokens are correctly signed and verified using BETTER_AUTH_SECRET
- **SC-016**: Password hashing uses secure algorithm (bcrypt/argon2) with appropriate cost factor
- **SC-017**: API responses include appropriate HTTP headers (Content-Type, CORS headers)
- **SC-018**: Error responses never expose sensitive information (stack traces, database details, secrets)
- **SC-019**: All endpoints are properly typed with Pydantic models for request/response validation
- **SC-020**: Database connection pooling is configured for optimal performance

## Non-Functional Requirements

### Security

- **NFR-001**: All passwords MUST be hashed using bcrypt or argon2 with minimum cost factor of 12
- **NFR-002**: JWT tokens MUST be signed using HS256 algorithm with BETTER_AUTH_SECRET from environment
- **NFR-003**: BETTER_AUTH_SECRET MUST be at least 32 characters and stored securely (never in code)
- **NFR-004**: API MUST validate and sanitize all user input to prevent SQL injection and XSS attacks
- **NFR-005**: API MUST implement rate limiting to prevent brute force attacks on authentication endpoints
- **NFR-006**: API MUST use HTTPS in production (enforced at deployment level)
- **NFR-007**: Error messages MUST NOT expose sensitive information (database structure, stack traces, secrets)
- **NFR-008**: Database credentials MUST be stored in environment variables, never in code

### Performance

- **NFR-009**: Authentication endpoints (signup, signin) MUST respond within 500ms under normal load
- **NFR-010**: Task CRUD endpoints MUST respond within 200ms under normal load
- **NFR-011**: Database queries MUST use indexes on frequently queried fields (user_id, email)
- **NFR-012**: API MUST handle at least 100 concurrent requests without degradation
- **NFR-013**: Database connection pool MUST be configured with appropriate min/max connections

### Reliability

- **NFR-014**: API MUST implement proper error handling for database connection failures
- **NFR-015**: API MUST log all errors with sufficient context for debugging
- **NFR-016**: API MUST return appropriate HTTP status codes for all error conditions
- **NFR-017**: Database transactions MUST be used for operations that modify multiple records

### Maintainability

- **NFR-018**: Code MUST follow FastAPI best practices and project structure conventions
- **NFR-019**: All endpoints MUST be documented with OpenAPI/Swagger annotations
- **NFR-020**: Database models MUST use SQLModel for type safety and validation
- **NFR-021**: Environment configuration MUST use Pydantic Settings for validation
- **NFR-022**: Code MUST include type hints for all functions and methods

### Compatibility

- **NFR-023**: API MUST be compatible with existing Next.js frontend (axios client, JWT format)
- **NFR-024**: API MUST enable CORS for frontend origin specified in environment variables
- **NFR-025**: API MUST accept JWT tokens in Authorization header with "Bearer {token}" format
- **NFR-026**: API MUST return JSON responses compatible with frontend TypeScript types
- **NFR-027**: Error response format MUST match frontend expectations (detail field)

## Technical Constraints

### Technology Stack (Fixed)

- **Backend Framework**: FastAPI (latest stable version)
- **ORM**: SQLModel (for type-safe database operations)
- **Database**: Neon PostgreSQL (serverless PostgreSQL)
- **Authentication**: Better Auth pattern with JWT tokens
- **Password Hashing**: bcrypt or argon2
- **Environment Management**: python-dotenv or Pydantic Settings

### Architecture Constraints

- **Monorepo Structure**: Backend code must reside in `backend/` directory at repository root
- **API Prefix**: All endpoints must be under `/api` prefix (e.g., `/api/auth/signup`, `/api/tasks`)
- **No Session-Based Auth**: Must use JWT tokens only, no server-side sessions
- **RESTful Design**: Must follow REST principles for endpoint design
- **User Isolation**: All data access must be scoped to authenticated user

### Database Constraints

- **PostgreSQL Compatibility**: All database features must be compatible with PostgreSQL
- **SQLModel Models**: All database models must use SQLModel (not raw SQLAlchemy)
- **Foreign Key Constraints**: Must enforce referential integrity at database level
- **Unique Constraints**: Must enforce uniqueness constraints at database level (e.g., email)
- **Indexes**: Must create indexes on frequently queried fields (user_id, email)

### Frontend Integration Constraints

- **JWT Format**: Access tokens must contain `user_id` and `exp` claims at minimum
- **Token Expiration**: Access tokens expire in 15 minutes, refresh tokens in 7 days
- **Error Format**: Errors must return JSON with `detail` field containing error message
- **CORS**: Must enable CORS for frontend origin (configurable)
- **Response Format**: Authentication responses must include user object and tokens

## Out of Scope

The following features are explicitly excluded from this specification:

- **Email Verification**: No email verification or confirmation required for signup
- **Password Reset**: No password reset or forgot password functionality
- **OAuth/Social Login**: No third-party authentication providers (Google, GitHub, etc.)
- **Task Sharing**: No ability to share tasks with other users
- **Task Categories/Tags**: No categorization or tagging of tasks
- **Task Priorities**: No priority levels for tasks
- **Task Due Dates**: No due date or deadline functionality
- **Task Attachments**: No file uploads or attachments
- **Real-time Updates**: No WebSocket or Server-Sent Events for live updates
- **Task Search**: No full-text search functionality
- **Task Filtering**: No advanced filtering beyond basic user isolation
- **Task Sorting**: No custom sorting options (default chronological order)
- **Pagination**: No pagination for task lists (return all user's tasks)
- **User Profile Management**: No ability to update user profile (name, email, password)
- **User Deletion**: No account deletion functionality
- **Admin Panel**: No administrative interface or admin users
- **Audit Logging**: No detailed audit trail of user actions
- **Multi-tenancy**: No organization or team features
- **API Versioning**: No versioned API endpoints (single version)
- **GraphQL**: No GraphQL API, REST only
- **Caching**: No Redis or caching layer
- **Background Jobs**: No asynchronous task processing or job queues
- **Notifications**: No email or push notifications
- **Analytics**: No usage analytics or metrics tracking

## Dependencies

### External Services

- **Neon PostgreSQL**: Serverless PostgreSQL database (connection string required in environment)
- **Frontend Application**: Next.js application at configurable origin (for CORS)

### Environment Variables Required

- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT signing (minimum 32 characters)
- `FRONTEND_URL`: Frontend origin for CORS configuration
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration (default: 15)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration (default: 7)

### Python Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `sqlmodel`: ORM and database models
- `psycopg2-binary` or `asyncpg`: PostgreSQL driver
- `python-jose[cryptography]`: JWT token handling
- `passlib[bcrypt]`: Password hashing
- `python-dotenv`: Environment variable management
- `pydantic`: Data validation
- `pydantic-settings`: Settings management

## API Endpoint Summary

### Authentication Endpoints

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate user and issue tokens
- `POST /api/auth/signout` - Invalidate user session
- `POST /api/auth/refresh` - Refresh access token using refresh token

### Task Endpoints (All Protected)

- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create new task for authenticated user
- `GET /api/tasks/{id}` - Get single task by ID (user isolation enforced)
- `PUT /api/tasks/{id}` - Update task by ID (user isolation enforced)
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status (user isolation enforced)
- `DELETE /api/tasks/{id}` - Delete task by ID (user isolation enforced)

### Utility Endpoints

- `GET /` - Health check / API info
- `GET /docs` - OpenAPI/Swagger documentation (auto-generated by FastAPI)
- `GET /redoc` - ReDoc documentation (auto-generated by FastAPI)

## Database Schema Summary

### Users Table

```
users
├── id (Primary Key, UUID or Integer)
├── email (Unique, Not Null, Indexed)
├── password_hash (Not Null)
├── name (Not Null)
├── created_at (Timestamp, Default: now())
└── updated_at (Timestamp, Default: now(), Auto-update)
```

### Tasks Table

```
tasks
├── id (Primary Key, UUID or Integer)
├── title (Not Null, Max 200 chars)
├── description (Nullable, Max 2000 chars)
├── completed (Boolean, Default: false)
├── user_id (Foreign Key -> users.id, Not Null, Indexed)
├── created_at (Timestamp, Default: now())
└── updated_at (Timestamp, Default: now(), Auto-update)

Constraints:
- Foreign Key: user_id REFERENCES users(id) ON DELETE CASCADE
- Index: user_id (for efficient user-scoped queries)
```

## Quality Validation Checklist

This specification will be validated against the following checklist (to be created in `specs/002-backend-api/checklists/requirements.md`):

- [ ] All user stories have assigned priorities (P1, P2, P3)
- [ ] Each user story is independently testable
- [ ] Acceptance scenarios use Given-When-Then format
- [ ] All functional requirements are specific and measurable
- [ ] Success criteria are technology-agnostic and measurable
- [ ] Edge cases are identified and addressed
- [ ] Out of scope items are explicitly listed
- [ ] Dependencies and constraints are documented
- [ ] API endpoints are fully specified
- [ ] Database schema is defined with constraints
- [ ] Security requirements are comprehensive
- [ ] Frontend integration contract is clear
- [ ] Maximum 3 [NEEDS CLARIFICATION] markers present

## Notes

- This specification is designed to integrate seamlessly with the existing Next.js frontend (001-professional-frontend)
- All API endpoints follow RESTful conventions
- User isolation is enforced at both application and database levels
- JWT tokens follow Better Auth pattern with access/refresh token pair
- Database schema uses SQLModel for type safety and validation
- Error responses follow consistent format for frontend integration
- No pagination initially - return all user's tasks (can be added later if needed)
- Focus on security, user isolation, and frontend compatibility
