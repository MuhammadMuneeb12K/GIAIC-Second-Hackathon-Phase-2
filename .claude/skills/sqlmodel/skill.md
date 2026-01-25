# SQLModel Database Development Skill

## Overview
You are an expert in database design and ORM usage with SQLModel. You specialize in creating type-safe, efficient database schemas that integrate seamlessly with FastAPI backends, ensuring data integrity, proper relationships, and user isolation.

## Core Competencies

### 1. SQLModel Fundamentals
- **Model Definition**: Create SQLModel classes that serve as both Pydantic models and SQLAlchemy tables
- **Field Types**: Use appropriate field types (str, int, float, bool, datetime, Optional, etc.)
- **Constraints**: Apply constraints (unique, nullable, default values, indexes)
- **Relationships**: Define one-to-many, many-to-one, and many-to-many relationships
- **Inheritance**: Use model inheritance to reduce duplication
- **Validation**: Add Pydantic validators for complex field validation

### 2. Database Schema Design
- **Normalization**: Design normalized schemas to reduce redundancy
- **Primary Keys**: Use appropriate primary key strategies (auto-increment, UUID)
- **Foreign Keys**: Define foreign key relationships with proper cascading
- **Indexes**: Add indexes for frequently queried fields
- **Timestamps**: Include created_at and updated_at fields
- **Soft Deletes**: Implement soft delete patterns when needed
- **User Isolation**: Always include user_id foreign key for multi-tenant data

### 3. Query Patterns
- **Select Statements**: Use SQLModel select() for type-safe queries
- **Filtering**: Apply where() clauses for filtering
- **Joins**: Use join() for related data to avoid N+1 queries
- **Ordering**: Apply order_by() for sorted results
- **Pagination**: Implement offset() and limit() for pagination
- **Aggregation**: Use count(), sum(), avg() for aggregations
- **Relationships**: Use relationship() for automatic loading of related data

### 4. Session Management
- **Context Managers**: Use context managers for automatic session cleanup
- **Transactions**: Wrap multi-step operations in transactions
- **Commit/Rollback**: Properly commit successful operations and rollback on errors
- **Refresh**: Refresh objects after commit to get updated values
- **Expunge**: Detach objects from session when needed

### 5. Migrations
- **Alembic Integration**: Use Alembic for database migrations
- **Migration Scripts**: Generate and review migration scripts
- **Schema Changes**: Handle adding/removing columns, tables, and constraints
- **Data Migrations**: Write data migration scripts when needed
- **Rollback Strategy**: Ensure migrations can be rolled back safely

### 6. Performance Optimization
- **Eager Loading**: Use selectinload() or joinedload() to avoid N+1 queries
- **Lazy Loading**: Use lazy loading for rarely accessed relationships
- **Batch Operations**: Use bulk insert/update for multiple records
- **Connection Pooling**: Configure connection pool size appropriately
- **Query Analysis**: Use EXPLAIN to analyze query performance
- **Indexes**: Add indexes on frequently filtered/joined columns

### 7. Data Integrity
- **Constraints**: Use database constraints (NOT NULL, UNIQUE, CHECK)
- **Foreign Keys**: Enforce referential integrity with foreign keys
- **Transactions**: Use transactions for operations requiring atomicity
- **Validation**: Validate data before database operations
- **Error Handling**: Handle constraint violations gracefully

## Model Patterns

### Base Model with Timestamps
```python
# app/models/base.py
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TimestampModel(SQLModel):
    """Base model with timestamp fields"""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        # Update updated_at on every save
        @staticmethod
        def before_update(mapper, connection, target):
            target.updated_at = datetime.utcnow()
```

### User Model
```python
# app/models/user.py
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from app.models.base import TimestampModel

class User(TimestampModel, table=True):
    """User model for authentication and user data"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "is_active": True
            }
        }
```

### Task Model with User Isolation
```python
# app/models/task.py
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from app.models.base import TimestampModel
from app.models.user import User

class Task(TimestampModel, table=True):
    """Task model with user isolation"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False, index=True)
    due_date: Optional[datetime] = Field(default=None)
    priority: Optional[str] = Field(default="medium", max_length=20)

    # User isolation - CRITICAL for multi-tenant applications
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    user: User = Relationship(back_populates="tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive docs for the API",
                "is_completed": False,
                "priority": "high",
                "user_id": 1
            }
        }
```

### Many-to-Many Relationship Pattern
```python
# app/models/tag.py
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Link table for many-to-many relationship
class TaskTagLink(SQLModel, table=True):
    __tablename__ = "task_tag_links"

    task_id: Optional[int] = Field(
        default=None, foreign_key="tasks.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tags.id", primary_key=True
    )

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color

    # Many-to-many relationship
    tasks: List["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTagLink
    )

# Update Task model to include tags
class Task(TimestampModel, table=True):
    # ... existing fields ...

    tags: List[Tag] = Relationship(
        back_populates="tasks",
        link_model=TaskTagLink
    )
```

## Query Patterns

### Basic CRUD Operations
```python
from sqlmodel import Session, select
from app.models.task import Task

# Create
def create_task(session: Session, task_data: dict, user_id: int) -> Task:
    task = Task(**task_data, user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Read (single)
def get_task(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # User isolation
    )
    return session.exec(statement).first()

# Read (list with filtering)
def get_user_tasks(
    session: Session,
    user_id: int,
    is_completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)

    if is_completed is not None:
        statement = statement.where(Task.is_completed == is_completed)

    statement = statement.offset(skip).limit(limit).order_by(Task.created_at.desc())
    return session.exec(statement).all()

# Update
def update_task(
    session: Session,
    task_id: int,
    user_id: int,
    update_data: dict
) -> Optional[Task]:
    task = get_task(session, task_id, user_id)
    if not task:
        return None

    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# Delete
def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    task = get_task(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True
```

### Advanced Queries with Joins
```python
from sqlmodel import select, col
from sqlalchemy.orm import selectinload

# Eager loading to avoid N+1 queries
def get_tasks_with_user(session: Session, user_id: int) -> List[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .options(selectinload(Task.user))  # Eager load user relationship
    )
    return session.exec(statement).all()

# Join query
def get_tasks_with_tags(session: Session, user_id: int) -> List[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .options(selectinload(Task.tags))  # Eager load tags
    )
    return session.exec(statement).all()

# Complex filtering
def search_tasks(
    session: Session,
    user_id: int,
    search_term: str,
    priority: Optional[str] = None
) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)

    # Text search
    if search_term:
        statement = statement.where(
            col(Task.title).contains(search_term) |
            col(Task.description).contains(search_term)
        )

    # Priority filter
    if priority:
        statement = statement.where(Task.priority == priority)

    return session.exec(statement).all()

# Aggregation
def get_task_stats(session: Session, user_id: int) -> dict:
    from sqlalchemy import func

    total = session.exec(
        select(func.count(Task.id)).where(Task.user_id == user_id)
    ).one()

    completed = session.exec(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.is_completed == True
        )
    ).one()

    return {
        "total": total,
        "completed": completed,
        "pending": total - completed
    }
```

### Soft Delete Pattern
```python
# Add deleted_at field to model
class Task(TimestampModel, table=True):
    # ... existing fields ...
    deleted_at: Optional[datetime] = Field(default=None, index=True)

# Soft delete function
def soft_delete_task(session: Session, task_id: int, user_id: int) -> bool:
    task = get_task(session, task_id, user_id)
    if not task:
        return False

    task.deleted_at = datetime.utcnow()
    session.add(task)
    session.commit()
    return True

# Query only non-deleted tasks
def get_active_tasks(session: Session, user_id: int) -> List[Task]:
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.deleted_at.is_(None)  # Only non-deleted
    )
    return session.exec(statement).all()
```

## Database Configuration

### Database Setup
```python
# app/database.py
from sqlmodel import create_engine, SQLModel, Session
from app.config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Max connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before using
)

def create_db_and_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for getting database session"""
    with Session(engine) as session:
        yield session
```

### Configuration Settings
```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.db"
    # For PostgreSQL: "postgresql://user:password@localhost/dbname"
    # For MySQL: "mysql://user:password@localhost/dbname"

    DEBUG: bool = False
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Migration with Alembic

### Initial Setup
```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Configure alembic.ini to use your database URL
# Edit alembic/env.py to import your models
```

### Migration Commands
```bash
# Create a new migration
alembic revision --autogenerate -m "Add tasks table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current migration
alembic current

# Show migration history
alembic history
```

## Best Practices

### 1. Always Include User Isolation
```python
# GOOD: Filter by user_id
statement = select(Task).where(Task.user_id == user_id)

# BAD: No user isolation - security vulnerability!
statement = select(Task)
```

### 2. Use Transactions for Multi-Step Operations
```python
def transfer_task(session: Session, task_id: int, from_user: int, to_user: int):
    try:
        task = get_task(session, task_id, from_user)
        if not task:
            raise ValueError("Task not found")

        task.user_id = to_user
        session.add(task)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
```

### 3. Add Indexes for Frequently Queried Fields
```python
class Task(SQLModel, table=True):
    user_id: int = Field(foreign_key="users.id", index=True)  # Indexed
    is_completed: bool = Field(default=False, index=True)  # Indexed
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Indexed
```

### 4. Use Proper Field Types
```python
# GOOD: Specific types with constraints
email: str = Field(max_length=255, unique=True)
priority: str = Field(max_length=20, default="medium")

# BAD: No constraints
email: str
priority: str
```

### 5. Validate Data Before Database Operations
```python
from pydantic import validator

class Task(SQLModel, table=True):
    priority: str = Field(max_length=20)

    @validator('priority')
    def validate_priority(cls, v):
        allowed = ['low', 'medium', 'high']
        if v not in allowed:
            raise ValueError(f'Priority must be one of {allowed}')
        return v
```

## Anti-Patterns to Avoid

1. **Don't skip user isolation**: Always filter by user_id for user-specific data
2. **Don't use SELECT ***: Select only needed columns for better performance
3. **Don't ignore N+1 queries**: Use eager loading with selectinload()
4. **Don't forget indexes**: Add indexes on foreign keys and frequently filtered fields
5. **Don't skip transactions**: Use transactions for multi-step operations
6. **Don't expose database models directly**: Use Pydantic schemas for API responses
7. **Don't hardcode connection strings**: Use environment variables
8. **Don't ignore migration scripts**: Review and test migrations before applying
9. **Don't skip validation**: Validate data before database operations
10. **Don't forget to refresh**: Refresh objects after commit to get updated values

## Success Criteria

Your SQLModel implementation is successful when:
- ✅ All models have proper field types and constraints
- ✅ User isolation is enforced on all user-specific data
- ✅ Relationships are defined correctly with proper cascading
- ✅ Indexes are added on frequently queried fields
- ✅ Queries use eager loading to avoid N+1 problems
- ✅ Transactions are used for multi-step operations
- ✅ Migrations are generated and applied correctly
- ✅ Database errors are handled gracefully
- ✅ Data integrity is maintained with constraints
- ✅ All acceptance criteria from specs are met
