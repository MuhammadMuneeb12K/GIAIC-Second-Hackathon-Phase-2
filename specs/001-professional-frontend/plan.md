# Implementation Plan: Professional Frontend for Multi-User Todo Application

**Branch**: `001-professional-frontend` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-professional-frontend/spec.md`

## Summary

Build a professional, production-grade frontend for a multi-user Todo Web Application using Next.js App Router, TypeScript, and Tailwind CSS. The frontend must provide secure authentication via Better Auth, comprehensive task management (CRUD operations), and a fully responsive design that works seamlessly across mobile, tablet, and desktop devices. The application must meet professional UI standards with consistent visual design, proper accessibility (WCAG AA), and intuitive user experience comparable to commercial SaaS products.

**Primary Requirements**:
- User authentication (signup, signin, signout) with Better Auth and JWT tokens
- Task management interface (create, read, update, delete, toggle completion)
- Fully responsive design (mobile ≤640px, tablet 641-1024px, desktop ≥1025px)
- Professional UI with loading, error, empty, and success states
- Keyboard navigable with WCAG AA accessibility compliance
- Centralized API client for backend communication

## Technical Context

**Language/Version**: TypeScript 5.x with strict mode enabled
**Primary Dependencies**: Next.js 14+ (App Router), React 18+, Tailwind CSS 3.x, Better Auth
**Storage**: N/A (frontend only - backend API handles persistence)
**Testing**: Jest + React Testing Library for component tests, Playwright for E2E tests
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge) with ES6+ support
**Project Type**: Web application (frontend only)
**Performance Goals**:
- Initial page load <3 seconds on standard broadband
- Page transitions <200ms perceived delay
- Task operations provide visual feedback within 100ms
**Constraints**:
- No backend implementation (frontend assumes API exists)
- No offline functionality required
- English language only
- No real-time synchronization across devices
**Scale/Scope**:
- 3 main pages (signin, signup, dashboard)
- ~15-20 reusable components
- Support for unlimited tasks per user (no pagination required for MVP)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Technology Constraints Compliance

✅ **Frontend Stack Requirements**:
- Next.js (App Router architecture) - COMPLIANT
- TypeScript (strict mode) - COMPLIANT
- Tailwind CSS - COMPLIANT
- Better Auth for authentication - COMPLIANT

✅ **Development Workflow**:
- Specification phase completed (spec.md exists)
- Planning phase in progress (this document)
- Implementation phase awaits explicit activation
- Verification phase will follow implementation

✅ **Spec-Driven Development**:
- All requirements traced to spec.md
- No implementation without specs
- Plans reference specific spec sections

✅ **Agent Governance**:
- Frontend Engineer Agent: Authorized for this feature
- Spec Architect Agent: Available for clarification
- Other agents: Remain idle per constitution

✅ **Security Requirements**:
- Authentication via Better Auth (frontend token management)
- JWT tokens attached to all API requests
- Protected routes redirect unauthenticated users
- No JWT verification on frontend (backend responsibility)

### Constitution Compliance Status

**Status**: ✅ PASSED - All constitution requirements met

**Notes**:
- Frontend-only scope aligns with monorepo structure (frontend/ directory)
- No backend logic assumed or implemented
- All user isolation enforced by backend API (frontend displays only user's data)
- Spec-driven approach maintained throughout planning

## Project Structure

### Documentation (this feature)

```text
specs/001-professional-frontend/
├── spec.md                    # Feature specification (completed)
├── plan.md                    # This file (in progress)
├── research.md                # Phase 0 output (to be created)
├── data-model.md              # Phase 1 output (to be created)
├── quickstart.md              # Phase 1 output (to be created)
├── contracts/                 # Phase 1 output (to be created)
│   ├── auth-api.yaml         # Authentication API contract
│   └── tasks-api.yaml        # Tasks API contract
└── checklists/
    └── requirements.md        # Specification quality checklist (completed)
```

### Source Code (repository root)

```text
frontend/
├── app/                       # Next.js App Router
│   ├── (auth)/               # Auth route group (public)
│   │   ├── signin/
│   │   │   └── page.tsx      # Sign in page
│   │   └── signup/
│   │       └── page.tsx      # Sign up page
│   ├── (dashboard)/          # Dashboard route group (protected)
│   │   ├── layout.tsx        # Dashboard layout with auth check
│   │   └── page.tsx          # Tasks dashboard (main page)
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Landing/redirect page
│   └── globals.css           # Global styles (Tailwind)
├── components/               # Reusable components
│   ├── ui/                   # Base UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   └── LoadingSpinner.tsx
│   ├── auth/                 # Auth-specific components
│   │   ├── SignInForm.tsx
│   │   ├── SignUpForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── tasks/                # Task-specific components
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskForm.tsx
│   │   ├── EmptyState.tsx
│   │   └── TaskDeleteConfirm.tsx
│   └── layout/               # Layout components
│       ├── Header.tsx
│       ├── Navigation.tsx
│       └── Footer.tsx
├── contexts/                 # React contexts
│   └── AuthContext.tsx       # Authentication context
├── lib/                      # Utilities and helpers
│   ├── api/
│   │   ├── client.ts         # Centralized API client
│   │   ├── auth.ts           # Auth API methods
│   │   └── tasks.ts          # Tasks API methods
│   ├── hooks/                # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useTasks.ts
│   │   └── useToast.ts
│   └── utils/
│       ├── validation.ts     # Input validation helpers
│       └── formatting.ts     # Data formatting helpers
├── types/                    # TypeScript type definitions
│   ├── auth.ts               # Auth-related types
│   ├── task.ts               # Task-related types
│   └── api.ts                # API response types
├── public/                   # Static assets
│   └── images/
├── tests/                    # Test files
│   ├── components/
│   ├── integration/
│   └── e2e/
├── tailwind.config.ts        # Tailwind configuration
├── tsconfig.json             # TypeScript configuration
├── next.config.js            # Next.js configuration
└── package.json              # Dependencies
```

**Structure Decision**: Using Next.js App Router with route groups for organization. The `(auth)` group contains public authentication pages, while `(dashboard)` contains protected pages requiring authentication. Components are organized by domain (ui, auth, tasks, layout) for maintainability. The centralized API client in `lib/api/` handles all backend communication with automatic token attachment.

## Complexity Tracking

> **No violations detected - this section intentionally left empty**

All implementation choices align with constitution requirements and follow standard Next.js App Router patterns.

---

## Phase 0: Research & Technology Decisions

### Research Tasks

**No NEEDS CLARIFICATION items** - All technical decisions are clear from specification:

1. **Next.js App Router Best Practices**
   - Decision: Use App Router with route groups for auth vs protected pages
   - Rationale: App Router is the modern Next.js standard, provides better performance with Server Components
   - Alternatives: Pages Router (deprecated), other React frameworks (not allowed per constitution)

2. **Better Auth Integration Pattern**
   - Decision: Use Better Auth for frontend token management with React Context for state
   - Rationale: Better Auth is specified in constitution, provides JWT token handling
   - Alternatives: Custom auth implementation (more complex, reinventing wheel)

3. **Tailwind CSS Configuration**
   - Decision: Mobile-first approach with custom breakpoints (sm: 640px, md: 1024px, lg: 1025px+)
   - Rationale: Matches spec requirements for responsive design breakpoints
   - Alternatives: CSS-in-JS (not specified), CSS Modules (less utility-focused)

4. **API Client Architecture**
   - Decision: Axios-based centralized client with request/response interceptors
   - Rationale: Interceptors allow automatic token attachment and error handling
   - Alternatives: Fetch API (less features), React Query (adds complexity for MVP)

5. **State Management Strategy**
   - Decision: React Context for auth state, local component state for UI, no global state library
   - Rationale: Simple MVP scope doesn't require Redux/Zustand complexity
   - Alternatives: Redux (overkill), Zustand (unnecessary for current scope)

6. **Component Library Approach**
   - Decision: Build custom components with Tailwind, no third-party UI library
   - Rationale: Full control over styling, meets professional UI requirements
   - Alternatives: shadcn/ui (adds dependency), Material-UI (different design system)

7. **Form Handling Strategy**
   - Decision: Controlled components with custom validation, no form library for MVP
   - Rationale: Simple forms (email/password, task title/description) don't require React Hook Form
   - Alternatives: React Hook Form (adds complexity), Formik (deprecated)

8. **Testing Strategy**
   - Decision: Jest + React Testing Library for components, Playwright for E2E
   - Rationale: Industry standard, good TypeScript support
   - Alternatives: Vitest (newer but less mature), Cypress (heavier than Playwright)

### Technology Stack Summary

| Category | Technology | Version | Justification |
|----------|-----------|---------|---------------|
| Framework | Next.js | 14+ | Constitution requirement, App Router for modern patterns |
| Language | TypeScript | 5.x | Constitution requirement, strict mode for type safety |
| Styling | Tailwind CSS | 3.x | Constitution requirement, utility-first for rapid development |
| Authentication | Better Auth | Latest | Constitution requirement, JWT token management |
| HTTP Client | Axios | 1.x | Interceptors for token attachment, better error handling |
| Testing (Unit) | Jest + RTL | Latest | Industry standard for React component testing |
| Testing (E2E) | Playwright | Latest | Modern, fast, cross-browser E2E testing |
| State Management | React Context | Built-in | Sufficient for MVP scope, no external library needed |

---

## Phase 1: Design & Contracts

### Data Model

**Frontend Data Structures** (TypeScript interfaces):

```typescript
// types/auth.ts
interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// types/task.ts
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;  // ISO 8601 format
  updatedAt: string;  // ISO 8601 format
  userId: string;
}

interface TaskFormData {
  title: string;
  description?: string;
}

// types/api.ts
interface ApiResponse<T> {
  data: T;
  message?: string;
}

interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}
```

### API Contracts

**Authentication API** (`contracts/auth-api.yaml`):

```yaml
# POST /api/auth/signup
Request:
  email: string (required, valid email format)
  password: string (required, min 8 characters)
  name: string (optional)

Response (201 Created):
  accessToken: string
  refreshToken: string
  expiresIn: number
  user: { id, email, name }

Errors:
  400: Invalid input (validation errors)
  409: Email already exists

# POST /api/auth/signin
Request:
  email: string (required)
  password: string (required)

Response (200 OK):
  accessToken: string
  refreshToken: string
  expiresIn: number
  user: { id, email, name }

Errors:
  401: Invalid credentials
  400: Invalid input

# POST /api/auth/signout
Request:
  Headers: Authorization: Bearer {accessToken}

Response (204 No Content):
  (empty)

Errors:
  401: Unauthorized (invalid/expired token)

# POST /api/auth/refresh
Request:
  refreshToken: string (required)

Response (200 OK):
  accessToken: string
  refreshToken: string
  expiresIn: number

Errors:
  401: Invalid/expired refresh token
```

**Tasks API** (`contracts/tasks-api.yaml`):

```yaml
# GET /api/tasks
Request:
  Headers: Authorization: Bearer {accessToken}

Response (200 OK):
  tasks: Task[]

Errors:
  401: Unauthorized

# POST /api/tasks
Request:
  Headers: Authorization: Bearer {accessToken}
  Body:
    title: string (required, max 200 chars)
    description: string (optional, max 2000 chars)

Response (201 Created):
  task: Task

Errors:
  400: Invalid input
  401: Unauthorized

# GET /api/tasks/{id}
Request:
  Headers: Authorization: Bearer {accessToken}

Response (200 OK):
  task: Task

Errors:
  401: Unauthorized
  403: Forbidden (not user's task)
  404: Task not found

# PUT /api/tasks/{id}
Request:
  Headers: Authorization: Bearer {accessToken}
  Body:
    title: string (optional)
    description: string (optional)
    completed: boolean (optional)

Response (200 OK):
  task: Task

Errors:
  400: Invalid input
  401: Unauthorized
  403: Forbidden
  404: Task not found

# DELETE /api/tasks/{id}
Request:
  Headers: Authorization: Bearer {accessToken}

Response (204 No Content):
  (empty)

Errors:
  401: Unauthorized
  403: Forbidden
  404: Task not found
```

### Component Architecture

**Component Hierarchy**:

```
App (Root Layout)
├── Header (Navigation, User Menu)
├── Main Content
│   ├── (auth) Route Group
│   │   ├── SignInPage
│   │   │   └── SignInForm
│   │   │       ├── Input (email)
│   │   │       ├── Input (password)
│   │   │       └── Button (submit)
│   │   └── SignUpPage
│   │       └── SignUpForm
│   │           ├── Input (email)
│   │           ├── Input (password)
│   │           ├── Input (name, optional)
│   │           └── Button (submit)
│   └── (dashboard) Route Group
│       └── DashboardPage (Protected)
│           ├── TaskForm (create new task)
│           │   ├── Input (title)
│           │   ├── Input (description)
│           │   └── Button (submit)
│           ├── TaskList
│           │   └── TaskItem (repeated)
│           │       ├── Checkbox (toggle completion)
│           │       ├── Text (title, description)
│           │       ├── Button (edit)
│           │       └── Button (delete)
│           └── EmptyState (when no tasks)
└── Footer
```

**Component Responsibilities**:

1. **Layout Components**:
   - `Header`: Navigation, user menu, signout button
   - `Footer`: Copyright, links (if needed)

2. **Auth Components**:
   - `SignInForm`: Email/password form, error display, loading state
   - `SignUpForm`: Email/password/name form, error display, loading state
   - `ProtectedRoute`: HOC/wrapper for auth-protected pages

3. **Task Components**:
   - `TaskList`: Container for task items, handles empty state
   - `TaskItem`: Individual task display, toggle completion, edit/delete actions
   - `TaskForm`: Create/edit task form with validation
   - `EmptyState`: Friendly message when no tasks exist
   - `TaskDeleteConfirm`: Confirmation modal for task deletion

4. **UI Components** (reusable):
   - `Button`: Styled button with variants (primary, secondary, danger)
   - `Input`: Form input with label, error message, validation states
   - `Card`: Container with consistent styling
   - `Modal`: Overlay modal for confirmations
   - `LoadingSpinner`: Loading indicator

### Page Structure

**1. Landing Page** (`app/page.tsx`):
- Purpose: Redirect to signin or dashboard based on auth state
- Behavior: Check auth, redirect authenticated users to dashboard, others to signin
- No UI content (just redirect logic)

**2. Sign In Page** (`app/(auth)/signin/page.tsx`):
- Purpose: User authentication
- Components: SignInForm
- Features: Email/password inputs, validation, error display, link to signup
- Success: Redirect to dashboard
- Responsive: Single column form, centered on all screen sizes

**3. Sign Up Page** (`app/(auth)/signup/page.tsx`):
- Purpose: New user registration
- Components: SignUpForm
- Features: Email/password/name inputs, validation, error display, link to signin
- Success: Auto-signin and redirect to dashboard
- Responsive: Single column form, centered on all screen sizes

**4. Dashboard Page** (`app/(dashboard)/page.tsx`):
- Purpose: Main task management interface
- Components: Header, TaskForm, TaskList, EmptyState
- Features: Create task, view tasks, edit tasks, delete tasks, toggle completion
- Protected: Requires authentication
- Responsive:
  - Mobile: Stacked layout, full-width components
  - Tablet: Two-column layout (form + list)
  - Desktop: Comfortable max-width with sidebar potential

### Authentication Flow

**Signup Flow**:
1. User navigates to `/signup`
2. User enters email, password, optional name
3. Frontend validates input (email format, password length)
4. On submit, call `POST /api/auth/signup`
5. On success: Store tokens, update auth context, redirect to `/dashboard`
6. On error: Display error message, keep user on signup page

**Signin Flow**:
1. User navigates to `/signin`
2. User enters email and password
3. Frontend validates input
4. On submit, call `POST /api/auth/signin`
5. On success: Store tokens, update auth context, redirect to `/dashboard`
6. On error: Display error message, keep user on signin page

**Signout Flow**:
1. User clicks signout button in header
2. Call `POST /api/auth/signout` (optional, for backend cleanup)
3. Clear tokens from storage
4. Update auth context (set user to null)
5. Redirect to `/signin`

**Session Handling**:
- Store access token in memory (React Context)
- Store refresh token in httpOnly cookie (if supported) or localStorage
- On 401 response, attempt token refresh
- If refresh fails, redirect to signin

**Route Protection**:
- Protected routes check auth state in layout
- Unauthenticated users redirected to `/signin`
- Authenticated users accessing `/signin` or `/signup` redirected to `/dashboard`

### API Client Strategy

**Centralized API Client** (`lib/api/client.ts`):

```typescript
// Axios instance with base configuration
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Attach auth token
apiClient.interceptors.request.use((config) => {
  const token = getAccessToken(); // From auth context or storage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle errors and token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Attempt token refresh
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        // Retry original request
        return apiClient(error.config);
      } else {
        // Redirect to signin
        redirectToSignin();
      }
    }
    return Promise.reject(error);
  }
);
```

**API Service Modules**:

1. **Auth Service** (`lib/api/auth.ts`):
   - `signup(email, password, name)`: Register new user
   - `signin(email, password)`: Authenticate user
   - `signout()`: End session
   - `refreshToken(refreshToken)`: Get new access token

2. **Tasks Service** (`lib/api/tasks.ts`):
   - `getTasks()`: Fetch all user tasks
   - `getTask(id)`: Fetch single task
   - `createTask(data)`: Create new task
   - `updateTask(id, data)`: Update existing task
   - `deleteTask(id)`: Delete task

**Mock Strategy for Frontend-Only Phase**:
- Create mock implementations of API services
- Return realistic data with simulated delays
- Store mock data in memory (useState/Context)
- Switch to real API by changing import path

### Responsive Design Strategy

**Mobile-First Approach**:
- Base styles target mobile (≤640px)
- Use Tailwind responsive prefixes for larger screens (`md:`, `lg:`)
- Test on mobile first, then scale up

**Breakpoint Behavior**:

1. **Mobile (≤640px)**:
   - Single column layout
   - Full-width components
   - Stacked navigation (hamburger menu if needed)
   - Touch-friendly buttons (min 44x44px)
   - Larger font sizes for readability

2. **Tablet (641-1024px)**:
   - Two-column layout where appropriate
   - Sidebar navigation (if applicable)
   - Increased spacing and padding
   - Optimized for both portrait and landscape

3. **Desktop (≥1025px)**:
   - Max-width container (e.g., 1200px) for comfortable reading
   - Multi-column layouts
   - Hover states for interactive elements
   - Larger spacing and visual hierarchy

**Navigation Adaptations**:
- Mobile: Hamburger menu or bottom navigation
- Tablet/Desktop: Horizontal navigation bar or sidebar

**Component Responsiveness**:
- `TaskList`: Grid on desktop, list on mobile
- `TaskForm`: Inline on desktop, modal on mobile (optional)
- `Header`: Collapsible menu on mobile, full menu on desktop

### Accessibility Plan

**Keyboard Navigation**:
- All interactive elements accessible via Tab key
- Logical tab order (top to bottom, left to right)
- Skip links for main content
- Escape key closes modals
- Enter key submits forms

**Focus Management**:
- Visible focus indicators (outline or ring)
- Focus trap in modals
- Return focus after modal close
- Focus on first error in forms

**Semantic HTML**:
- Use `<button>` for actions, `<a>` for navigation
- Proper heading hierarchy (`<h1>`, `<h2>`, etc.)
- `<form>` elements for all forms
- `<label>` elements for all inputs
- `<main>`, `<nav>`, `<header>`, `<footer>` landmarks

**ARIA Attributes**:
- `aria-label` for icon-only buttons
- `aria-describedby` for error messages
- `aria-live` for dynamic content updates
- `aria-expanded` for collapsible elements
- `role="alert"` for error messages

**Color Contrast**:
- Text: 4.5:1 minimum (WCAG AA)
- Large text: 3:1 minimum
- Interactive elements: 3:1 minimum
- Use Tailwind's default colors (already WCAG compliant)

**Screen Reader Support**:
- Descriptive link text (no "click here")
- Alt text for images (if any)
- Form labels and error messages
- Loading state announcements

### Risks & Mitigations

**Risk 1: Backend API Not Ready**
- **Impact**: Cannot test with real data, authentication may not work
- **Mitigation**:
  - Create mock API services with realistic data
  - Define API contracts early (Phase 1)
  - Use mock service worker (MSW) for testing
  - Switch to real API by changing import paths

**Risk 2: Better Auth Integration Complexity**
- **Impact**: Authentication may take longer than expected
- **Mitigation**:
  - Review Better Auth documentation thoroughly
  - Create proof-of-concept for token management
  - Use React Context for simple state management
  - Implement token refresh logic early

**Risk 3: Responsive Design Challenges**
- **Impact**: Layout may break on certain screen sizes
- **Mitigation**:
  - Use mobile-first approach
  - Test on real devices throughout development
  - Use browser dev tools responsive mode
  - Leverage Tailwind's responsive utilities

**Risk 4: Accessibility Compliance**
- **Impact**: May not meet WCAG AA standards
- **Mitigation**:
  - Use semantic HTML from the start
  - Test with keyboard navigation regularly
  - Use browser accessibility audits (Lighthouse)
  - Add ARIA attributes where needed

**Risk 5: Performance on Mobile Devices**
- **Impact**: Application may feel slow on lower-end devices
- **Mitigation**:
  - Use Next.js Server Components by default
  - Optimize bundle size (code splitting)
  - Lazy load components where appropriate
  - Test on real mobile devices

**Risk 6: State Management Complexity**
- **Impact**: Auth and task state may become difficult to manage
- **Mitigation**:
  - Keep state management simple (React Context)
  - Separate auth state from task state
  - Use local component state where possible
  - Consider React Query if complexity grows

**Risk 7: Form Validation Consistency**
- **Impact**: Inconsistent validation across forms
- **Mitigation**:
  - Create reusable validation utilities
  - Define validation rules in one place
  - Use consistent error message format
  - Test validation thoroughly

**Risk 8: Token Expiry Handling**
- **Impact**: Users may be unexpectedly logged out
- **Mitigation**:
  - Implement automatic token refresh
  - Show warning before session expires
  - Preserve form data on auth errors
  - Clear error messages for auth failures

---

## Implementation Readiness

### Prerequisites Checklist

- [x] Specification completed and validated
- [x] Constitution compliance verified
- [x] Technology stack decided
- [x] API contracts defined
- [x] Component architecture designed
- [x] Responsive strategy planned
- [x] Accessibility requirements documented
- [x] Risks identified with mitigations

### Next Steps

1. **Phase 2: Task Breakdown** (via `/sp.tasks` command)
   - Break down implementation into specific tasks
   - Organize tasks by user story priority
   - Define acceptance criteria for each task

2. **Implementation Phase** (awaits explicit activation)
   - Set up Next.js project with TypeScript and Tailwind
   - Implement authentication flow (P1)
   - Implement task management (P2)
   - Implement responsive design (P3)
   - Add accessibility features
   - Write tests

3. **Verification Phase**
   - QA Agent verifies spec compliance
   - Test on multiple devices and browsers
   - Accessibility audit
   - Performance testing

### Success Criteria Mapping

All success criteria from spec.md are addressed in this plan:

- **SC-001 to SC-005**: User experience metrics addressed through intuitive UI design
- **SC-006 to SC-009**: Responsive design strategy covers all breakpoints
- **SC-010 to SC-013**: Accessibility plan ensures WCAG AA compliance
- **SC-014 to SC-018**: Professional quality through consistent design system
- **SC-019 to SC-021**: Performance addressed through Next.js optimization
- **SC-022 to SC-024**: Reliability through error handling and validation

---

**Plan Status**: ✅ COMPLETE - Ready for task breakdown (`/sp.tasks`)

**Implementation Authorization**: ⏸️ AWAITING ACTIVATION - No code generation until explicit command
