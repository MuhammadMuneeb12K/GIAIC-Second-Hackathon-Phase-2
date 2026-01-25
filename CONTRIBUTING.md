# Contributing to TaskFlow

First off, thank you for considering contributing to TaskFlow! It's people like you that make TaskFlow such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

---

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at conduct@taskflow.com. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 How Can I Contribute?

### 1. Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

**When reporting a bug, include:**
- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs **actual behavior**
- **Screenshots** (if applicable)
- **Environment details**:
  - OS (Windows, macOS, Linux)
  - Browser (Chrome, Firefox, Safari, etc.)
  - Node.js version
  - Python version
  - Any relevant package versions

**Example Bug Report:**
```markdown
**Title**: Task deletion fails with 500 error

**Description**: When attempting to delete a task, the API returns a 500 error.

**Steps to Reproduce**:
1. Log in to the application
2. Navigate to dashboard
3. Click delete button on any task
4. Observe error in console

**Expected**: Task should be deleted successfully
**Actual**: 500 Internal Server Error

**Environment**:
- OS: Windows 11
- Browser: Chrome 120
- Node.js: 18.17.0
- Python: 3.11.0

**Screenshots**: [Attach screenshot]
```

### 2. Suggesting Features

We love feature suggestions! Before creating a feature request:
- Check if the feature has already been suggested
- Consider if it fits the project's scope and goals

**When suggesting a feature, include:**
- **Clear title and description**
- **Use cases** - why is this feature needed?
- **Proposed solution** - how should it work?
- **Alternatives considered** - what other approaches did you think about?
- **Additional context** - mockups, examples, etc.

**Example Feature Request:**
```markdown
**Title**: Add task priority levels

**Description**: Allow users to set priority levels (High, Medium, Low) for tasks.

**Use Case**: Users need to prioritize their tasks to focus on what's most important.

**Proposed Solution**:
- Add a priority field to the task model
- Add a dropdown in the task form
- Display priority with color-coded badges
- Add filter by priority

**Alternatives**:
- Use tags instead of dedicated priority field
- Use due dates as implicit priority

**Mockup**: [Attach design mockup]
```

### 3. Contributing Code

We welcome code contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test your changes**
5. **Commit your changes** (see commit guidelines below)
6. **Push to your branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

---

## 💻 Development Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Git

### Setup Steps

1. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/taskflow.git
   cd taskflow
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/taskflow.git
   ```

3. **Setup backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Setup frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

5. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

---

## 📝 Coding Standards

### Frontend (TypeScript/React)

**Style Guide:**
- Use **TypeScript** for all new code
- Use **functional components** with hooks
- Use **named exports** for components
- Use **PascalCase** for component names
- Use **camelCase** for variables and functions
- Use **UPPER_CASE** for constants

**Example:**
```typescript
// Good
export const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = () => {
    setIsEditing(true);
  };

  return <div>{task.title}</div>;
};

// Bad
export default function taskItem(props) {
  var editing = false;
  return <div>{props.task.title}</div>;
}
```

**Best Practices:**
- ✅ Use TypeScript interfaces for props
- ✅ Add JSDoc comments for complex functions
- ✅ Use meaningful variable names
- ✅ Keep components small and focused
- ✅ Extract reusable logic into custom hooks
- ✅ Use proper error boundaries
- ✅ Add loading and error states

### Backend (Python/FastAPI)

**Style Guide:**
- Follow **PEP 8** style guide
- Use **snake_case** for variables and functions
- Use **PascalCase** for classes
- Use **UPPER_CASE** for constants
- Use **type hints** for all functions

**Example:**
```python
# Good
from typing import List
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

async def create_task(
    task_data: TaskCreate,
    current_user: User
) -> Task:
    """Create a new task for the current user."""
    task = Task(**task_data.dict(), user_id=current_user.id)
    db.add(task)
    await db.commit()
    return task

# Bad
def createTask(taskData, user):
    task = Task(title=taskData['title'], userId=user['id'])
    return task
```

**Best Practices:**
- ✅ Use type hints
- ✅ Add docstrings to functions
- ✅ Use Pydantic for validation
- ✅ Handle errors properly
- ✅ Use async/await for I/O operations
- ✅ Write unit tests

### General Guidelines

- **DRY (Don't Repeat Yourself)**: Extract common logic
- **KISS (Keep It Simple, Stupid)**: Prefer simple solutions
- **YAGNI (You Aren't Gonna Need It)**: Don't add unnecessary features
- **Single Responsibility**: Each function/component should do one thing
- **Meaningful Names**: Use descriptive names for variables and functions

---

## 📝 Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring (no functional changes)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, build, etc.)

### Examples

```bash
# Feature
git commit -m "feat(tasks): add priority field to tasks"

# Bug fix
git commit -m "fix(auth): resolve token refresh issue"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Refactoring
git commit -m "refactor(api): simplify task creation logic"

# Multiple lines
git commit -m "feat(dashboard): add statistics cards

- Add total tasks count
- Add completion rate
- Add pending tasks count
- Style cards with Tailwind

Closes #123"
```

### Commit Best Practices

- ✅ Use present tense ("add feature" not "added feature")
- ✅ Use imperative mood ("move cursor to..." not "moves cursor to...")
- ✅ Keep subject line under 50 characters
- ✅ Capitalize subject line
- ✅ Don't end subject line with a period
- ✅ Separate subject from body with a blank line
- ✅ Wrap body at 72 characters
- ✅ Reference issues and pull requests in the footer

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   # Frontend
   cd frontend && npm test

   # Backend
   cd backend && pytest
   ```

3. **Check code style**
   ```bash
   # Frontend
   npm run lint

   # Backend
   flake8 app/
   ```

4. **Build successfully**
   ```bash
   # Frontend
   npm run build

   # Backend
   # Ensure no import errors
   python -m app.main
   ```

### Pull Request Template

When creating a PR, use this template:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #123
Related to #456

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Screenshots (if applicable)
[Add screenshots here]

## Testing
- [ ] I have tested this locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **At least one maintainer** must approve
3. **All conversations** must be resolved
4. **No merge conflicts** with main branch

### After Approval

- Maintainers will merge your PR
- Your contribution will be credited in the release notes
- Thank you for contributing! 🎉

---

## 🧪 Testing Guidelines

### Frontend Tests

```typescript
// Example test
import { render, screen, fireEvent } from '@testing-library/react';
import TaskItem from './TaskItem';

describe('TaskItem', () => {
  it('should render task title', () => {
    const task = { id: '1', title: 'Test Task', completed: false };
    render(<TaskItem task={task} onEdit={jest.fn()} onDelete={jest.fn()} />);
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('should call onEdit when edit button is clicked', () => {
    const onEdit = jest.fn();
    const task = { id: '1', title: 'Test Task', completed: false };
    render(<TaskItem task={task} onEdit={onEdit} onDelete={jest.fn()} />);
    fireEvent.click(screen.getByText('Edit'));
    expect(onEdit).toHaveBeenCalledWith(task);
  });
});
```

### Backend Tests

```python
# Example test
import pytest
from app.models.task import Task

def test_create_task(client, auth_headers):
    """Test creating a new task."""
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"

def test_get_tasks(client, auth_headers):
    """Test getting all tasks."""
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🎯 Good First Issues

Looking for a place to start? Check out issues labeled with:
- `good first issue` - Perfect for newcomers
- `help wanted` - We need your help!
- `documentation` - Improve our docs

---

## 💬 Questions?

- **GitHub Discussions**: Ask questions and discuss ideas
- **Discord**: Join our community server (link in README)
- **Email**: contribute@taskflow.com

---

## 🙏 Thank You!

Your contributions make TaskFlow better for everyone. We appreciate your time and effort!

**Happy Coding! 🚀**
