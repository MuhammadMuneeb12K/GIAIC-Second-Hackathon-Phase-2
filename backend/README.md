# Backend API - Multi-User Todo Application

FastAPI backend for a secure, multi-user todo application with JWT authentication and user isolation.

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Task Management**: Full CRUD operations for tasks with user isolation
- **Security**: Password hashing with bcrypt, JWT token validation, user data isolation
- **Database**: PostgreSQL with SQLModel ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT with Better Auth pattern
- **Password Hashing**: bcrypt (cost factor 12)

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database (Neon recommended)
- pip or poetry for dependency management

### Installation

1. **Clone the repository** (if not already done)

2. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

   Required environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Secret key for JWT (minimum 32 characters)
   - `FRONTEND_URL`: Frontend origin for CORS
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration (default: 15)
   - `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration (default: 7)

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Authenticate user and issue tokens
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/signout` - Sign out user

### Task Endpoints (Protected)

- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get single task by ID
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete task

## Project Structure

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
│   │   ├── auth.py          # Auth schemas
│   │   └── task.py          # Task schemas
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection
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
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md                # This file
```

## Security Features

- **Password Hashing**: bcrypt with cost factor 12
- **JWT Tokens**: HS256 algorithm with configurable expiration
- **User Isolation**: All task operations enforce user ownership
- **Input Validation**: Comprehensive validation with Pydantic
- **CORS**: Configurable CORS for frontend integration
- **Error Handling**: Consistent error responses without sensitive data exposure

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Deployment

1. Set environment variables in production environment
2. Use production-grade ASGI server (uvicorn with workers)
3. Enable HTTPS at reverse proxy/load balancer level
4. Configure database connection pooling
5. Set up monitoring and logging

## License

[Your License Here]

## Support

For issues and questions, please refer to the project documentation in `/specs/002-backend-api/`.
