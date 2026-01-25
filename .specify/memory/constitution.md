<!--
Sync Impact Report:
Version: 1.0.0 (Initial Constitution)
Ratification Date: 2026-01-10
Last Amended: 2026-01-10

Changes:
- Initial constitution created for Hackathon II – Phase II
- Established 10 core principles covering purpose, rules, workflow, technology, security, governance, and success criteria
- Defined strict agent boundaries and role-based responsibilities
- Established spec-driven development as mandatory workflow
- Set technology stack constraints (Next.js, FastAPI, SQLModel, Better Auth, Neon PostgreSQL)

Templates Status:
✅ plan-template.md - Constitution Check section aligns with principles
✅ spec-template.md - User story prioritization aligns with workflow requirements
✅ tasks-template.md - Task organization aligns with development workflow
⚠️  Command files - Need to verify agent-specific references

Follow-up TODOs:
- None - all placeholders filled
-->

# Hackathon II – Phase II Todo Application Constitution

## Core Principles

### I. Purpose

This system exists to build a Full-Stack, Multi-User Todo Web Application using a spec-driven, agentic development workflow.

The system MUST transform a console-based Todo application into a modern web application with:
- Persistent storage (Neon PostgreSQL)
- Authentication (Better Auth + JWT)
- User isolation (enforced at database and API layers)
- RESTful API (FastAPI)
- Responsive frontend (Next.js App Router)

**Rationale**: This constitution exists solely to fulfill Hackathon II – Phase II requirements. All development must be traceable, auditable, and demonstrable to judges.

### II. Absolute Rules (NON-NEGOTIABLE)

The following rules are inviolable and override all other instructions:

1. NO manual coding by the user is allowed
2. All development MUST be spec-driven
3. All actions MUST be traceable to written specifications
4. No implementation may occur without relevant specs
5. Claude Code is the only entity allowed to write code
6. Human input is limited to prompts, reviews, and approvals
7. Sub-agents MUST obey their defined roles and boundaries
8. No agent may exceed its assigned scope
9. Security and user isolation are mandatory, not optional
10. Any ambiguity MUST be resolved by updating specs, not guessing

**Rationale**: These rules ensure accountability, traceability, and compliance with hackathon requirements. Violations compromise the entire project's integrity.

### III. Development Workflow (MANDATORY)

All work MUST follow this sequence without exception:

**1. Specification Phase**
- Validate existing specs
- Create missing specs using Spec-Kit Plus conventions
- Specs MUST include user stories and acceptance criteria
- Specs define WHAT, not HOW

**2. Planning Phase**
- Generate implementation plan strictly from specs
- Break work into backend, frontend, auth, and database tasks
- Plans MUST reference specific spec sections

**3. Implementation Phase**
- Backend: FastAPI + SQLModel
- Frontend: Next.js App Router + TypeScript
- Authentication: Better Auth (frontend) + JWT verification (backend)
- Database: Neon PostgreSQL with user isolation

**4. Verification Phase**
- QA Agent verifies spec compliance
- Integration Tester verifies cross-layer behavior
- Security Agent verifies auth and isolation

**Rationale**: No phase may be skipped or merged. This ensures quality gates and prevents implementation drift from specifications.

### IV. Technology Constraints

The following technologies are REQUIRED and non-negotiable:

**Frontend Stack:**
- Next.js (App Router architecture)
- TypeScript (strict mode)
- Tailwind CSS

**Backend Stack:**
- Python FastAPI
- SQLModel ORM
- Pydantic for validation

**Database:**
- Neon Serverless PostgreSQL

**Authentication:**
- Better Auth (frontend token management)
- JWT Tokens (backend verification)

**Repository Structure:**
- Monorepo (single repository)
- Shared Spec-Kit context
- Layered CLAUDE.md files

**Rationale**: Any deviation is prohibited unless explicitly stated in specs. This ensures consistency and prevents technology sprawl.

### V. Authentication & Security Law

Security is mandatory and non-negotiable. The following rules MUST be enforced:

1. All API endpoints MUST require a valid JWT token (except auth endpoints)
2. JWT tokens MUST be issued by Better Auth
3. FastAPI MUST verify JWT using a shared secret
4. User identity MUST be extracted from JWT only (never from URL or request body)
5. User ID in database queries MUST match the authenticated user
6. No user may access another user's data under any circumstances
7. Token expiry MUST be enforced
8. Unauthorized requests MUST return 401 status code
9. Forbidden requests (wrong user) MUST return 403 status code

**Rationale**: Security violations are critical failures. User data isolation is a core hackathon requirement and must be demonstrable to judges.

### VI. Spec-Kit Governance

Specifications are the single source of truth:

1. All specs live inside the `/specs` directory
2. Specs MUST be referenced using `@specs` paths
3. Specs define WHAT, not HOW
4. Implementation MUST conform exactly to specs
5. If specs change, implementation MUST be updated accordingly
6. Specs are version-controlled and auditable
7. No implementation without corresponding spec

**Rationale**: Spec-driven development ensures traceability and prevents scope creep. Judges can verify that implementation matches specifications.

### VII. Agent Governance

Agents operate under strict role boundaries. No agent may perform another agent's role:

**Orchestrator Agent:**
- Controls workflow and delegation only
- Cannot write code or specs

**Spec Architect Agent:**
- Writes and validates specifications only
- Cannot implement code

**Backend Engineer Agent:**
- Implements FastAPI backend only
- Cannot modify frontend or specs

**Frontend Engineer Agent:**
- Implements Next.js frontend only
- Cannot modify backend or specs

**Authentication & Security Agent:**
- Designs and verifies auth and JWT security
- Cannot implement unrelated features

**Database & ORM Agent:**
- Designs and validates database schema
- Cannot implement API endpoints

**QA & Spec Compliance Agent:**
- Audits implementation against specs
- Cannot modify code or specs

**Integration Tester Agent:**
- Verifies end-to-end system behavior
- Cannot modify implementation

**Rationale**: Role boundaries prevent conflicts, ensure expertise, and maintain clear accountability. Each agent is responsible for its domain only.

### VIII. Monorepo Structure Law

The repository MUST follow this structure:

```
/
├── .specify/              # Spec-Kit Plus templates and scripts
├── specs/                 # All specifications
├── frontend/              # Next.js application
├── backend/               # FastAPI application
├── CLAUDE.md              # Root-level agent guidance
├── frontend/CLAUDE.md     # Frontend-specific guidance
└── backend/CLAUDE.md      # Backend-specific guidance
```

**Rules:**
- All agents MUST respect this structure
- No code outside designated directories
- Specs remain separate from implementation
- CLAUDE.md files provide context-specific guidance

**Rationale**: Clear structure ensures agents know where to work and prevents file conflicts.

### IX. Execution Control

The system MUST remain idle until explicitly activated by the user.

**Valid Activation Commands:**
- "INITIALIZE SUB-AGENTS:"
- "EXECUTE PHASE II:"
- "BEGIN SPEC CREATION:"
- "/sp.specify [feature-name]"
- "/sp.plan [feature-name]"
- "/sp.tasks [feature-name]"
- "/sp.implement [feature-name]"

**Without Activation:**
- No planning
- No file creation
- No code generation
- No spec modification

**Rationale**: Prevents premature or unauthorized work. User maintains control over when work begins.

### X. Success Criteria

The system is successful ONLY if all of the following are true:

**Feature Completeness:**
- All Phase II features are implemented
- User registration and login work
- Task CRUD operations work
- User-specific task lists display correctly

**Security & Isolation:**
- Authentication is secure and enforced
- Each user sees only their own tasks
- JWT tokens are properly validated
- No cross-user data leakage

**Integration:**
- Frontend, backend, auth, and database integrate correctly
- API endpoints return expected responses
- Frontend displays data correctly
- Error handling works across all layers

**Compliance:**
- Implementation matches specs exactly
- Workflow is auditable and explainable to judges
- All code is generated by Claude Code (no manual coding)
- Spec-driven development is demonstrable

**Rationale**: These criteria are measurable and verifiable. Judges can validate each criterion independently.

## Development Standards

### Code Quality

**Backend (FastAPI):**
- Type hints required for all functions
- Pydantic models for all request/response schemas
- User isolation enforced in all database queries
- Error handling with appropriate HTTP status codes
- OpenAPI documentation auto-generated

**Frontend (Next.js):**
- TypeScript strict mode enabled
- Server Components by default, Client Components only when needed
- API calls through centralized client with auth headers
- Error boundaries for graceful error handling
- Responsive design with Tailwind CSS

**Database (SQLModel):**
- All models include `user_id` foreign key
- Indexes on frequently queried fields
- Timestamps (created_at, updated_at) on all models
- Proper relationships and cascading deletes

### Testing Requirements

**Backend Testing:**
- Unit tests for business logic
- Integration tests for API endpoints
- Authentication tests for protected routes
- User isolation tests (verify users cannot access other users' data)

**Frontend Testing:**
- Component tests with React Testing Library
- Integration tests for user flows
- Authentication flow tests

**End-to-End Testing:**
- Complete user journeys (signup → login → CRUD operations)
- Cross-browser compatibility
- Responsive design validation

## Governance

### Amendment Process

1. Amendments MUST be proposed in writing
2. Amendments MUST include rationale and impact analysis
3. Version number MUST be incremented according to semantic versioning:
   - **MAJOR**: Backward incompatible changes (e.g., removing a principle)
   - **MINOR**: New principles or sections added
   - **PATCH**: Clarifications, wording fixes, non-semantic changes
4. All dependent templates MUST be updated for consistency
5. Sync Impact Report MUST be generated and prepended to constitution

### Compliance Review

- All PRs MUST verify compliance with this constitution
- QA Agent MUST audit implementation against constitution principles
- Security Agent MUST verify authentication and isolation rules
- Any violations MUST be documented and resolved before merge

### Version Control

- Constitution is version-controlled in Git
- Changes are tracked in Sync Impact Report
- Historical versions are preserved for audit trail

### Conflict Resolution

In case of conflicts between documents:
1. This Constitution supersedes all other documents
2. Specs supersede implementation plans
3. Implementation plans supersede code
4. When in doubt, refer to this Constitution

**Version**: 1.0.0 | **Ratified**: 2026-01-10 | **Last Amended**: 2026-01-10
