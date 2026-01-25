# Skills Documentation

This directory contains comprehensive skill documentation for all major technologies and practices used in this hackathon project. Each skill file provides expert-level guidance, patterns, best practices, and examples.

## Available Skills

### Frontend Development
- **[Next.js](./next.js/skill.md)** - Modern App Router architecture, Server/Client Components, TypeScript integration, and FastAPI backend integration
- **[TypeScript](./typescript/skill.md)** - Type-safe development, advanced type system, React integration, and API type definitions

### Backend Development
- **[FastAPI](./fastapi/skill.md)** - REST API development, dependency injection, authentication, and database integration
- **[SQLModel](./sqlmodel/skill.md)** - Database schema design, ORM patterns, query optimization, and user isolation

### Authentication & Security
- **[Better Auth](./better-auth/skill.md)** - JWT authentication, token management, session handling, and security best practices

### Development Practices
- **[Testing](./testing/skill.md)** - Unit testing, integration testing, E2E testing with Jest, pytest, and Playwright
- **[Git Workflow](./git-workflow/skill.md)** - Version control, branching strategies, commit conventions, and pull request best practices
- **[API Design](./api-design/skill.md)** - RESTful API design, URL patterns, error handling, and documentation

## How to Use These Skills

### For Development
When working on a specific technology, refer to the relevant skill file for:
- **Patterns and Examples**: Copy-paste ready code patterns
- **Best Practices**: Industry-standard approaches
- **Anti-Patterns**: Common mistakes to avoid
- **Troubleshooting**: Solutions to common problems

### For Code Review
Use skill files as a reference when reviewing code:
- Check if code follows documented patterns
- Verify best practices are being followed
- Ensure anti-patterns are avoided
- Validate security practices

### For Learning
Each skill file is structured as a comprehensive guide:
1. **Core Competencies**: What you should know
2. **Patterns**: How to implement features
3. **Best Practices**: What to do
4. **Anti-Patterns**: What to avoid
5. **Success Criteria**: How to measure quality

## Skill File Structure

Each skill file follows this structure:

```markdown
# Technology Name Skill

## Overview
Brief description of the technology and expertise level

## Core Competencies
Key areas of knowledge and skills

## Implementation Patterns
Code examples and patterns for common tasks

## Best Practices
Recommended approaches and guidelines

## Anti-Patterns to Avoid
Common mistakes and what not to do

## Success Criteria
How to know your implementation is successful
```

## Quick Reference by Task

### Starting a New Feature
1. Read **[API Design](./api-design/skill.md)** for endpoint design
2. Review **[SQLModel](./sqlmodel/skill.md)** for database schema
3. Check **[FastAPI](./fastapi/skill.md)** for backend implementation
4. Reference **[Next.js](./next.js/skill.md)** for frontend components
5. Follow **[Git Workflow](./git-workflow/skill.md)** for version control

### Implementing Authentication
1. **[Better Auth](./better-auth/skill.md)** - Complete auth implementation guide
2. **[FastAPI](./fastapi/skill.md)** - Backend auth endpoints
3. **[Next.js](./next.js/skill.md)** - Frontend auth context and protected routes
4. **[TypeScript](./typescript/skill.md)** - Type-safe auth types

### Writing Tests
1. **[Testing](./testing/skill.md)** - Comprehensive testing guide
2. **[FastAPI](./fastapi/skill.md)** - Backend testing patterns
3. **[Next.js](./next.js/skill.md)** - Frontend testing with React Testing Library

### Database Operations
1. **[SQLModel](./sqlmodel/skill.md)** - Schema design and queries
2. **[FastAPI](./fastapi/skill.md)** - Database integration
3. **[TypeScript](./typescript/skill.md)** - Type definitions for models

### API Development
1. **[API Design](./api-design/skill.md)** - RESTful design principles
2. **[FastAPI](./fastapi/skill.md)** - Implementation patterns
3. **[TypeScript](./typescript/skill.md)** - API client types

## Technology Stack Overview

This project uses a modern full-stack architecture:

### Frontend
- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **React** for UI components
- **Better Auth** for authentication

### Backend
- **FastAPI** for REST API
- **SQLModel** for database ORM
- **Python 3.10+** for backend logic
- **JWT** for authentication tokens

### Database
- **PostgreSQL** (production) or **SQLite** (development)
- **SQLModel** for type-safe database operations

### Development Tools
- **Git** for version control
- **pytest** for backend testing
- **Jest/Vitest** for frontend testing
- **Playwright** for E2E testing

## Best Practices Summary

### Code Quality
- ✅ Write type-safe code (TypeScript strict mode, Python type hints)
- ✅ Follow consistent naming conventions
- ✅ Keep functions small and focused
- ✅ Write self-documenting code
- ✅ Add comments only for complex logic

### Security
- ✅ Never commit secrets or credentials
- ✅ Validate all user input
- ✅ Implement proper authentication and authorization
- ✅ Use parameterized queries (SQLModel handles this)
- ✅ Enforce user data isolation

### Testing
- ✅ Write tests for critical functionality
- ✅ Test both happy and error paths
- ✅ Keep tests independent and isolated
- ✅ Use meaningful test names
- ✅ Aim for meaningful coverage, not just high percentages

### Git Workflow
- ✅ Write clear, descriptive commit messages
- ✅ Create feature branches for new work
- ✅ Keep commits atomic and focused
- ✅ Review your own code before creating PRs
- ✅ Respond to PR feedback promptly

### API Design
- ✅ Follow RESTful conventions
- ✅ Use appropriate HTTP methods and status codes
- ✅ Provide clear error messages
- ✅ Document all endpoints
- ✅ Implement pagination for lists

## Common Patterns

### User Isolation Pattern
All user-specific data must be filtered by `user_id`:

```python
# Backend (FastAPI + SQLModel)
statement = select(Task).where(Task.user_id == current_user.id)
tasks = session.exec(statement).all()
```

```typescript
// Frontend (Next.js + TypeScript)
const tasks = await api.get<Task[]>('/api/tasks');
// API automatically filters by authenticated user
```

### Authentication Pattern
JWT tokens are used for authentication:

```typescript
// Frontend: Token in Authorization header
headers: {
  'Authorization': `Bearer ${accessToken}`
}
```

```python
# Backend: Extract user from token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    user = session.get(User, payload["sub"])
    return user
```

### Error Handling Pattern
Consistent error responses across the API:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues

#### TypeScript Errors
- Check **[TypeScript](./typescript/skill.md)** for type definitions
- Ensure strict mode is enabled
- Avoid using `any` type

#### Authentication Issues
- Review **[Better Auth](./better-auth/skill.md)** for token handling
- Check token expiration and refresh logic
- Verify CORS configuration

#### Database Errors
- Consult **[SQLModel](./sqlmodel/skill.md)** for query patterns
- Ensure user isolation is implemented
- Check foreign key relationships

#### API Errors
- Reference **[API Design](./api-design/skill.md)** for proper patterns
- Verify HTTP methods and status codes
- Check request/response formats

## Contributing to Skills

When you discover new patterns or best practices:

1. Update the relevant skill file
2. Add code examples
3. Document the pattern clearly
4. Include both good and bad examples
5. Update this README if adding new skills

## Resources

### Official Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Better Auth Documentation](https://better-auth.com)

### Testing Resources
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro)
- [pytest Documentation](https://docs.pytest.org)
- [Playwright Documentation](https://playwright.dev)

### Git Resources
- [Git Documentation](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org)
- [GitHub Flow](https://guides.github.com/introduction/flow)

## Success Metrics

Your implementation is successful when:

- ✅ Code follows patterns documented in skill files
- ✅ All tests pass (unit, integration, E2E)
- ✅ TypeScript compiles with no errors (strict mode)
- ✅ API follows RESTful conventions
- ✅ Authentication and authorization work correctly
- ✅ User data isolation is enforced
- ✅ Code is well-documented and maintainable
- ✅ Git history is clean and meaningful
- ✅ No security vulnerabilities
- ✅ Performance is acceptable

## Getting Help

1. **Check the relevant skill file** for patterns and examples
2. **Search for similar patterns** in the codebase
3. **Review the official documentation** for the technology
4. **Ask specific questions** with context and code examples
5. **Share error messages** and what you've tried

## Next Steps

1. **Familiarize yourself** with the skill files relevant to your work
2. **Bookmark frequently used patterns** for quick reference
3. **Follow the best practices** outlined in each skill
4. **Avoid the anti-patterns** documented in each skill
5. **Update skills** as you learn new patterns

---

**Remember**: These skills are living documents. Update them as you discover better patterns and practices!
