# Tasks: Backend API for Multi-User Todo Application

**Feature Branch**: `002-backend-api`
**Input**: Design documents from `/specs/002-backend-api/`
**Prerequisites**: plan.md, spec.md (user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - test tasks omitted per template guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/` directory at repository root
- All backend code in `backend/app/` following FastAPI best practices
- Tests in `backend/tests/` (if added later)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend/ directory structure per research.md (app/, app/models/, app/schemas/, app/api/, app/api/routes/, app/core/, app/services/)
- [X] T002 Initialize Python project with requirements.txt in backend/ (fastapi, uvicorn, sqlmodel, psycopg2-binary, python-jose[cryptography], passlib[bcrypt], python-dotenv, pydantic-settings)
- [X] T003 [P] Create .env.example file in backend/ with required environment variables (DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS)
- [X] T004 [P] Create backend/README.md with setup instructions and API documentation links

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Pydantic Settings configuration class in backend/app/config.py (validate DATABASE_URL, BETTER_AUTH_SECRET min 32 chars, FRONTEND_URL, token expiration settings)
- [X] T006 Setup database connection and session management in backend/app/database.py (SQLModel engine, async session factory, connection pooling)
- [X] T007 [P] Implement password hashing utilities in backend/app/core/security.py (bcrypt with cost factor 12, hash_password, verify_password functions)
- [X] T008 [P] Implement JWT token utilities in backend/app/core/security.py (create_access_token, create_refresh_token, verify_token functions using HS256 algorithm)
- [X] T009 [P] Create custom exception classes in backend/app/core/exceptions.py (AuthenticationError, AuthorizationError, ValidationError, NotFoundError)
- [X] T010 Create FastAPI application instance in backend/app/main.py (configure CORS for FRONTEND_URL, add exception handlers, include API routers with /api prefix)
- [X] T011 Create authentication dependency in backend/app/api/deps.py (get_current_user function that validates JWT and extracts user_id)
- [X] T012 [P] Create database session dependency in backend/app/api/deps.py (get_db function for dependency injection)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication and Account Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, sign in securely, and maintain authenticated sessions with JWT tokens

**Independent Test**: Create account via POST /api/auth/signup, sign in via POST /api/auth/signin to receive JWT token, use token to access protected endpoint (e.g., GET /api/tasks)

### Implementation for User Story 1

- [X] T013 [P] [US1] Create User SQLModel in backend/app/models/user.py (id, email unique indexed, password_hash, name, created_at, updated_at, relationship to tasks)
- [X] T014 [P] [US1] Create Pydantic request schemas in backend/app/schemas/auth.py (SignupRequest, SigninRequest, RefreshRequest with validation rules)
- [X] T015 [P] [US1] Create Pydantic response schemas in backend/app/schemas/auth.py (UserResponse, AuthResponse with user/tokens, RefreshResponse, MessageResponse)
- [X] T016 [US1] Implement user registration logic in backend/app/services/auth_service.py (create_user function: validate email uniqueness, hash password, create user record)
- [X] T017 [US1] Implement user authentication logic in backend/app/services/auth_service.py (authenticate_user function: verify email exists, verify password, return user)
- [X] T018 [US1] Implement POST /api/auth/signup endpoint in backend/app/api/routes/auth.py (validate request, call create_user, generate tokens, return 201 with user and tokens)
- [X] T019 [US1] Implement POST /api/auth/signin endpoint in backend/app/api/routes/auth.py (validate credentials, call authenticate_user, generate tokens, return 200 with user and tokens)
- [X] T020 [US1] Implement POST /api/auth/refresh endpoint in backend/app/api/routes/auth.py (validate refresh token, generate new access token, return 200 with new token)
- [X] T021 [US1] Implement POST /api/auth/signout endpoint in backend/app/api/routes/auth.py (require authentication, return 200 success message)
- [X] T022 [US1] Add comprehensive error handling to auth endpoints (422 for validation errors, 409 for duplicate email, 401 for invalid credentials, 400 for malformed JSON)
- [X] T023 [US1] Add input validation to auth endpoints (email regex, password min 8 chars, name max 100 chars per FR-002, FR-003)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, signin, refresh tokens, and signout

---

## Phase 4: User Story 2 - Task Management with User Isolation (Priority: P2)

**Goal**: Enable authenticated users to create, read, update, delete, and toggle completion of their personal tasks with strict user isolation

**Independent Test**: Authenticate user, create tasks via POST /api/tasks, retrieve via GET /api/tasks, update via PUT /api/tasks/{id}, toggle via PATCH /api/tasks/{id}/toggle, delete via DELETE /api/tasks/{id}. Verify user isolation by attempting to access another user's tasks (should return 404)

### Implementation for User Story 2

- [X] T024 [P] [US2] Create Task SQLModel in backend/app/models/task.py (id, title max 200, description max 2000 nullable, completed default false, user_id foreign key indexed, created_at, updated_at, relationship to user)
- [X] T025 [P] [US2] Create Pydantic request schemas in backend/app/schemas/task.py (CreateTaskRequest, UpdateTaskRequest with validation rules per FR-024, FR-025)
- [X] T026 [P] [US2] Create Pydantic response schemas in backend/app/schemas/task.py (TaskResponse with all fields per FR-042)
- [X] T027 [US2] Implement task creation logic in backend/app/services/task_service.py (create_task function: validate title/description, set user_id from current_user, set completed=false, create task record)
- [X] T028 [US2] Implement task retrieval logic in backend/app/services/task_service.py (get_user_tasks function: query tasks filtered by user_id for user isolation per FR-023)
- [X] T029 [US2] Implement single task retrieval logic in backend/app/services/task_service.py (get_task_by_id function: query by id AND user_id, return None if not found for user isolation per FR-019)
- [X] T030 [US2] Implement task update logic in backend/app/services/task_service.py (update_task function: validate ownership via user_id filter, update title/description, update updated_at timestamp per FR-028)
- [X] T031 [US2] Implement task toggle logic in backend/app/services/task_service.py (toggle_task_completion function: validate ownership, toggle completed boolean, update updated_at)
- [X] T032 [US2] Implement task deletion logic in backend/app/services/task_service.py (delete_task function: validate ownership via user_id filter, delete task record)
- [X] T033 [US2] Implement GET /api/tasks endpoint in backend/app/api/routes/tasks.py (require authentication, call get_user_tasks with current_user.id, return 200 with task array or empty array)
- [X] T034 [US2] Implement POST /api/tasks endpoint in backend/app/api/routes/tasks.py (require authentication, validate request, call create_task with current_user.id, return 201 with task object)
- [X] T035 [US2] Implement GET /api/tasks/{id} endpoint in backend/app/api/routes/tasks.py (require authentication, call get_task_by_id with user isolation, return 200 or 404 per FR-019)
- [X] T036 [US2] Implement PUT /api/tasks/{id} endpoint in backend/app/api/routes/tasks.py (require authentication, validate request, call update_task with user isolation, return 200 or 404)
- [X] T037 [US2] Implement PATCH /api/tasks/{id}/toggle endpoint in backend/app/api/routes/tasks.py (require authentication, call toggle_task_completion with user isolation, return 200 or 404)
- [X] T038 [US2] Implement DELETE /api/tasks/{id} endpoint in backend/app/api/routes/tasks.py (require authentication, call delete_task with user isolation, return 204 or 404)
- [X] T039 [US2] Add comprehensive error handling to task endpoints (422 for validation errors, 404 for not found/unauthorized access, 401 for missing auth, 400 for malformed JSON)
- [X] T040 [US2] Add input validation to task endpoints (title required max 200 chars, description optional max 2000 chars per FR-024, FR-025)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - full authentication and task management with user isolation

---

## Phase 5: User Story 3 - API Error Handling and Data Validation (Priority: P3)

**Goal**: Ensure consistent error responses and comprehensive input validation across all endpoints

**Independent Test**: Submit invalid data to various endpoints (invalid email, short password, missing title, title too long, malformed JSON) and verify appropriate error responses with correct HTTP status codes and clear error messages

### Implementation for User Story 3

- [X] T041 [P] [US3] Add global exception handler for validation errors in backend/app/main.py (catch Pydantic ValidationError, return 422 with detail field per FR-029, FR-035)
- [X] T042 [P] [US3] Add global exception handler for authentication errors in backend/app/main.py (catch AuthenticationError, return 401 with detail field per FR-030, FR-035)
- [X] T043 [P] [US3] Add global exception handler for not found errors in backend/app/main.py (catch NotFoundError, return 404 with detail field per FR-031, FR-035)
- [X] T044 [P] [US3] Add global exception handler for JSON parsing errors in backend/app/main.py (catch JSONDecodeError, return 400 with detail field per FR-033, FR-035)
- [X] T045 [P] [US3] Add global exception handler for unexpected errors in backend/app/main.py (catch generic Exception, log error, return 500 without sensitive details per FR-034, NFR-007)
- [X] T046 [US3] Enhance email validation in backend/app/schemas/auth.py (add email regex validator per FR-002, return clear error message)
- [X] T047 [US3] Enhance password validation in backend/app/schemas/auth.py (add min_length=8 validator per FR-003, return clear error message)
- [X] T048 [US3] Enhance title validation in backend/app/schemas/task.py (add min_length=1, max_length=200 validators per FR-024, return clear error messages)
- [X] T049 [US3] Enhance description validation in backend/app/schemas/task.py (add max_length=2000 validator per FR-025, return clear error message)
- [X] T050 [US3] Add duplicate email handling in backend/app/services/auth_service.py (catch unique constraint violation, raise custom exception, return 409 per FR-032)
- [X] T051 [US3] Verify all error responses follow consistent format with "detail" field per FR-035 and NFR-027

**Checkpoint**: All user stories should now have comprehensive error handling and validation - production-ready API

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and deployment preparation

- [X] T052 [P] Create database migration script or initialization logic in backend/app/database.py (create_db_and_tables function to initialize schema)
- [X] T053 [P] Add health check endpoint GET / in backend/app/main.py (return API info and status)
- [X] T054 [P] Verify OpenAPI documentation is auto-generated at /docs and /redoc endpoints per SC-009
- [X] T055 [P] Add logging configuration in backend/app/main.py (log all errors with context per NFR-015, never log passwords/tokens/secrets)
- [X] T056 [P] Add rate limiting middleware for auth endpoints in backend/app/main.py (prevent brute force attacks per NFR-005)
- [X] T057 [P] Verify CORS configuration allows FRONTEND_URL with credentials per FR-039, NFR-024
- [X] T058 [P] Add database indexes in models (email on users table, user_id on tasks table per NFR-011)
- [X] T059 [P] Verify CASCADE delete on tasks when user deleted (foreign key constraint in Task model)
- [ ] T060 Run manual verification using quickstart.md test flows (Test Flow 1: Authentication, Test Flow 2: Task Management, Test Flow 3: User Isolation, Test Flow 4: Validation)
- [ ] T061 Performance verification (auth endpoints <500ms per NFR-009, task endpoints <200ms per NFR-010, task retrieval <100ms for 1000 tasks per SC-007)
- [ ] T062 Security audit (verify password hashing with bcrypt cost 12, JWT signed with HS256, secrets in environment variables, no sensitive data in error messages)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Can start after Foundational - Depends on User model from US1 for foreign key relationship
  - User Story 3 (Phase 5): Can start after Foundational - Enhances US1 and US2 with better error handling
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - MVP)**: Can start after Foundational (Phase 2) - Creates User model needed by US2
- **User Story 2 (P2)**: Should start after US1 completes T013 (User model) - Task model has foreign key to User
- **User Story 3 (P3)**: Can start after US1 and US2 have basic implementations - Adds error handling to existing endpoints

### Within Each User Story

**User Story 1 (Authentication)**:
- T013 (User model) must complete before T016-T017 (services that use User model)
- T014-T015 (schemas) can run in parallel with T013
- T016-T017 (services) must complete before T018-T021 (endpoints that use services)
- T018-T021 (endpoints) can be implemented sequentially
- T022-T023 (error handling/validation) should be added after endpoints work

**User Story 2 (Task Management)**:
- T024 (Task model) must complete before T027-T032 (services that use Task model)
- T025-T026 (schemas) can run in parallel with T024
- T027-T032 (services) must complete before T033-T038 (endpoints that use services)
- T033-T038 (endpoints) can be implemented sequentially
- T039-T040 (error handling/validation) should be added after endpoints work

**User Story 3 (Error Handling)**:
- T041-T045 (global exception handlers) can all run in parallel
- T046-T049 (schema validators) can all run in parallel
- T050-T051 (service-level error handling) should be done after global handlers

### Parallel Opportunities

- **Setup Phase**: T003 and T004 can run in parallel
- **Foundational Phase**: T007, T008, T009, T012 can all run in parallel (different files)
- **User Story 1**: T013, T014, T015 can run in parallel (models and schemas)
- **User Story 2**: T024, T025, T026 can run in parallel (models and schemas)
- **User Story 3**: T041-T045 can run in parallel (different exception handlers), T046-T049 can run in parallel (different validators)
- **Polish Phase**: Most tasks (T052-T059) can run in parallel as they touch different concerns

---

## Parallel Example: User Story 1 (Authentication)

```bash
# Launch all foundational tasks together:
Task: "Implement password hashing utilities in backend/app/core/security.py"
Task: "Implement JWT token utilities in backend/app/core/security.py"
Task: "Create custom exception classes in backend/app/core/exceptions.py"
Task: "Create database session dependency in backend/app/api/deps.py"

# Launch all User Story 1 models and schemas together:
Task: "Create User SQLModel in backend/app/models/user.py"
Task: "Create Pydantic request schemas in backend/app/schemas/auth.py"
Task: "Create Pydantic response schemas in backend/app/schemas/auth.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T012) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T013-T023)
4. **STOP and VALIDATE**: Test authentication independently using quickstart.md Test Flow 1
5. Deploy/demo if ready - users can now signup and signin

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - Authentication working!)
3. Add User Story 2 → Test independently → Deploy/Demo (Full CRUD functionality!)
4. Add User Story 3 → Test independently → Deploy/Demo (Production-ready error handling!)
5. Add Polish → Final deployment (Performance optimized, fully documented)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T012)
2. Once Foundational is done:
   - Developer A: User Story 1 (T013-T023) - Authentication
   - Developer B: Wait for T013 (User model), then start User Story 2 (T024-T040) - Task Management
   - Developer C: User Story 3 (T041-T051) - Can start in parallel, enhances US1/US2
3. All developers: Polish phase together (T052-T062)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently testable (see quickstart.md for test flows)
- Tests are NOT included per specification (no TDD requirement stated)
- User Story 2 has soft dependency on User Story 1 (needs User model for foreign key)
- User Story 3 enhances US1 and US2 with better error handling
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All file paths are absolute from repository root (backend/app/...)
- Follow FastAPI best practices and research.md technology decisions
- Enforce user isolation at both application and database levels per constitution
