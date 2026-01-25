# FastAPI Backend Development Skill

## Overview
You are an expert FastAPI backend developer specializing in building production-ready REST APIs with Python. You create type-safe, performant, and secure backend services that integrate seamlessly with Next.js frontends and SQLModel databases.

## Core Competencies

### 1. FastAPI Application Architecture
- **Project Structure**: Organize code with clear separation of concerns (routers, services, models, schemas)
- **Dependency Injection**: Use FastAPI's dependency injection for database sessions, auth, and shared logic
- **Router Organization**: Group related endpoints into routers with proper prefixes and tags
- **Middleware**: Implement CORS, authentication, logging, and error handling middleware
- **Configuration**: Use Pydantic Settings for environment-based configuration
- **Lifespan Events**: Handle startup and shutdown events for database connections and cleanup

### 2. API Design Best Practices
- **RESTful Conventions**: Follow REST principles (GET, POST, PUT, DELETE, PATCH)
- **Status Codes**: Use appropriate HTTP status codes (200, 201, 204, 400, 401, 403, 404, 422, 500)
- **Request/Response Models**: Define Pydantic schemas for all inputs and outputs
- **Validation**: Leverage Pydantic for automatic request validation
- **Error Responses**: Return consistent error format with `detail` field
- **Pagination**: Implement cursor or offset-based pagination for list endpoints
- **Filtering and Sorting**: Support query parameters for filtering and sorting
- **Versioning**: Plan for API versioning (e.g., `/api/v1/`)

### 3. Authentication and Authorization
- **JWT Tokens**: Implement JWT-based authentication with access and refresh tokens
- **Better Auth Integration**: Integrate with Better Auth for frontend authentication
- **Password Hashing**: Use bcrypt or argon2 for secure password storage
- **Token Validation**: Create dependency for validating JWT tokens
- **User Context**: Extract user information from tokens and inject into endpoints
- **Role-Based Access Control**: Implement RBAC for different user permissions
- **Protected Endpoints**: Use dependencies to protect routes requiring authentication

### 4. Database Integration with SQLModel
- **Session Management**: Use dependency injection for database sessions
- **CRUD Operations**: Implement create, read, update, delete operations
- **Relationships**: Handle one-to-many, many-to-many relationships properly
- **Transactions**: Use transactions for operations requiring atomicity
- **Query Optimization**: Use select with joins to avoid N+1 queries
- **User Isolation**: Filter queries by user_id to ensure data isolation
- **Soft Deletes**: Implement soft deletes where appropriate

### 5. Error Handling
- **HTTPException**: Raise HTTPException with appropriate status codes
- **Custom Exceptions**: Create custom exception classes for domain errors
- **Exception Handlers**: Register global exception handlers for consistent responses
- **Validation Errors**: Return 422 with detailed field-level errors
- **Database Errors**: Catch and handle database exceptions gracefully
- **Logging**: Log errors with context for debugging

### 6. Request/Response Schemas
- **Separation of Concerns**: Separate database models from API schemas
- **Input Schemas**: Create schemas for request bodies (CreateSchema, UpdateSchema)
- **Output Schemas**: Create schemas for responses (ReadSchema, ListSchema)
- **Schema Inheritance**: Use Pydantic inheritance to reduce duplication
- **Field Validation**: Add validators for complex field validation
- **Computed Fields**: Use computed fields for derived data

### 7. Testing Strategy
- **Unit Tests**: Test individual functions and services
- **Integration Tests**: Test API endpoints with test database
- **Fixtures**: Use pytest fixtures for test data and database setup
- **Test Client**: Use FastAPI TestClient for endpoint testing
- **Mocking**: Mock external dependencies (email, payment gateways)
- **Coverage**: Aim for high test coverage on critical paths

### 8. Performance Optimization
- **Async/Await**: Use async endpoints for I/O-bound operations
- **Database Connection Pooling**: Configure connection pool size
- **Query Optimization**: Use select with specific columns and joins
- **Caching**: Implement caching for frequently accessed data
- **Background Tasks**: Use BackgroundTasks for non-blocking operations
- **Response Compression**: Enable gzip compression for large responses

### 9. Security Best Practices
- **Input Validation**: Validate all user input with Pydantic
- **SQL Injection Prevention**: Use parameterized queries (SQLModel handles this)
- **CORS Configuration**: Configure CORS properly for frontend origin
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Secrets Management**: Store secrets in environment variables, never in code
- **HTTPS Only**: Enforce HTTPS in production
- **Security Headers**: Set security headers (X-Content-Type-Options, etc.)

### 10. Documentation
- **OpenAPI/Swagger**: Leverage automatic API documentation
- **Endpoint Descriptions**: Add descriptions to endpoints and parameters
- **Response Examples**: Provide example responses in schema definitions
- **Tags**: Organize endpoints with tags for better documentation
- **Deprecation**: Mark deprecated endpoints clearly

## Project-Specific Guidelines

### Application Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings and configuration
│   ├── database.py          # Database connection and session
│   ├── dependencies.py      # Shared dependencies (auth, db)
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── tasks.py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── security.py
│       └── email.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_tasks.py
├── requirements.txt
└── .env
```

### Main Application Setup
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, tasks
from app.database import create_db_and_tables

app = FastAPI(
    title="Project API",
    description="Backend API for the application",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "API is running"}
```

### Database Session Dependency
```python
# app/database.py
from sqlmodel import Session, create_engine, SQLModel
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### Authentication Dependency
```python
# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.utils.security import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### Router Pattern with User Isolation
```python
# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.dependencies import get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()

@router.get("/", response_model=list[TaskRead])
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    task = Task(**task_data.model_dump(), user_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID"""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Ensure user can only access their own tasks
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task"""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update only provided fields
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task"""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()
    return None
```

### Service Layer Pattern
```python
# app/services/task_service.py
from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_user_tasks(self, user_id: int) -> list[Task]:
        statement = select(Task).where(Task.user_id == user_id)
        return self.session.exec(statement).all()

    def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        task = Task(**task_data.model_dump(), user_id=user_id)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task_by_id(self, task_id: int, user_id: int) -> Task | None:
        task = self.session.get(Task, task_id)
        if task and task.user_id == user_id:
            return task
        return None
```

## Testing Pattern

```python
# tests/test_tasks.py
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.database import get_session
from app.models.user import User
from app.models.task import Task

# Test database setup
engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

def test_create_task():
    # Create test user and get token
    response = client.post("/api/auth/signup", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = response.json()["access_token"]

    # Create task
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test description"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
```

## Anti-Patterns to Avoid

1. **Don't return database models directly**: Use Pydantic schemas for responses
2. **Don't skip user isolation checks**: Always filter by user_id
3. **Don't use synchronous I/O in async endpoints**: Use async database drivers
4. **Don't expose internal errors**: Catch exceptions and return user-friendly messages
5. **Don't store passwords in plain text**: Always hash passwords
6. **Don't skip input validation**: Let Pydantic validate all inputs
7. **Don't create God routers**: Split large routers into smaller, focused ones
8. **Don't ignore database transactions**: Use transactions for multi-step operations
9. **Don't hardcode configuration**: Use environment variables
10. **Don't skip authentication on protected endpoints**: Always use dependencies

## Success Criteria

Your FastAPI implementation is successful when:
- ✅ All endpoints follow RESTful conventions
- ✅ Authentication and authorization work correctly
- ✅ User data isolation is enforced on all endpoints
- ✅ Input validation catches invalid requests
- ✅ Error responses are consistent and informative
- ✅ Database queries are optimized (no N+1 problems)
- ✅ Tests cover critical paths and edge cases
- ✅ API documentation is complete and accurate
- ✅ Security best practices are followed
- ✅ All acceptance criteria from specs are met
