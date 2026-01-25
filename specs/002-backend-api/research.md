# Research & Technology Decisions: Backend API

**Feature**: Backend API for Multi-User Todo Application
**Branch**: 002-backend-api
**Date**: 2026-01-11
**Phase**: Phase 0 - Research & Decision Documentation

## Purpose

This document captures all technology decisions, best practices research, and architectural choices made during the planning phase. All decisions are derived from the approved specification and constitution requirements.

---

## Technology Stack Decisions

### 1. Backend Framework: FastAPI

**Decision**: Use FastAPI as the backend web framework

**Rationale**:
- **Specification Requirement**: Explicitly required in spec.md (Technical Constraints section)
- **Constitution Compliance**: Listed as required technology in constitution.md Section IV
- **Performance**: FastAPI is one of the fastest Python frameworks, meeting NFR-009 and NFR-010 performance requirements
- **Type Safety**: Built-in Pydantic validation aligns with NFR-019 requirement for typed endpoints
- **Auto-Documentation**: Automatic OpenAPI/Swagger generation satisfies SC-009 and NFR-019
- **Async Support**: Native async/await support for database operations and concurrent requests (NFR-012)

**Alternatives Considered**:
- Django REST Framework: Rejected - heavier framework, slower performance, not specified in requirements
- Flask: Rejected - lacks built-in validation and auto-documentation, not specified in requirements

**Best Practices**:
- Use APIRouter for endpoint organization by domain (auth, tasks)
- Implement dependency injection for database sessions and authentication
- Use Pydantic models for all request/response validation
- Enable CORS middleware for frontend integration
- Configure exception handlers for consistent error responses

---

### 2. ORM: SQLModel

**Decision**: Use SQLModel for database operations

**Rationale**:
- **Specification Requirement**: Explicitly required in spec.md (Technical Constraints section)
- **Constitution Compliance**: Listed as required technology in constitution.md Section IV
- **Type Safety**: Combines SQLAlchemy and Pydantic for type-safe database operations (NFR-020)
- **FastAPI Integration**: Seamless integration with FastAPI's Pydantic validation
- **Simplicity**: Single model definition for both database schema and API validation
- **PostgreSQL Support**: Full PostgreSQL feature support including constraints and indexes

**Alternatives Considered**:
- Raw SQLAlchemy: Rejected - requires separate Pydantic models, more boilerplate
- Django ORM: Rejected - tied to Django framework, not compatible with FastAPI
- Tortoise ORM: Rejected - not specified in requirements, less mature ecosystem

**Best Practices**:
- Define models with proper type hints for all fields
- Use Field() for constraints (max_length, default values)
- Implement relationships using Relationship() for foreign keys
- Add indexes using index=True on frequently queried fields (user_id, email)
- Use Optional[] for nullable fields
- Implement created_at and updated_at with default factories

---

### 3. Database: Neon PostgreSQL

**Decision**: Use Neon Serverless PostgreSQL as the database

**Rationale**:
- **Specification Requirement**: Explicitly required in spec.md (Technical Constraints section)
- **Constitution Compliance**: Listed as required technology in constitution.md Section IV
- **Serverless**: Auto-scaling and connection pooling handled by Neon (NFR-013)
- **PostgreSQL Compatibility**: Full PostgreSQL feature set including constraints, indexes, and CASCADE deletes
- **Performance**: Low-latency connections suitable for NFR-009 and NFR-010 requirements
- **Cost-Effective**: Pay-per-use model suitable for hackathon project

**Alternatives Considered**:
- Self-hosted PostgreSQL: Rejected - requires infrastructure management, not specified
- MySQL: Rejected - not specified, different SQL dialect
- MongoDB: Rejected - NoSQL not suitable for relational data model with foreign keys

**Best Practices**:
- Use connection pooling via SQLModel engine configuration
- Store DATABASE_URL in environment variables (NFR-008)
- Use async database driver (asyncpg) for better performance
- Implement proper connection error handling (NFR-014)
- Use database transactions for multi-record operations (NFR-017)

---

### 4. Authentication: JWT with Better Auth Pattern

**Decision**: Use JWT tokens following Better Auth pattern

**Rationale**:
- **Specification Requirement**: Explicitly required in spec.md (Technical Constraints section)
- **Constitution Compliance**: Section V mandates JWT verification with Better Auth
- **Stateless**: No server-side session storage required (Architecture Constraints)
- **Frontend Compatibility**: Matches existing Next.js frontend implementation (001-professional-frontend)
- **Security**: Industry-standard token-based authentication with expiration
- **Scalability**: Stateless tokens enable horizontal scaling

**Alternatives Considered**:
- Session-based auth: Rejected - explicitly prohibited in Architecture Constraints
- OAuth2: Rejected - out of scope per specification
- API Keys: Rejected - less secure, no expiration mechanism

**Best Practices**:
- Use HS256 algorithm for JWT signing (NFR-002)
- Store BETTER_AUTH_SECRET in environment variables (NFR-003, minimum 32 characters)
- Set access token expiration to 15 minutes (FR-009)
- Set refresh token expiration to 7 days (FR-010)
- Include user_id and exp claims in JWT payload (FR-007)
- Validate JWT signature and expiration on all protected endpoints (FR-013)
- Extract user_id from validated JWT for user isolation (FR-014)

**JWT Library**: python-jose[cryptography]
- Industry-standard JWT implementation for Python
- Supports HS256 algorithm
- Provides encode/decode with signature verification
- Compatible with FastAPI dependency injection

---

### 5. Password Hashing: bcrypt

**Decision**: Use bcrypt for password hashing

**Rationale**:
- **Specification Requirement**: FR-004 requires bcrypt or argon2
- **Security**: Industry-standard password hashing with configurable cost factor
- **NFR Compliance**: NFR-001 requires minimum cost factor of 12
- **Library Support**: passlib[bcrypt] provides excellent Python integration
- **Performance**: Suitable for authentication endpoint performance requirements (NFR-009)

**Alternatives Considered**:
- argon2: Also acceptable per spec, but bcrypt is more widely adopted and tested
- PBKDF2: Rejected - less secure than bcrypt for password hashing
- Plain SHA256: Rejected - not suitable for password hashing (no salt, too fast)

**Best Practices**:
- Use passlib.context.CryptContext for password hashing
- Set bcrypt rounds to 12 (cost factor) per NFR-001
- Never log or expose password hashes
- Hash passwords before storing in database (FR-004)
- Use constant-time comparison for password verification

---

### 6. Environment Management: Pydantic Settings

**Decision**: Use Pydantic Settings for environment variable management

**Rationale**:
- **Specification Requirement**: Listed in Python Dependencies section
- **NFR Compliance**: NFR-021 requires Pydantic Settings for validation
- **Type Safety**: Validates environment variables at startup (SC-014)
- **FastAPI Integration**: Native integration with FastAPI
- **Error Handling**: Clear error messages for missing or invalid environment variables

**Alternatives Considered**:
- python-dotenv only: Rejected - lacks validation, type conversion, and error handling
- os.environ: Rejected - no validation or type safety

**Best Practices**:
- Create Settings class inheriting from BaseSettings
- Define all required environment variables with type hints
- Use Field() for validation rules (min_length for secrets)
- Load .env file automatically in development
- Validate settings at application startup
- Use dependency injection to access settings in endpoints

**Required Environment Variables**:
- DATABASE_URL: Neon PostgreSQL connection string
- BETTER_AUTH_SECRET: JWT signing secret (minimum 32 characters)
- FRONTEND_URL: Frontend origin for CORS
- ACCESS_TOKEN_EXPIRE_MINUTES: Access token expiration (default: 15)
- REFRESH_TOKEN_EXPIRE_DAYS: Refresh token expiration (default: 7)

---

## Architecture Decisions

### 1. Project Structure: Monorepo with backend/ Directory

**Decision**: Place all backend code in backend/ directory at repository root

**Rationale**:
- **Constitution Requirement**: Section VIII mandates monorepo structure
- **Specification Requirement**: Architecture Constraints specify backend/ directory
- **Separation of Concerns**: Clear separation between frontend and backend code
- **Shared Specs**: Both frontend and backend reference same specifications

**Directory Structure**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Pydantic Settings configuration
│   ├── database.py          # Database connection and session management
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth request/response schemas
│   │   └── task.py          # Task request/response schemas
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection (auth, db session)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py      # Authentication endpoints
│   │       └── tasks.py     # Task CRUD endpoints
│   ├── core/                # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py      # Password hashing, JWT utilities
│   │   └── exceptions.py    # Custom exception classes
│   └── services/            # Business logic layer
│       ├── __init__.py
│       ├── auth_service.py  # Authentication business logic
│       └── task_service.py  # Task business logic
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Authentication tests
│   └── test_tasks.py        # Task CRUD tests
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md                # Backend documentation
```

---

### 2. API Prefix: /api

**Decision**: All endpoints must be under /api prefix

**Rationale**:
- **Specification Requirement**: Architecture Constraints mandate /api prefix
- **Frontend Compatibility**: Matches frontend API client configuration
- **Versioning Readiness**: Allows future versioning (e.g., /api/v2) if needed
- **Clear Separation**: Distinguishes API endpoints from static files or documentation

**Implementation**:
- Configure FastAPI app with prefix="/api"
- All routes automatically prefixed: /api/auth/signup, /api/tasks, etc.
- Root endpoint (/) remains at root for health checks
- Documentation endpoints (/docs, /redoc) remain at root

---

### 3. User Isolation Strategy

**Decision**: Enforce user isolation at both application and database levels

**Rationale**:
- **Constitution Requirement**: Section V mandates user isolation enforcement
- **Specification Requirement**: FR-023 requires user isolation on all task operations
- **Security**: Defense in depth - multiple layers of protection
- **Data Integrity**: Prevents accidental cross-user data access

**Application-Level Isolation**:
- Extract user_id from validated JWT token (FR-014)
- Add user_id filter to all database queries
- Return 404 for tasks owned by different users (FR-019)
- Never accept user_id from request body or URL parameters

**Database-Level Isolation**:
- Foreign key constraint: tasks.user_id REFERENCES users.id
- Index on user_id for query performance (NFR-011)
- CASCADE delete: when user deleted, all tasks deleted automatically

**Implementation Pattern**:
```python
# Get current user from JWT
current_user = get_current_user(token)

# Query with user isolation
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == current_user.id  # User isolation enforced
).first()

if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

---

### 4. Error Response Format

**Decision**: Use consistent error response format with "detail" field

**Rationale**:
- **Specification Requirement**: FR-035 requires consistent error format with "detail" field
- **Frontend Compatibility**: NFR-027 requires error format matching frontend expectations
- **FastAPI Default**: Matches FastAPI's default HTTPException format
- **User Experience**: Clear, actionable error messages

**Error Response Structure**:
```json
{
  "detail": "Error message here"
}
```

**HTTP Status Codes**:
- 400 Bad Request: Malformed JSON or invalid request format (FR-033)
- 401 Unauthorized: Missing or invalid JWT token (FR-030)
- 404 Not Found: Resource not found or unauthorized access (FR-031)
- 409 Conflict: Duplicate email registration (FR-032)
- 422 Unprocessable Entity: Validation errors (FR-029)
- 500 Internal Server Error: Unexpected server errors (FR-034)

**Security Consideration**:
- Never expose sensitive information in error messages (NFR-007, SC-018)
- Use generic messages for authentication failures (security best practice)
- Log detailed errors server-side for debugging (NFR-015)

---

### 5. CORS Configuration

**Decision**: Enable CORS for frontend origin specified in environment variable

**Rationale**:
- **Specification Requirement**: FR-039 requires CORS for frontend origin
- **Frontend Integration**: Allows Next.js frontend to make API requests
- **Security**: Restrict CORS to specific frontend origin, not wildcard
- **Flexibility**: Configurable via FRONTEND_URL environment variable

**CORS Configuration**:
- Allow origin: Value from FRONTEND_URL environment variable
- Allow credentials: True (for JWT tokens in Authorization header)
- Allow methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
- Allow headers: Authorization, Content-Type

---

## Security Best Practices

### 1. JWT Security

**Practices**:
- Use HS256 algorithm (symmetric signing) per NFR-002
- Store secret in environment variable (NFR-003)
- Minimum secret length: 32 characters (NFR-003)
- Set appropriate expiration times (15 min access, 7 day refresh)
- Validate signature and expiration on every request (FR-013)
- Never log or expose JWT secrets

### 2. Password Security

**Practices**:
- Hash passwords with bcrypt cost factor 12 (NFR-001)
- Never log or expose password hashes
- Use constant-time comparison for password verification
- Enforce minimum password length of 8 characters (FR-003)
- Return generic error messages for failed authentication (security best practice)

### 3. Input Validation

**Practices**:
- Validate all request bodies with Pydantic models (FR-036)
- Sanitize user input to prevent SQL injection (NFR-004)
- Validate email format with regex (FR-002)
- Enforce maximum lengths (title: 200, description: 2000) (FR-024, FR-025)
- Use Pydantic Field() validators for constraints

### 4. Rate Limiting

**Practices**:
- Implement rate limiting on authentication endpoints (NFR-005)
- Prevent brute force attacks on signup/signin
- Use slowapi or similar library for rate limiting
- Configure appropriate limits (e.g., 5 requests per minute for auth endpoints)

---

## Performance Optimization

### 1. Database Indexing

**Strategy**:
- Index on users.email for login queries (NFR-011)
- Index on tasks.user_id for user-scoped queries (NFR-011)
- Composite index on (user_id, created_at) if sorting by date

**Expected Performance**:
- Task retrieval: <100ms for users with up to 1000 tasks (SC-007)
- Authentication: <500ms under normal load (NFR-009)
- Task CRUD: <200ms under normal load (NFR-010)

### 2. Connection Pooling

**Strategy**:
- Configure SQLModel engine with connection pool (NFR-013)
- Set appropriate pool size based on expected concurrency
- Use async database driver (asyncpg) for better performance
- Handle connection errors gracefully (NFR-014)

### 3. Async Operations

**Strategy**:
- Use async/await for all database operations
- Use async FastAPI endpoints for I/O-bound operations
- Leverage FastAPI's async capabilities for concurrent requests (NFR-012)

---

## Testing Strategy

### 1. Unit Tests

**Scope**:
- Password hashing and verification
- JWT token generation and validation
- Input validation with Pydantic models
- Business logic in service layer

### 2. Integration Tests

**Scope**:
- API endpoint functionality
- Database operations with test database
- Authentication flow (signup, signin, token validation)
- User isolation enforcement
- Error handling and status codes

### 3. Security Tests

**Scope**:
- JWT validation (expired tokens, invalid signatures)
- User isolation (cross-user access attempts)
- Password security (hashing, verification)
- Input validation (SQL injection attempts, XSS)

---

## Deployment Considerations

### 1. Environment Variables

**Production Requirements**:
- DATABASE_URL: Neon PostgreSQL connection string
- BETTER_AUTH_SECRET: Strong random secret (minimum 32 characters)
- FRONTEND_URL: Production frontend URL for CORS
- ACCESS_TOKEN_EXPIRE_MINUTES: 15 (default)
- REFRESH_TOKEN_EXPIRE_DAYS: 7 (default)

### 2. HTTPS

**Requirement**:
- NFR-006 requires HTTPS in production
- Enforced at deployment level (reverse proxy, load balancer)
- Not handled by FastAPI application directly

### 3. Logging

**Strategy**:
- Log all errors with context (NFR-015)
- Use structured logging (JSON format)
- Never log sensitive information (passwords, tokens, secrets)
- Log authentication attempts for security monitoring

---

## Risks and Mitigations

### Risk 1: Database Connection Failures

**Mitigation**:
- Implement proper error handling (NFR-014)
- Return 503 Service Unavailable status
- Log errors for monitoring
- Configure connection retry logic

### Risk 2: JWT Token Expiration During Request

**Mitigation**:
- Validate token at request start
- Return 401 if expired
- Frontend handles token refresh automatically

### Risk 3: Concurrent Task Updates

**Mitigation**:
- Use database-level constraints
- Implement optimistic locking if needed
- Return appropriate conflict errors

### Risk 4: Brute Force Attacks

**Mitigation**:
- Implement rate limiting on auth endpoints (NFR-005)
- Use generic error messages for failed authentication
- Monitor failed authentication attempts

---

## Summary

All technology decisions are derived from approved specifications and constitution requirements. No assumptions or shortcuts have been made. The chosen technologies (FastAPI, SQLModel, Neon PostgreSQL, JWT, bcrypt) are explicitly required and provide the necessary features for security, performance, and frontend integration.

The architecture follows monorepo structure with clear separation of concerns. User isolation is enforced at both application and database levels. Security best practices are documented and will be implemented according to NFR requirements.

This research document resolves all technology choices and provides clear guidance for implementation planning in subsequent phases.
