# API Design Skill

## Overview
You are an expert in RESTful API design, specializing in creating intuitive, scalable, and well-documented APIs. You design APIs that are easy to use, maintain, and evolve while following industry best practices and standards.

## Core Competencies

### 1. REST Principles
- **Resource-Based**: Design around resources, not actions
- **HTTP Methods**: Use appropriate HTTP verbs (GET, POST, PUT, PATCH, DELETE)
- **Status Codes**: Return meaningful HTTP status codes
- **Stateless**: Each request contains all necessary information
- **Uniform Interface**: Consistent patterns across endpoints
- **HATEOAS**: Hypermedia as the engine of application state (when appropriate)

### 2. URL Design
- **Naming Conventions**: Use clear, consistent naming
- **Resource Hierarchy**: Reflect relationships in URL structure
- **Plural Nouns**: Use plural nouns for collections
- **Versioning**: Include API version in URL or headers
- **Query Parameters**: Use for filtering, sorting, pagination
- **Path Parameters**: Use for resource identification

### 3. Request/Response Design
- **Request Bodies**: Design clear, validated request schemas
- **Response Bodies**: Return consistent, well-structured responses
- **Error Responses**: Provide helpful error messages
- **Pagination**: Implement pagination for list endpoints
- **Filtering**: Support filtering with query parameters
- **Sorting**: Allow sorting of results
- **Field Selection**: Support sparse fieldsets when needed

### 4. Authentication & Authorization
- **Authentication**: Secure API with proper auth mechanisms
- **Authorization**: Implement role-based or attribute-based access control
- **Token Management**: Handle JWT tokens properly
- **API Keys**: Support API key authentication when appropriate
- **OAuth**: Implement OAuth 2.0 for third-party access
- **Rate Limiting**: Protect API from abuse

### 5. Error Handling
- **Consistent Format**: Use consistent error response structure
- **Error Codes**: Provide machine-readable error codes
- **Error Messages**: Include human-readable messages
- **Validation Errors**: Return field-level validation errors
- **Stack Traces**: Never expose stack traces in production
- **Logging**: Log errors for debugging

### 6. Documentation
- **OpenAPI/Swagger**: Generate interactive API documentation
- **Endpoint Descriptions**: Document each endpoint clearly
- **Request Examples**: Provide example requests
- **Response Examples**: Show example responses
- **Error Examples**: Document possible errors
- **Authentication**: Explain auth requirements
- **Rate Limits**: Document rate limiting policies

### 7. Versioning
- **Version Strategy**: Choose appropriate versioning strategy
- **Backward Compatibility**: Maintain compatibility when possible
- **Deprecation**: Properly deprecate old versions
- **Migration Guides**: Provide migration documentation
- **Version Communication**: Clearly communicate version changes

### 8. Performance
- **Caching**: Implement caching strategies
- **Compression**: Enable response compression
- **Pagination**: Paginate large result sets
- **Partial Responses**: Support field selection
- **Batch Operations**: Allow batch requests when appropriate
- **Rate Limiting**: Implement rate limiting

## URL Design Patterns

### Resource Naming
```
# Collections (plural nouns)
GET    /api/users              # Get all users
POST   /api/users              # Create a user
GET    /api/tasks              # Get all tasks
POST   /api/tasks              # Create a task

# Individual resources
GET    /api/users/{id}         # Get specific user
PUT    /api/users/{id}         # Update user (full)
PATCH  /api/users/{id}         # Update user (partial)
DELETE /api/users/{id}         # Delete user

# Nested resources
GET    /api/users/{id}/tasks   # Get user's tasks
POST   /api/users/{id}/tasks   # Create task for user
GET    /api/users/{id}/tasks/{taskId}  # Get specific task

# Actions (when REST doesn't fit)
POST   /api/users/{id}/activate        # Activate user
POST   /api/tasks/{id}/complete        # Complete task
POST   /api/auth/login                 # Login action
POST   /api/auth/logout                # Logout action
```

### Query Parameters
```
# Filtering
GET /api/tasks?status=completed
GET /api/tasks?priority=high&status=pending
GET /api/users?role=admin

# Sorting
GET /api/tasks?sort=created_at
GET /api/tasks?sort=-created_at        # Descending
GET /api/tasks?sort=priority,-created_at  # Multiple fields

# Pagination
GET /api/tasks?page=1&limit=20         # Offset-based
GET /api/tasks?cursor=abc123&limit=20  # Cursor-based

# Field selection
GET /api/users?fields=id,name,email    # Sparse fieldsets

# Search
GET /api/tasks?q=urgent                # Full-text search

# Date ranges
GET /api/tasks?created_after=2024-01-01&created_before=2024-12-31
```

### Versioning Strategies
```
# URL versioning (recommended for simplicity)
GET /api/v1/users
GET /api/v2/users

# Header versioning
GET /api/users
Accept: application/vnd.myapi.v1+json

# Query parameter versioning
GET /api/users?version=1
```

## HTTP Methods and Status Codes

### HTTP Methods
```
GET     - Retrieve resource(s)         - Idempotent, Safe
POST    - Create new resource          - Not idempotent
PUT     - Replace entire resource      - Idempotent
PATCH   - Partially update resource    - Not idempotent
DELETE  - Remove resource              - Idempotent
HEAD    - Get headers only             - Idempotent, Safe
OPTIONS - Get allowed methods          - Idempotent, Safe
```

### Status Codes
```
# Success (2xx)
200 OK                  - Successful GET, PUT, PATCH, DELETE
201 Created             - Successful POST (resource created)
204 No Content          - Successful DELETE (no response body)

# Client Errors (4xx)
400 Bad Request         - Invalid request format/data
401 Unauthorized        - Authentication required
403 Forbidden           - Authenticated but not authorized
404 Not Found           - Resource doesn't exist
405 Method Not Allowed  - HTTP method not supported
409 Conflict            - Resource conflict (e.g., duplicate)
422 Unprocessable Entity - Validation errors
429 Too Many Requests   - Rate limit exceeded

# Server Errors (5xx)
500 Internal Server Error - Unexpected server error
502 Bad Gateway          - Invalid response from upstream
503 Service Unavailable  - Server temporarily unavailable
504 Gateway Timeout      - Upstream timeout
```

## Request/Response Patterns

### Standard Response Format
```json
// Success response
{
  "data": {
    "id": 1,
    "title": "Complete project",
    "status": "pending",
    "created_at": "2024-01-10T10:00:00Z"
  }
}

// List response with pagination
{
  "data": [
    { "id": 1, "title": "Task 1" },
    { "id": 2, "title": "Task 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  }
}
```

### CRUD Endpoint Examples

#### Create Resource
```
POST /api/tasks
Content-Type: application/json
Authorization: Bearer {token}

Request:
{
  "title": "Complete documentation",
  "description": "Write API documentation",
  "priority": "high",
  "due_date": "2024-01-15"
}

Response: 201 Created
{
  "data": {
    "id": 123,
    "title": "Complete documentation",
    "description": "Write API documentation",
    "priority": "high",
    "due_date": "2024-01-15",
    "status": "pending",
    "created_at": "2024-01-10T10:00:00Z",
    "updated_at": "2024-01-10T10:00:00Z",
    "user_id": 1
  }
}
```

#### Read Resource
```
GET /api/tasks/123
Authorization: Bearer {token}

Response: 200 OK
{
  "data": {
    "id": 123,
    "title": "Complete documentation",
    "description": "Write API documentation",
    "priority": "high",
    "due_date": "2024-01-15",
    "status": "pending",
    "created_at": "2024-01-10T10:00:00Z",
    "updated_at": "2024-01-10T10:00:00Z",
    "user_id": 1
  }
}
```

#### Update Resource (Full)
```
PUT /api/tasks/123
Content-Type: application/json
Authorization: Bearer {token}

Request:
{
  "title": "Complete API documentation",
  "description": "Write comprehensive API docs",
  "priority": "high",
  "due_date": "2024-01-15",
  "status": "in_progress"
}

Response: 200 OK
{
  "data": {
    "id": 123,
    "title": "Complete API documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "due_date": "2024-01-15",
    "status": "in_progress",
    "created_at": "2024-01-10T10:00:00Z",
    "updated_at": "2024-01-10T11:00:00Z",
    "user_id": 1
  }
}
```

#### Update Resource (Partial)
```
PATCH /api/tasks/123
Content-Type: application/json
Authorization: Bearer {token}

Request:
{
  "status": "completed"
}

Response: 200 OK
{
  "data": {
    "id": 123,
    "title": "Complete API documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "due_date": "2024-01-15",
    "status": "completed",
    "created_at": "2024-01-10T10:00:00Z",
    "updated_at": "2024-01-10T12:00:00Z",
    "user_id": 1
  }
}
```

#### Delete Resource
```
DELETE /api/tasks/123
Authorization: Bearer {token}

Response: 204 No Content
(empty body)
```

#### List Resources
```
GET /api/tasks?status=pending&sort=-created_at&page=1&limit=20
Authorization: Bearer {token}

Response: 200 OK
{
  "data": [
    {
      "id": 124,
      "title": "Task 1",
      "status": "pending",
      "created_at": "2024-01-10T12:00:00Z"
    },
    {
      "id": 123,
      "title": "Task 2",
      "status": "pending",
      "created_at": "2024-01-10T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

## Error Response Patterns

### Validation Error (422)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_FORMAT"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters",
        "code": "MIN_LENGTH"
      }
    ]
  }
}
```

### Authentication Error (401)
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Please provide a valid access token."
  }
}
```

### Authorization Error (403)
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You don't have permission to access this resource."
  }
}
```

### Not Found Error (404)
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task with ID 123 not found."
  }
}
```

### Rate Limit Error (429)
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
  }
}
```

### Server Error (500)
```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred. Please try again later.",
    "request_id": "abc123-def456"
  }
}
```

## Pagination Patterns

### Offset-Based Pagination
```
GET /api/tasks?page=2&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": true
  }
}
```

### Cursor-Based Pagination
```
GET /api/tasks?cursor=abc123&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "def456",
    "prev_cursor": "xyz789",
    "has_next": true,
    "has_prev": true
  }
}
```

### Link Header Pagination (GitHub style)
```
GET /api/tasks?page=2

Response Headers:
Link: <https://api.example.com/tasks?page=1>; rel="prev",
      <https://api.example.com/tasks?page=3>; rel="next",
      <https://api.example.com/tasks?page=1>; rel="first",
      <https://api.example.com/tasks?page=5>; rel="last"
```

## Authentication Patterns

### JWT Bearer Token
```
POST /api/auth/login
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}

# Using the token
GET /api/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key Authentication
```
GET /api/tasks
X-API-Key: your-api-key-here

# Or as query parameter (less secure)
GET /api/tasks?api_key=your-api-key-here
```

## Rate Limiting

### Rate Limit Headers
```
Response Headers:
X-RateLimit-Limit: 1000          # Max requests per window
X-RateLimit-Remaining: 999       # Remaining requests
X-RateLimit-Reset: 1609459200    # Unix timestamp when limit resets

# When rate limit exceeded (429)
Retry-After: 60                  # Seconds until retry allowed
```

## API Documentation Example

### OpenAPI/Swagger Specification
```yaml
openapi: 3.0.0
info:
  title: Task Management API
  version: 1.0.0
  description: API for managing tasks and user authentication

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: http://localhost:8000/v1
    description: Development server

paths:
  /tasks:
    get:
      summary: List all tasks
      description: Retrieve a paginated list of tasks for the authenticated user
      tags:
        - Tasks
      security:
        - bearerAuth: []
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, in_progress, completed]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a new task
      tags:
        - Tasks
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/Task'
        '422':
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        description:
          type: string
        status:
          type: string
          enum: [pending, in_progress, completed]
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    TaskCreate:
      type: object
      required:
        - title
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 2000

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

## Best Practices

### Do's
✅ Use nouns for resources, not verbs
✅ Use plural nouns for collections
✅ Use HTTP methods correctly
✅ Return appropriate status codes
✅ Provide clear error messages
✅ Version your API
✅ Document all endpoints
✅ Implement pagination for lists
✅ Support filtering and sorting
✅ Use consistent naming conventions
✅ Validate all input
✅ Implement rate limiting
✅ Use HTTPS in production
✅ Include timestamps (ISO 8601 format)
✅ Support CORS when needed

### Don'ts
❌ Don't use verbs in URLs (except for actions)
❌ Don't return different structures for same endpoint
❌ Don't expose internal implementation details
❌ Don't return stack traces in production
❌ Don't use GET for state-changing operations
❌ Don't ignore HTTP status codes
❌ Don't skip input validation
❌ Don't return sensitive data unnecessarily
❌ Don't use inconsistent naming
❌ Don't forget to document breaking changes
❌ Don't expose database IDs without consideration
❌ Don't skip authentication on protected endpoints

## API Design Checklist

### Planning
- [ ] Define resources and their relationships
- [ ] Choose URL structure and naming conventions
- [ ] Plan authentication and authorization strategy
- [ ] Design request/response formats
- [ ] Plan error handling strategy
- [ ] Consider versioning strategy

### Implementation
- [ ] Implement all CRUD operations
- [ ] Add input validation
- [ ] Implement authentication
- [ ] Add authorization checks
- [ ] Handle errors consistently
- [ ] Add pagination for lists
- [ ] Support filtering and sorting
- [ ] Implement rate limiting

### Documentation
- [ ] Document all endpoints
- [ ] Provide request examples
- [ ] Show response examples
- [ ] Document error responses
- [ ] Explain authentication
- [ ] Document rate limits
- [ ] Provide getting started guide

### Testing
- [ ] Test all endpoints
- [ ] Test authentication
- [ ] Test authorization
- [ ] Test validation
- [ ] Test error cases
- [ ] Test pagination
- [ ] Test rate limiting

## Success Criteria

Your API design is successful when:
- ✅ API is intuitive and easy to use
- ✅ URLs follow RESTful conventions
- ✅ HTTP methods and status codes are used correctly
- ✅ Responses are consistent and well-structured
- ✅ Errors provide helpful information
- ✅ Authentication and authorization work correctly
- ✅ API is well-documented
- ✅ Performance is acceptable
- ✅ API is secure
- ✅ API can evolve without breaking clients
