# Data Model: Backend API

**Feature**: Backend API for Multi-User Todo Application
**Branch**: 002-backend-api
**Date**: 2026-01-11
**Phase**: Phase 1 - Data Model Design

## Purpose

This document defines the data model for the backend API, including all entities, their attributes, relationships, constraints, and validation rules. This model is derived directly from the approved specification (spec.md).

---

## Entity Overview

The system has two primary entities:

1. **User** - Represents a registered user account with authentication credentials
2. **Task** - Represents a todo item owned by a specific user

**Relationship**: One User has many Tasks (one-to-many)

---

## Entity: User

### Description

Represents a registered user account in the system. Users can create accounts, authenticate, and manage their personal todo lists. Each user is isolated from other users' data.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer or UUID | Primary Key, Auto-increment/Generated | Unique identifier for the user |
| `email` | String | Unique, Not Null, Indexed, Max 255 chars | User's email address (used for login) |
| `password_hash` | String | Not Null, Max 255 chars | Bcrypt-hashed password (never store plain text) |
| `name` | String | Not Null, Max 100 chars | User's display name |
| `created_at` | DateTime | Not Null, Default: now() | Timestamp when user account was created |
| `updated_at` | DateTime | Not Null, Default: now(), Auto-update | Timestamp when user account was last updated |

### Validation Rules

**Email** (FR-002):
- Must match standard email regex pattern
- Format: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Must be unique across all users (FR-005)
- Case-insensitive uniqueness check recommended

**Password** (FR-003, FR-004):
- Minimum length: 8 characters (enforced before hashing)
- Must be hashed using bcrypt with cost factor 12 (NFR-001)
- Never store or log plain text passwords

**Name**:
- Required field (Not Null)
- Maximum length: 100 characters
- Minimum length: 1 character (not empty)

### Indexes

- **Primary Index**: `id` (automatic with Primary Key)
- **Unique Index**: `email` (for uniqueness constraint and login queries)

**Rationale**: Email index is critical for login performance (NFR-009 requires <500ms auth response time)

### Relationships

**Outgoing**:
- `tasks` → One-to-Many relationship with Task entity
- When user is deleted, all associated tasks are CASCADE deleted

**Incoming**: None

### Database Constraints

```sql
-- Unique constraint on email
CONSTRAINT unique_email UNIQUE (email)

-- Not null constraints
CONSTRAINT user_email_not_null CHECK (email IS NOT NULL)
CONSTRAINT user_password_hash_not_null CHECK (password_hash IS NOT NULL)
CONSTRAINT user_name_not_null CHECK (name IS NOT NULL)
```

### SQLModel Implementation Notes

```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
```

### Security Considerations

- **Password Hash**: Never expose password_hash in API responses (FR-040)
- **Email Privacy**: Consider email privacy in public-facing features (not applicable for this MVP)
- **User Isolation**: User ID extracted from JWT, never from request body (FR-014)

---

## Entity: Task

### Description

Represents a todo item owned by a specific user. Tasks have a title, optional description, completion status, and are strictly isolated to their owner. Users can only access their own tasks.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer or UUID | Primary Key, Auto-increment/Generated | Unique identifier for the task |
| `title` | String | Not Null, Max 200 chars | Task title (required) |
| `description` | String | Nullable, Max 2000 chars | Optional task description |
| `completed` | Boolean | Not Null, Default: false | Task completion status |
| `user_id` | Integer or UUID | Foreign Key, Not Null, Indexed | Owner of the task (references users.id) |
| `created_at` | DateTime | Not Null, Default: now() | Timestamp when task was created |
| `updated_at` | DateTime | Not Null, Default: now(), Auto-update | Timestamp when task was last updated |

### Validation Rules

**Title** (FR-024):
- Required field (Not Null)
- Minimum length: 1 character (not empty)
- Maximum length: 200 characters
- Trimmed of leading/trailing whitespace

**Description** (FR-025):
- Optional field (Nullable)
- Maximum length: 2000 characters if provided
- Trimmed of leading/trailing whitespace

**Completed** (FR-026):
- Boolean field
- Default value: false (new tasks are incomplete)
- Cannot be null

**User ID** (FR-016, FR-023):
- Required field (Not Null)
- Must reference a valid user in users table
- Automatically set from authenticated user's JWT token
- Never accepted from request body (security requirement)

### Indexes

- **Primary Index**: `id` (automatic with Primary Key)
- **Foreign Key Index**: `user_id` (critical for user-scoped queries)

**Rationale**: user_id index is critical for performance (NFR-011, SC-007 requires <100ms query time for 1000 tasks)

### Relationships

**Outgoing**: None

**Incoming**:
- `user` → Many-to-One relationship with User entity
- Task belongs to exactly one user

### Database Constraints

```sql
-- Foreign key constraint with CASCADE delete
CONSTRAINT fk_task_user FOREIGN KEY (user_id)
    REFERENCES users(id) ON DELETE CASCADE

-- Not null constraints
CONSTRAINT task_title_not_null CHECK (title IS NOT NULL)
CONSTRAINT task_user_id_not_null CHECK (user_id IS NOT NULL)
CONSTRAINT task_completed_not_null CHECK (completed IS NOT NULL)

-- Length constraints (enforced at application level via Pydantic)
-- title: max 200 characters
-- description: max 2000 characters
```

### SQLModel Implementation Notes

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="tasks")
```

### User Isolation Enforcement

**Application Level** (FR-023):
- All queries MUST filter by `user_id = current_user.id`
- Never accept user_id from request body or URL parameters
- Return 404 for tasks owned by different users (FR-019)

**Database Level**:
- Foreign key constraint ensures referential integrity
- CASCADE delete ensures orphaned tasks are removed
- Index on user_id enables efficient user-scoped queries

**Query Pattern**:
```python
# Correct: User isolation enforced
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == current_user.id
).first()

# Incorrect: No user isolation (NEVER DO THIS)
task = db.query(Task).filter(Task.id == task_id).first()
```

### Security Considerations

- **User Isolation**: Critical security requirement (Constitution Section V)
- **Input Validation**: Prevent XSS via title/description validation (NFR-004)
- **SQL Injection**: SQLModel/SQLAlchemy provides parameterized queries (NFR-004)

---

## Entity Relationships Diagram

```
┌─────────────────────────────────────┐
│ User                                │
├─────────────────────────────────────┤
│ id (PK)                             │
│ email (UNIQUE, INDEXED)             │
│ password_hash                       │
│ name                                │
│ created_at                          │
│ updated_at                          │
└─────────────────────────────────────┘
         │
         │ 1
         │
         │ has many
         │
         │ N
         ▼
┌─────────────────────────────────────┐
│ Task                                │
├─────────────────────────────────────┤
│ id (PK)                             │
│ title                               │
│ description (NULLABLE)              │
│ completed (DEFAULT: false)          │
│ user_id (FK, INDEXED)               │
│ created_at                          │
│ updated_at                          │
└─────────────────────────────────────┘
```

**Relationship Type**: One-to-Many (1:N)
- One User can have many Tasks
- Each Task belongs to exactly one User
- Cascade Delete: When User is deleted, all their Tasks are deleted

---

## Data Model Validation

### Specification Compliance

✅ **User Entity**:
- All attributes from spec.md Key Entities section included
- Email unique constraint enforced (FR-005)
- Password hashing required (FR-004)
- Timestamps included (created_at, updated_at)

✅ **Task Entity**:
- All attributes from spec.md Key Entities section included
- Title validation (max 200 chars) enforced (FR-024)
- Description validation (max 2000 chars) enforced (FR-025)
- Completed default value (false) enforced (FR-026)
- User isolation via user_id foreign key (FR-016, FR-023)
- Timestamps included (FR-027, FR-028)

✅ **Relationships**:
- One-to-Many relationship correctly defined
- Foreign key constraint with CASCADE delete
- Indexes on frequently queried fields (email, user_id)

✅ **Constitution Compliance**:
- User isolation enforced at database level (Section V)
- No manual coding - model derived from specifications (Section II)
- SQLModel required technology used (Section IV)

---

## Migration Strategy

### Initial Migration

**Order of Operations**:
1. Create `users` table first (no dependencies)
2. Create `tasks` table second (depends on users table)

**Migration Tool**: Alembic (standard for SQLModel/SQLAlchemy)

### Migration Considerations

- **Indexes**: Create indexes on email and user_id for performance
- **Constraints**: Enforce unique email and foreign key constraints
- **Defaults**: Set default values for completed, created_at, updated_at
- **Rollback**: Ensure migrations can be rolled back safely

---

## Performance Considerations

### Query Optimization

**User Queries**:
- Login by email: O(1) with email index
- User lookup by ID: O(1) with primary key

**Task Queries**:
- List user's tasks: O(N) with user_id index, where N = user's task count
- Get single task: O(1) with primary key + user_id filter
- Expected performance: <100ms for 1000 tasks (SC-007)

### Scalability

**Current Design**:
- Suitable for thousands of users
- Suitable for thousands of tasks per user
- No pagination initially (return all user's tasks)

**Future Optimization** (if needed):
- Add pagination for large task lists
- Add composite index on (user_id, created_at) for sorted queries
- Consider soft deletes instead of hard deletes

---

## Edge Cases

### Concurrent Operations

**Scenario**: Two clients update same task simultaneously
**Mitigation**: Database-level constraints, optimistic locking if needed

### Orphaned Data

**Scenario**: User deleted, what happens to tasks?
**Mitigation**: CASCADE delete ensures tasks are automatically removed

### Empty Collections

**Scenario**: User has no tasks
**Mitigation**: Return empty array (200 OK), not 404 (per spec edge cases)

### Special Characters

**Scenario**: Task title/description contains emojis, Unicode
**Mitigation**: PostgreSQL UTF-8 encoding handles Unicode correctly

---

## Summary

This data model defines two entities (User, Task) with a one-to-many relationship. All attributes, constraints, and validation rules are derived from the approved specification. User isolation is enforced at both application and database levels. The model is optimized for performance with appropriate indexes and follows SQLModel best practices.

**Next Steps**: Create API contracts (contracts/) and quickstart guide (quickstart.md) in Phase 1.
