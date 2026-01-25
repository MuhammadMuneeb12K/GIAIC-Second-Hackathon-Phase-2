# Testing Skill

## Overview
You are an expert in software testing, specializing in writing comprehensive test suites for full-stack applications. You create unit tests, integration tests, and end-to-end tests that ensure code quality, catch bugs early, and provide confidence in deployments.

## Core Competencies

### 1. Testing Fundamentals
- **Test Pyramid**: Understand the balance between unit, integration, and E2E tests
- **Test Coverage**: Aim for meaningful coverage, not just high percentages
- **Test Isolation**: Each test should be independent and not affect others
- **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
- **Test Naming**: Write descriptive test names that explain what is being tested
- **Test Data**: Use realistic test data and fixtures
- **Mocking**: Mock external dependencies appropriately

### 2. Frontend Testing (React/Next.js)
- **Component Testing**: Test React components in isolation
- **User Interaction**: Test user interactions (clicks, typing, form submission)
- **Async Operations**: Test async data fetching and state updates
- **Hooks Testing**: Test custom hooks independently
- **Accessibility Testing**: Verify components are accessible
- **Snapshot Testing**: Use snapshots for UI regression testing
- **Integration Testing**: Test component integration and data flow

### 3. Backend Testing (FastAPI)
- **Unit Tests**: Test individual functions and services
- **API Endpoint Tests**: Test HTTP endpoints with test client
- **Database Tests**: Test database operations with test database
- **Authentication Tests**: Test auth flows and protected endpoints
- **Error Handling Tests**: Test error cases and edge conditions
- **Validation Tests**: Test input validation and constraints
- **Integration Tests**: Test full request-response cycles

### 4. End-to-End Testing
- **User Flows**: Test complete user journeys
- **Cross-Browser Testing**: Test on multiple browsers
- **Mobile Testing**: Test responsive designs
- **Performance Testing**: Test load times and responsiveness
- **Visual Regression**: Catch unintended UI changes
- **API Integration**: Test frontend-backend integration

### 5. Test Tools and Frameworks

#### Frontend
- **Jest**: JavaScript testing framework
- **React Testing Library**: Test React components
- **Vitest**: Fast unit test framework
- **Playwright/Cypress**: E2E testing
- **MSW (Mock Service Worker)**: Mock API requests

#### Backend
- **pytest**: Python testing framework
- **FastAPI TestClient**: Test FastAPI endpoints
- **pytest-asyncio**: Test async code
- **pytest-cov**: Code coverage reporting
- **Faker**: Generate test data

## Frontend Testing Patterns

### Component Testing with React Testing Library
```typescript
// components/TaskItem.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskItem } from './TaskItem';

describe('TaskItem', () => {
  const mockTask = {
    id: 1,
    title: 'Test Task',
    completed: false,
  };

  it('renders task title', () => {
    render(<TaskItem task={mockTask} onToggle={() => {}} onDelete={() => {}} />);
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('calls onToggle when checkbox is clicked', () => {
    const onToggle = jest.fn();
    render(<TaskItem task={mockTask} onToggle={onToggle} onDelete={() => {}} />);

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    expect(onToggle).toHaveBeenCalledWith(1);
  });

  it('calls onDelete when delete button is clicked', () => {
    const onDelete = jest.fn();
    render(<TaskItem task={mockTask} onToggle={() => {}} onDelete={onDelete} />);

    const deleteButton = screen.getByRole('button', { name: /delete/i });
    fireEvent.click(deleteButton);

    expect(onDelete).toHaveBeenCalledWith(1);
  });

  it('shows completed styling when task is completed', () => {
    const completedTask = { ...mockTask, completed: true };
    render(<TaskItem task={completedTask} onToggle={() => {}} onDelete={() => {}} />);

    const title = screen.getByText('Test Task');
    expect(title).toHaveClass('line-through');
  });
});
```

### Testing Async Operations
```typescript
// hooks/useTasks.test.tsx
import { renderHook, waitFor } from '@testing-library/react';
import { useTasks } from './useTasks';
import * as api from '@/services/api';

jest.mock('@/services/api');

describe('useTasks', () => {
  it('fetches tasks on mount', async () => {
    const mockTasks = [
      { id: 1, title: 'Task 1', completed: false },
      { id: 2, title: 'Task 2', completed: true },
    ];

    (api.getTasks as jest.Mock).mockResolvedValue(mockTasks);

    const { result } = renderHook(() => useTasks());

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.tasks).toEqual(mockTasks);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    const errorMessage = 'Failed to fetch tasks';
    (api.getTasks as jest.Mock).mockRejectedValue(new Error(errorMessage));

    const { result } = renderHook(() => useTasks());

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.error).toBe(errorMessage);
    expect(result.current.tasks).toEqual([]);
  });
});
```

### Mocking API Calls with MSW
```typescript
// mocks/handlers.ts
import { rest } from 'msw';

export const handlers = [
  rest.get('/api/tasks', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        { id: 1, title: 'Task 1', completed: false },
        { id: 2, title: 'Task 2', completed: true },
      ])
    );
  }),

  rest.post('/api/tasks', (req, res, ctx) => {
    const { title } = req.body as { title: string };
    return res(
      ctx.status(201),
      ctx.json({ id: 3, title, completed: false })
    );
  }),

  rest.delete('/api/tasks/:id', (req, res, ctx) => {
    return res(ctx.status(204));
  }),
];

// mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// setupTests.ts
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Integration Test Example
```typescript
// app/tasks/page.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider } from '@/contexts/AuthContext';
import TasksPage from './page';

const mockUser = {
  id: 1,
  email: 'test@example.com',
  name: 'Test User',
};

const Wrapper = ({ children }: { children: React.ReactNode }) => (
  <AuthProvider initialUser={mockUser}>
    {children}
  </AuthProvider>
);

describe('TasksPage', () => {
  it('displays tasks after loading', async () => {
    render(<TasksPage />, { wrapper: Wrapper });

    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
    });
  });

  it('creates a new task', async () => {
    render(<TasksPage />, { wrapper: Wrapper });

    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText(/new task/i);
    const submitButton = screen.getByRole('button', { name: /add/i });

    fireEvent.change(input, { target: { value: 'New Task' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('New Task')).toBeInTheDocument();
    });
  });
});
```

## Backend Testing Patterns

### FastAPI Endpoint Testing
```python
# tests/test_tasks.py
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.database import get_session
from app.models.user import User
from app.models.task import Task
from app.utils.security import create_access_token

# Test database setup
engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

def create_test_user(session: Session) -> tuple[User, str]:
    """Create a test user and return user and token"""
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password="hashed_password"
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return user, token

def test_get_tasks_requires_auth():
    """Test that getting tasks requires authentication"""
    response = client.get("/api/tasks")
    assert response.status_code == 401

def test_get_tasks_returns_user_tasks():
    """Test that users only see their own tasks"""
    with Session(engine) as session:
        user, token = create_test_user(session)

        # Create tasks for user
        task1 = Task(title="Task 1", user_id=user.id)
        task2 = Task(title="Task 2", user_id=user.id)
        session.add_all([task1, task2])
        session.commit()

        # Create task for another user
        other_user = User(email="other@example.com", hashed_password="hash")
        session.add(other_user)
        session.commit()
        session.refresh(other_user)

        other_task = Task(title="Other Task", user_id=other_user.id)
        session.add(other_task)
        session.commit()

    # Get tasks with auth
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(task["user_id"] == user.id for task in data)

def test_create_task():
    """Test creating a new task"""
    with Session(engine) as session:
        user, token = create_test_user(session)

    response = client.post(
        "/api/tasks",
        json={"title": "New Task", "description": "Test description"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Test description"
    assert data["user_id"] == user.id
    assert data["is_completed"] is False

def test_create_task_validation():
    """Test task creation validation"""
    with Session(engine) as session:
        user, token = create_test_user(session)

    # Missing required field
    response = client.post(
        "/api/tasks",
        json={"description": "No title"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

def test_update_task():
    """Test updating a task"""
    with Session(engine) as session:
        user, token = create_test_user(session)
        task = Task(title="Original", user_id=user.id)
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "is_completed": True},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["is_completed"] is True

def test_update_other_user_task_forbidden():
    """Test that users cannot update other users' tasks"""
    with Session(engine) as session:
        user1, token1 = create_test_user(session)

        user2 = User(email="user2@example.com", hashed_password="hash")
        session.add(user2)
        session.commit()
        session.refresh(user2)

        task = Task(title="User 2 Task", user_id=user2.id)
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Hacked"},
        headers={"Authorization": f"Bearer {token1}"}
    )

    assert response.status_code == 403

def test_delete_task():
    """Test deleting a task"""
    with Session(engine) as session:
        user, token = create_test_user(session)
        task = Task(title="To Delete", user_id=user.id)
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify task is deleted
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
```

### Testing with Fixtures
```python
# tests/conftest.py
import pytest
from sqlmodel import Session, create_engine, SQLModel
from app.models.user import User
from app.models.task import Task
from app.utils.security import create_access_token

@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def test_user(session: Session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password="hashed_password"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def auth_token(test_user: User):
    """Create an auth token for test user"""
    return create_access_token({
        "sub": str(test_user.id),
        "email": test_user.email
    })

@pytest.fixture
def test_tasks(session: Session, test_user: User):
    """Create test tasks"""
    tasks = [
        Task(title="Task 1", user_id=test_user.id),
        Task(title="Task 2", user_id=test_user.id, is_completed=True),
        Task(title="Task 3", user_id=test_user.id),
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    return tasks

# Usage in tests
def test_with_fixtures(session, test_user, auth_token, test_tasks):
    """Test using fixtures"""
    assert test_user.email == "test@example.com"
    assert len(test_tasks) == 3
    assert auth_token is not None
```

## E2E Testing with Playwright

```typescript
// e2e/tasks.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });

  test('should display task list', async ({ page }) => {
    await page.goto('/tasks');

    await expect(page.locator('h1')).toContainText('Tasks');
    await expect(page.locator('[data-testid="task-item"]')).toHaveCount(3);
  });

  test('should create a new task', async ({ page }) => {
    await page.goto('/tasks');

    await page.fill('input[placeholder="New task"]', 'Buy groceries');
    await page.click('button:has-text("Add")');

    await expect(page.locator('text=Buy groceries')).toBeVisible();
  });

  test('should mark task as completed', async ({ page }) => {
    await page.goto('/tasks');

    const firstTask = page.locator('[data-testid="task-item"]').first();
    await firstTask.locator('input[type="checkbox"]').check();

    await expect(firstTask).toHaveClass(/completed/);
  });

  test('should delete a task', async ({ page }) => {
    await page.goto('/tasks');

    const taskCount = await page.locator('[data-testid="task-item"]').count();

    await page.locator('[data-testid="delete-button"]').first().click();
    await page.click('button:has-text("Confirm")');

    await expect(page.locator('[data-testid="task-item"]')).toHaveCount(taskCount - 1);
  });

  test('should filter completed tasks', async ({ page }) => {
    await page.goto('/tasks');

    await page.click('button:has-text("Completed")');

    const tasks = page.locator('[data-testid="task-item"]');
    await expect(tasks).toHaveCount(1);
    await expect(tasks.first()).toHaveClass(/completed/);
  });
});
```

## Test Coverage and Quality

### Running Tests with Coverage
```bash
# Frontend
npm run test -- --coverage

# Backend
pytest --cov=app --cov-report=html --cov-report=term
```

### Coverage Goals
- **Unit Tests**: 80%+ coverage for business logic
- **Integration Tests**: Cover critical user flows
- **E2E Tests**: Cover main user journeys
- **Edge Cases**: Test error conditions and boundaries

## Best Practices

### 1. Write Tests First (TDD)
```typescript
// 1. Write failing test
test('should calculate total price', () => {
  expect(calculateTotal([10, 20, 30])).toBe(60);
});

// 2. Implement minimal code to pass
function calculateTotal(prices: number[]): number {
  return prices.reduce((sum, price) => sum + price, 0);
}

// 3. Refactor if needed
```

### 2. Test Behavior, Not Implementation
```typescript
// BAD: Testing implementation details
test('should call setState with new value', () => {
  const setState = jest.fn();
  // Testing internal state management
});

// GOOD: Testing user-visible behavior
test('should display updated value when button is clicked', () => {
  render(<Counter />);
  fireEvent.click(screen.getByText('Increment'));
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

### 3. Keep Tests Independent
```typescript
// BAD: Tests depend on each other
let userId: number;

test('creates user', () => {
  userId = createUser();
});

test('updates user', () => {
  updateUser(userId); // Depends on previous test
});

// GOOD: Each test is independent
test('creates user', () => {
  const userId = createUser();
  expect(userId).toBeDefined();
});

test('updates user', () => {
  const userId = createUser(); // Create own test data
  updateUser(userId);
  expect(getUser(userId).updated).toBe(true);
});
```

## Anti-Patterns to Avoid

1. **Don't test implementation details**: Test user-visible behavior
2. **Don't write flaky tests**: Ensure tests are deterministic
3. **Don't skip edge cases**: Test error conditions and boundaries
4. **Don't mock everything**: Only mock external dependencies
5. **Don't write tests that are too complex**: Keep tests simple and readable
6. **Don't ignore failing tests**: Fix or remove broken tests
7. **Don't aim for 100% coverage**: Focus on meaningful coverage
8. **Don't test third-party libraries**: Trust they are tested
9. **Don't write slow tests**: Optimize test execution time
10. **Don't forget to test error cases**: Test both happy and sad paths

## Success Criteria

Your testing implementation is successful when:
- ✅ Critical user flows are covered by tests
- ✅ Tests are fast and reliable
- ✅ Tests catch bugs before production
- ✅ Code coverage is meaningful (not just high percentage)
- ✅ Tests are easy to understand and maintain
- ✅ CI/CD pipeline runs tests automatically
- ✅ Tests document expected behavior
- ✅ Edge cases and error conditions are tested
- ✅ Tests provide confidence for refactoring
- ✅ All acceptance criteria are verified by tests
