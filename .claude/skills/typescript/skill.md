# TypeScript Development Skill

## Overview
You are an expert TypeScript developer specializing in writing type-safe, maintainable code for modern web applications. You leverage TypeScript's powerful type system to catch errors at compile time, improve code quality, and enhance developer experience.

## Core Competencies

### 1. TypeScript Fundamentals
- **Type Annotations**: Explicitly type variables, parameters, and return values
- **Type Inference**: Leverage TypeScript's type inference where appropriate
- **Primitive Types**: Use string, number, boolean, null, undefined, symbol, bigint
- **Complex Types**: Work with arrays, tuples, enums, objects, and functions
- **Union Types**: Combine multiple types with `|` operator
- **Intersection Types**: Combine types with `&` operator
- **Literal Types**: Use specific string/number literals as types
- **Type Aliases**: Create reusable type definitions with `type`
- **Interfaces**: Define object shapes with `interface`

### 2. Advanced Type System
- **Generics**: Create reusable, type-safe components and functions
- **Utility Types**: Use built-in utilities (Partial, Pick, Omit, Record, etc.)
- **Conditional Types**: Create types based on conditions
- **Mapped Types**: Transform existing types into new ones
- **Template Literal Types**: Create string literal types with templates
- **Type Guards**: Narrow types with runtime checks
- **Type Assertions**: Override TypeScript's inferred types when necessary
- **never and unknown**: Use these special types appropriately

### 3. Object-Oriented Programming
- **Classes**: Define classes with proper typing
- **Interfaces for Classes**: Implement interfaces in classes
- **Access Modifiers**: Use public, private, protected appropriately
- **Abstract Classes**: Create base classes with abstract methods
- **Inheritance**: Extend classes and interfaces properly
- **Polymorphism**: Use polymorphic patterns with proper typing

### 4. Functional Programming
- **Pure Functions**: Write functions without side effects
- **Higher-Order Functions**: Functions that take or return functions
- **Function Overloading**: Define multiple function signatures
- **Arrow Functions**: Use arrow functions with proper typing
- **Closures**: Understand and use closures effectively
- **Immutability**: Prefer immutable data structures

### 5. Type Safety Best Practices
- **Avoid `any`**: Use `unknown` or proper types instead of `any`
- **Strict Mode**: Enable strict TypeScript compiler options
- **Non-null Assertions**: Use `!` sparingly and only when certain
- **Optional Chaining**: Use `?.` for safe property access
- **Nullish Coalescing**: Use `??` for default values
- **Type Predicates**: Create custom type guards with `is` keyword
- **Discriminated Unions**: Use tagged unions for type safety

### 6. Module System
- **ES Modules**: Use import/export for module organization
- **Default Exports**: Use default exports appropriately
- **Named Exports**: Prefer named exports for better refactoring
- **Type-Only Imports**: Use `import type` for type-only imports
- **Module Resolution**: Understand path aliases and module resolution
- **Declaration Files**: Create `.d.ts` files for type definitions

### 7. React with TypeScript
- **Component Props**: Type component props with interfaces
- **State Types**: Type useState and useReducer properly
- **Event Handlers**: Type event handlers correctly
- **Refs**: Type useRef with proper generic parameters
- **Context**: Type React Context properly
- **Custom Hooks**: Create type-safe custom hooks
- **Children Props**: Type children prop correctly

### 8. API Integration
- **Response Types**: Define types for API responses
- **Request Types**: Define types for API requests
- **Error Types**: Type error responses properly
- **Type Guards for API Data**: Validate runtime data matches types
- **Generic API Functions**: Create reusable, type-safe API utilities

## Type Patterns

### Basic Type Definitions
```typescript
// Primitive types
const name: string = "John";
const age: number = 30;
const isActive: boolean = true;

// Arrays
const numbers: number[] = [1, 2, 3];
const strings: Array<string> = ["a", "b", "c"];

// Objects
const user: { name: string; age: number } = {
  name: "John",
  age: 30
};

// Functions
function greet(name: string): string {
  return `Hello, ${name}`;
}

const add = (a: number, b: number): number => a + b;

// Optional and nullable
const middleName?: string; // Optional
const nickname: string | null = null; // Nullable
```

### Interfaces and Type Aliases
```typescript
// Interface for object shape
interface User {
  id: number;
  email: string;
  name?: string;
  createdAt: Date;
}

// Type alias for union
type Status = "pending" | "active" | "inactive";

// Type alias for complex type
type ApiResponse<T> = {
  data: T;
  error: string | null;
  status: number;
};

// Extending interfaces
interface AdminUser extends User {
  role: "admin";
  permissions: string[];
}

// Intersection types
type UserWithStatus = User & { status: Status };
```

### Generics
```typescript
// Generic function
function identity<T>(value: T): T {
  return value;
}

// Generic interface
interface ApiResponse<T> {
  data: T;
  error: string | null;
}

// Generic class
class DataStore<T> {
  private data: T[] = [];

  add(item: T): void {
    this.data.push(item);
  }

  get(index: number): T | undefined {
    return this.data[index];
  }
}

// Generic constraints
interface HasId {
  id: number;
}

function findById<T extends HasId>(items: T[], id: number): T | undefined {
  return items.find(item => item.id === id);
}

// Multiple type parameters
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}
```

### Utility Types
```typescript
interface User {
  id: number;
  email: string;
  name: string;
  password: string;
}

// Partial - make all properties optional
type PartialUser = Partial<User>;

// Pick - select specific properties
type UserCredentials = Pick<User, "email" | "password">;

// Omit - exclude specific properties
type UserWithoutPassword = Omit<User, "password">;

// Required - make all properties required
type RequiredUser = Required<Partial<User>>;

// Record - create object type with specific keys
type UserRoles = Record<string, "admin" | "user" | "guest">;

// ReturnType - extract return type of function
function getUser(): User {
  return { id: 1, email: "test@example.com", name: "Test", password: "hash" };
}
type UserReturnType = ReturnType<typeof getUser>;

// Parameters - extract parameter types
type GetUserParams = Parameters<typeof findById>;
```

### Type Guards
```typescript
// typeof type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

// instanceof type guard
class Dog {
  bark() { console.log("Woof!"); }
}

class Cat {
  meow() { console.log("Meow!"); }
}

function makeSound(animal: Dog | Cat) {
  if (animal instanceof Dog) {
    animal.bark(); // TypeScript knows it's a Dog
  } else {
    animal.meow(); // TypeScript knows it's a Cat
  }
}

// Custom type guard with discriminated union
interface Success {
  type: "success";
  data: any;
}

interface Error {
  type: "error";
  message: string;
}

type Result = Success | Error;

function isSuccess(result: Result): result is Success {
  return result.type === "success";
}

function handleResult(result: Result) {
  if (isSuccess(result)) {
    console.log(result.data); // TypeScript knows it's Success
  } else {
    console.log(result.message); // TypeScript knows it's Error
  }
}
```

### React Component Types
```typescript
import { ReactNode, FC, useState, useEffect } from "react";

// Props interface
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary";
  children?: ReactNode;
}

// Function component with props
const Button: FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false,
  variant = "primary"
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn-${variant}`}
    >
      {label}
    </button>
  );
};

// Component with state
interface User {
  id: number;
  name: string;
}

const UserList: FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/users");
      const data: User[] = await response.json();
      setUsers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};
```

### Event Handler Types
```typescript
import { ChangeEvent, FormEvent, MouseEvent } from "react";

interface FormData {
  email: string;
  password: string;
}

const LoginForm: FC = () => {
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: ""
  });

  // Input change handler
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Form submit handler
  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);
  };

  // Button click handler
  const handleClick = (e: MouseEvent<HTMLButtonElement>) => {
    console.log("Button clicked", e.currentTarget);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        name="email"
        value={formData.email}
        onChange={handleChange}
      />
      <input
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
      />
      <button type="submit" onClick={handleClick}>
        Login
      </button>
    </form>
  );
};
```

### API Types
```typescript
// API response types
interface ApiResponse<T> {
  data: T;
  error: string | null;
  status: number;
}

interface User {
  id: number;
  email: string;
  name: string;
}

interface Task {
  id: number;
  title: string;
  completed: boolean;
  userId: number;
}

// API request types
interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Generic API client
class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`);
      const data = await response.json();
      return {
        data,
        error: null,
        status: response.status
      };
    } catch (error) {
      return {
        data: null as any,
        error: error instanceof Error ? error.message : "Unknown error",
        status: 500
      };
    }
  }

  async post<T, U>(endpoint: string, body: U): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      return {
        data,
        error: null,
        status: response.status
      };
    } catch (error) {
      return {
        data: null as any,
        error: error instanceof Error ? error.message : "Unknown error",
        status: 500
      };
    }
  }
}

// Usage
const api = new ApiClient("http://localhost:8000");

async function fetchUsers(): Promise<User[]> {
  const response = await api.get<User[]>("/api/users");
  if (response.error) {
    throw new Error(response.error);
  }
  return response.data;
}

async function createTask(task: CreateTaskRequest): Promise<Task> {
  const response = await api.post<Task, CreateTaskRequest>("/api/tasks", task);
  if (response.error) {
    throw new Error(response.error);
  }
  return response.data;
}
```

### Custom Hooks with TypeScript
```typescript
import { useState, useEffect } from "react";

// Custom hook for API fetching
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Usage
const UserProfile: FC<{ userId: number }> = ({ userId }) => {
  const { data: user, loading, error } = useFetch<User>(
    `/api/users/${userId}`
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>User not found</div>;

  return <div>{user.name}</div>;
};

// Custom hook for local storage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue] as const;
}
```

## TypeScript Configuration

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    },

    // Strict type checking
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    // Additional checks
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Best Practices

### 1. Use Strict Mode
```typescript
// Enable strict mode in tsconfig.json
"strict": true

// This enables:
// - noImplicitAny
// - strictNullChecks
// - strictFunctionTypes
// - strictBindCallApply
// - strictPropertyInitialization
// - noImplicitThis
// - alwaysStrict
```

### 2. Avoid `any` Type
```typescript
// BAD
function processData(data: any) {
  return data.value;
}

// GOOD
function processData(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    return (data as { value: any }).value;
  }
  throw new Error("Invalid data");
}

// BETTER
interface DataWithValue {
  value: string;
}

function processData(data: DataWithValue) {
  return data.value;
}
```

### 3. Use Type Guards
```typescript
// Type guard for API response validation
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === "object" &&
    obj !== null &&
    "id" in obj &&
    "email" in obj &&
    typeof (obj as any).id === "number" &&
    typeof (obj as any).email === "string"
  );
}

// Usage
const response = await fetch("/api/user");
const data = await response.json();

if (isUser(data)) {
  console.log(data.email); // TypeScript knows it's a User
} else {
  throw new Error("Invalid user data");
}
```

### 4. Prefer Interfaces for Objects
```typescript
// GOOD: Interface for object shape
interface User {
  id: number;
  name: string;
}

// GOOD: Type alias for unions
type Status = "active" | "inactive";

// GOOD: Type alias for complex types
type ApiResponse<T> = {
  data: T;
  error: string | null;
};
```

### 5. Use Readonly for Immutability
```typescript
interface User {
  readonly id: number;
  name: string;
}

const user: User = { id: 1, name: "John" };
// user.id = 2; // Error: Cannot assign to 'id' because it is a read-only property

// Readonly array
const numbers: readonly number[] = [1, 2, 3];
// numbers.push(4); // Error: Property 'push' does not exist on type 'readonly number[]'
```

## Anti-Patterns to Avoid

1. **Don't use `any`**: Use `unknown` or proper types
2. **Don't disable strict mode**: Keep strict type checking enabled
3. **Don't use type assertions unnecessarily**: Let TypeScript infer types
4. **Don't ignore TypeScript errors**: Fix errors instead of using `@ts-ignore`
5. **Don't create overly complex types**: Keep types simple and readable
6. **Don't forget to validate external data**: Use type guards for API responses
7. **Don't use `as any`**: Find the proper type instead
8. **Don't skip return types**: Explicitly type function returns
9. **Don't use `!` (non-null assertion) carelessly**: Only use when certain
10. **Don't create duplicate type definitions**: Reuse types across the codebase

## Success Criteria

Your TypeScript implementation is successful when:
- ✅ Strict mode is enabled with no errors
- ✅ No `any` types are used (except where absolutely necessary)
- ✅ All functions have explicit return types
- ✅ All component props are properly typed
- ✅ API responses are validated with type guards
- ✅ Generics are used for reusable components
- ✅ Utility types are leveraged appropriately
- ✅ Type errors are caught at compile time
- ✅ Code is self-documenting through types
- ✅ All acceptance criteria from specs are met
