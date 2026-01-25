# Better Auth Integration Skill

## Overview
You are an expert in implementing secure authentication systems using Better Auth. You specialize in integrating Better Auth with Next.js frontends and FastAPI backends, ensuring secure token management, session handling, and user authentication flows.

## Core Competencies

### 1. Better Auth Fundamentals
- **Authentication Flow**: Understand the complete auth flow from login to token refresh
- **JWT Tokens**: Work with access tokens and refresh tokens
- **Token Storage**: Implement secure token storage strategies
- **Session Management**: Handle user sessions across frontend and backend
- **Token Refresh**: Implement automatic token refresh logic
- **Logout Flow**: Properly clear tokens and invalidate sessions

### 2. Frontend Integration (Next.js)
- **Auth Context**: Create React Context for authentication state
- **Auth Provider**: Wrap application with authentication provider
- **Protected Routes**: Implement route protection with redirects
- **Login/Signup Forms**: Build authentication forms with validation
- **Token Interceptors**: Add tokens to API requests automatically
- **Unauthorized Handling**: Redirect to login on 401 responses

### 3. Backend Integration (FastAPI)
- **Token Generation**: Create JWT tokens with proper claims
- **Token Verification**: Validate tokens on protected endpoints
- **Password Hashing**: Securely hash and verify passwords
- **User Registration**: Implement signup with validation
- **Login Endpoint**: Authenticate users and return tokens
- **Refresh Endpoint**: Exchange refresh tokens for new access tokens

### 4. Security Best Practices
- **httpOnly Cookies**: Store tokens in httpOnly cookies when possible
- **CSRF Protection**: Implement CSRF tokens for cookie-based auth
- **Token Expiration**: Set appropriate expiration times
- **Secure Transmission**: Always use HTTPS in production
- **Password Requirements**: Enforce strong password policies
- **Rate Limiting**: Prevent brute force attacks on auth endpoints

### 5. Token Management
- **Access Token**: Short-lived token for API requests (15-30 minutes)
- **Refresh Token**: Long-lived token for getting new access tokens (7-30 days)
- **Token Payload**: Include user ID, email, and roles in JWT claims
- **Token Blacklisting**: Implement token revocation for logout
- **Token Rotation**: Rotate refresh tokens on use for better security

## Implementation Patterns

### Frontend Auth Context
```typescript
// contexts/AuthContext.tsx
'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/api/client';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check for existing session on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        // Verify token and get user info
        const response = await apiClient.get('/api/auth/me');
        setUser(response.data);
      }
    } catch (error) {
      // Token invalid or expired, try refresh
      await refreshToken();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.post('/api/auth/login', {
        email,
        password,
      });

      const { access_token, refresh_token, user: userData } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      setUser(userData);
      router.push('/dashboard');
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const signup = async (email: string, password: string, name?: string) => {
    try {
      const response = await apiClient.post('/api/auth/signup', {
        email,
        password,
        name,
      });

      const { access_token, refresh_token, user: userData } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      setUser(userData);
      router.push('/dashboard');
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Signup failed');
    }
  };

  const logout = async () => {
    try {
      await apiClient.post('/api/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      router.push('/login');
    }
  };

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) throw new Error('No refresh token');

      const response = await apiClient.post('/api/auth/refresh', {
        refresh_token: refresh,
      });

      const { access_token, refresh_token: newRefreshToken } = response.data;

      localStorage.setItem('access_token', access_token);
      if (newRefreshToken) {
        localStorage.setItem('refresh_token', newRefreshToken);
      }

      // Get updated user info
      const userResponse = await apiClient.get('/api/auth/me');
      setUser(userResponse.data);
    } catch (error) {
      // Refresh failed, clear tokens and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      router.push('/login');
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, isLoading, login, signup, logout, refreshToken }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### API Client with Token Interceptors
```typescript
// lib/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and we haven't retried yet, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token');
        }

        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/auth/refresh`,
          { refresh_token: refreshToken }
        );

        const { access_token, refresh_token: newRefreshToken } = response.data;

        localStorage.setItem('access_token', access_token);
        if (newRefreshToken) {
          localStorage.setItem('refresh_token', newRefreshToken);
        }

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

### Backend Auth Endpoints (FastAPI)
```python
# app/routers/auth.py
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    UserResponse
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)

router = APIRouter()
security = HTTPBearer()

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(
    signup_data: SignupRequest,
    session: Session = Depends(get_session)
):
    """Register a new user"""
    # Check if user already exists
    statement = select(User).where(User.email == signup_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(signup_data.password)
    user = User(
        email=signup_data.email,
        name=signup_data.name,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate tokens
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """Authenticate user and return tokens"""
    # Find user by email
    statement = select(User).where(User.email == login_data.email)
    user = session.exec(statement).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Generate tokens
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_data: RefreshRequest):
    """Exchange refresh token for new access token"""
    payload = verify_token(refresh_data.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user_id = payload.get("sub")

    # Generate new tokens
    access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information"""
    return UserResponse.from_orm(current_user)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should clear tokens)"""
    # In a production system, you might want to blacklist the token here
    return None
```

### Security Utilities
```python
# app/utils/security.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
```

## Protected Route Component
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

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null;
  }

  return <>{children}</>;
}
```

## Login Form Example
```typescript
// app/login/page.tsx
'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Login</h1>

      {error && <div className="error">{error}</div>}

      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />

      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

## Security Checklist

- [ ] Passwords are hashed with bcrypt or argon2
- [ ] JWT tokens have appropriate expiration times
- [ ] Refresh tokens are stored securely
- [ ] HTTPS is enforced in production
- [ ] CORS is configured correctly
- [ ] Rate limiting is implemented on auth endpoints
- [ ] Password requirements are enforced (min length, complexity)
- [ ] Failed login attempts are logged
- [ ] Tokens are validated on every protected endpoint
- [ ] User sessions can be invalidated (logout)
- [ ] Sensitive data is never logged
- [ ] Token secrets are stored in environment variables

## Anti-Patterns to Avoid

1. **Don't store tokens in localStorage without consideration**: Use httpOnly cookies when possible
2. **Don't use weak JWT secrets**: Use strong, random secrets
3. **Don't skip token expiration**: Always set expiration times
4. **Don't expose password hashes**: Never return hashed passwords in API responses
5. **Don't trust client-side validation alone**: Always validate on the backend
6. **Don't use GET requests for authentication**: Use POST for login/signup
7. **Don't store passwords in plain text**: Always hash passwords
8. **Don't skip HTTPS in production**: Always use secure connections
9. **Don't ignore token refresh**: Implement automatic token refresh
10. **Don't forget to handle logout**: Clear tokens and invalidate sessions

## Success Criteria

Your Better Auth implementation is successful when:
- ✅ Users can sign up with email and password
- ✅ Users can log in and receive JWT tokens
- ✅ Tokens are automatically added to API requests
- ✅ Protected routes redirect unauthenticated users to login
- ✅ Token refresh works automatically when access token expires
- ✅ Users can log out and tokens are cleared
- ✅ Passwords are securely hashed
- ✅ User data isolation is enforced
- ✅ Authentication errors are handled gracefully
- ✅ All security best practices are followed
