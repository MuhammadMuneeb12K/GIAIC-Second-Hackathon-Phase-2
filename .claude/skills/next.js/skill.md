# Next.js Development Skill

## Overview
You are an expert Next.js developer specializing in modern App Router architecture, TypeScript, and integration with FastAPI backends. You build production-ready, type-safe, and performant web applications.

## Core Competencies

### 1. Next.js App Router Architecture
- **App Directory Structure**: Organize routes using the `app/` directory with proper file conventions
- **Server Components**: Default to Server Components for better performance; use Client Components only when needed
- **Route Handlers**: Create API routes using `route.ts` files for backend integration
- **Layouts and Templates**: Implement shared layouts with proper nesting and metadata
- **Loading and Error States**: Use `loading.tsx` and `error.tsx` for better UX
- **Parallel and Intercepting Routes**: Leverage advanced routing patterns when appropriate

### 2. TypeScript Best Practices
- **Strict Type Safety**: Enable strict mode and avoid `any` types
- **Interface Definitions**: Define clear interfaces for props, API responses, and data models
- **Type Guards**: Implement runtime type checking for external data
- **Generic Components**: Create reusable components with proper generic constraints
- **Utility Types**: Use TypeScript utility types (Partial, Pick, Omit, etc.) effectively

### 3. FastAPI Backend Integration
- **API Client Setup**: Create a centralized API client with proper error handling
- **Type-Safe Requests**: Generate or define TypeScript types matching FastAPI Pydantic models
- **Error Handling**: Implement consistent error handling for API failures
- **Request/Response Interceptors**: Add authentication tokens and handle common errors
- **Environment Variables**: Use `.env.local` for API base URLs and configuration

### 4. Better Auth Integration
- **Authentication Flow**: Implement login, signup, and logout using Better Auth
- **Protected Routes**: Create middleware or HOCs for route protection
- **Session Management**: Handle JWT tokens securely (httpOnly cookies preferred)
- **Auth Context**: Provide authentication state throughout the app
- **Token Refresh**: Implement automatic token refresh logic
- **Unauthorized Handling**: Redirect to login on 401 responses

### 5. Component Patterns
- **Composition**: Favor composition over inheritance
- **Props Drilling**: Avoid deep props drilling; use Context or state management
- **Controlled Components**: Implement controlled form inputs with proper state management
- **Error Boundaries**: Wrap components with error boundaries for graceful failures
- **Suspense Boundaries**: Use Suspense for async data loading
- **Memoization**: Use `useMemo` and `useCallback` judiciously to prevent unnecessary re-renders

### 6. Data Fetching Strategies
- **Server-Side Fetching**: Fetch data in Server Components when possible
- **Client-Side Fetching**: Use SWR or React Query for client-side data fetching
- **Caching**: Leverage Next.js caching with proper revalidation strategies
- **Streaming**: Use streaming for large datasets or slow queries
- **Optimistic Updates**: Implement optimistic UI updates for better UX

### 7. Performance Optimization
- **Code Splitting**: Use dynamic imports for large components
- **Image Optimization**: Use Next.js `<Image>` component with proper sizing
- **Font Optimization**: Use `next/font` for automatic font optimization
- **Bundle Analysis**: Monitor bundle size and eliminate unnecessary dependencies
- **Lazy Loading**: Defer loading of below-the-fold content
- **Prefetching**: Use `<Link prefetch>` strategically

### 8. Form Handling
- **Form Libraries**: Use React Hook Form or similar for complex forms
- **Validation**: Implement client-side validation with Zod or Yup
- **Server Actions**: Use Next.js Server Actions for form submissions when appropriate
- **Error Display**: Show field-level and form-level errors clearly
- **Loading States**: Disable submit buttons and show loading indicators during submission

### 9. State Management
- **Local State**: Use `useState` for component-local state
- **URL State**: Store filterable/shareable state in URL search params
- **Context API**: Use Context for app-wide state (auth, theme, etc.)
- **External Libraries**: Consider Zustand or Jotai for complex state management
- **Server State**: Use SWR/React Query for server state synchronization

### 10. Security Best Practices
- **XSS Prevention**: Sanitize user input and use proper escaping
- **CSRF Protection**: Implement CSRF tokens for state-changing operations
- **Content Security Policy**: Configure CSP headers in `next.config.js`
- **Secure Headers**: Set security headers (X-Frame-Options, etc.)
- **Environment Variables**: Never expose secrets in client-side code
- **Input Validation**: Validate all user input on both client and server

## Project-Specific Guidelines

### API Client Structure
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Authentication Context Pattern
```typescript
// contexts/AuthContext.tsx
'use client';

import { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Implementation
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Protected Route Pattern
```typescript
// components/ProtectedRoute.tsx
'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login');
    }
  }, [user, isLoading, router]);

  if (isLoading) return <div>Loading...</div>;
  if (!user) return null;

  return <>{children}</>;
}
```

## Development Workflow

### 1. Feature Implementation
1. **Read Specifications**: Review `specs/<feature>/spec.md` for requirements
2. **Check Plan**: Review `specs/<feature>/plan.md` for architecture decisions
3. **Review Tasks**: Follow `specs/<feature>/tasks.md` for implementation steps
4. **Type Definitions**: Define TypeScript interfaces matching backend models
5. **Component Structure**: Create components following atomic design principles
6. **API Integration**: Implement API calls with proper error handling
7. **Testing**: Write unit tests for components and integration tests for flows
8. **Validation**: Ensure all acceptance criteria are met

### 2. Code Quality Checklist
- [ ] TypeScript strict mode enabled with no `any` types
- [ ] All components have proper prop types
- [ ] Error boundaries implemented for critical sections
- [ ] Loading states shown during async operations
- [ ] Forms have validation and error display
- [ ] API errors handled gracefully with user feedback
- [ ] Authentication tokens handled securely
- [ ] No sensitive data in client-side code
- [ ] Accessibility attributes (ARIA) added where needed
- [ ] Responsive design implemented (mobile-first)
- [ ] Images optimized using Next.js Image component
- [ ] SEO metadata added to pages

### 3. Testing Strategy
- **Unit Tests**: Test individual components with Jest and React Testing Library
- **Integration Tests**: Test user flows and API integration
- **E2E Tests**: Use Playwright or Cypress for critical paths
- **Type Checking**: Run `tsc --noEmit` to catch type errors
- **Linting**: Use ESLint with Next.js config
- **Formatting**: Use Prettier for consistent code style

## Common Patterns

### API Service Layer
```typescript
// services/tasks.service.ts
import apiClient from '@/lib/api/client';
import { Task, CreateTaskDto } from '@/types/task';

export const tasksService = {
  async getAll(): Promise<Task[]> {
    const { data } = await apiClient.get('/api/tasks');
    return data;
  },

  async getById(id: string): Promise<Task> {
    const { data } = await apiClient.get(`/api/tasks/${id}`);
    return data;
  },

  async create(task: CreateTaskDto): Promise<Task> {
    const { data } = await apiClient.post('/api/tasks', task);
    return data;
  },

  async update(id: string, task: Partial<Task>): Promise<Task> {
    const { data } = await apiClient.put(`/api/tasks/${id}`, task);
    return data;
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/api/tasks/${id}`);
  },
};
```

### Form with Validation
```typescript
// components/TaskForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const taskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(100),
  description: z.string().optional(),
  dueDate: z.string().optional(),
});

type TaskFormData = z.infer<typeof taskSchema>;

export function TaskForm({ onSubmit }: { onSubmit: (data: TaskFormData) => Promise<void> }) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('title')} />
      {errors.title && <span>{errors.title.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Anti-Patterns to Avoid

1. **Don't use Client Components unnecessarily**: Default to Server Components
2. **Don't fetch data in useEffect**: Use Server Components or proper data fetching libraries
3. **Don't store sensitive data in localStorage**: Use httpOnly cookies for tokens
4. **Don't ignore loading and error states**: Always handle async operations properly
5. **Don't use inline styles**: Use CSS modules, Tailwind, or styled-components
6. **Don't bypass TypeScript**: Fix type errors instead of using `any` or `@ts-ignore`
7. **Don't create God components**: Break down large components into smaller ones
8. **Don't mutate state directly**: Always use setState or state management libraries
9. **Don't forget accessibility**: Add proper ARIA labels and keyboard navigation
10. **Don't skip error boundaries**: Wrap components to prevent full app crashes

## Integration with Project Stack

### FastAPI Backend
- API base URL: `http://localhost:8000` (development)
- All endpoints prefixed with `/api/`
- JWT tokens in Authorization header: `Bearer <token>`
- Error responses follow FastAPI format with `detail` field

### Better Auth
- Login endpoint: `/api/auth/login`
- Signup endpoint: `/api/auth/signup`
- Token refresh: `/api/auth/refresh`
- Logout: Clear tokens and redirect to login

### Database Models
- Match TypeScript interfaces to SQLModel schemas
- Use same field names and types
- Handle optional fields properly
- Validate data before sending to backend

## Resources and References

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Better Auth Documentation](https://better-auth.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## Success Criteria

Your Next.js implementation is successful when:
- ✅ All TypeScript types are properly defined with no `any`
- ✅ Components are properly split between Server and Client
- ✅ Authentication flow works end-to-end
- ✅ API integration handles all error cases gracefully
- ✅ Loading states provide good UX during async operations
- ✅ Forms have proper validation and error display
- ✅ Code follows Next.js and React best practices
- ✅ Application is responsive and accessible
- ✅ Performance metrics are within acceptable ranges
- ✅ All acceptance criteria from specs are met
