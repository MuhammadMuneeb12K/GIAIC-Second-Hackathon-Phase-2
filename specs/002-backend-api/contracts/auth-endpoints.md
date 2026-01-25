# API Contract: Authentication Endpoints

**Feature**: Backend API for Multi-User Todo Application
**Domain**: Authentication
**Base Path**: `/api/auth`
**Date**: 2026-01-11

## Overview

This contract defines all authentication-related endpoints for user registration, login, token management, and logout. All endpoints follow RESTful conventions and return JSON responses.

---

## Endpoint: POST /api/auth/signup

### Description

Creates a new user account with email, password, and name. Returns user object and JWT tokens upon successful registration.

### Specification Reference

- **User Story**: User Story 1 - User Authentication and Account Management (P1)
- **Functional Requirements**: FR-001, FR-002, FR-003, FR-004, FR-005
- **Success Criteria**: SC-001

### Request

**Method**: `POST`
**Path**: `/api/auth/signup`
**Content-Type**: `application/json`
**Authentication**: None (public endpoint)

**Request Body Schema**:
```json
{
  "email": "string (required, email format, max 255 chars)",
  "password": "string (required, min 8 chars)",
  "name": "string (required, min 1 char, max 100 chars)"
}
```

**Request Body Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Validation Rules**:
- `email`: Must match email regex pattern (FR-002), must be unique (FR-005)
- `password`: Minimum 8 characters (FR-003), will be hashed with bcrypt (FR-004)
- `name`: Required, not empty, max 100 characters

### Response

**Success Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-11T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response Fields**:
- `user.id`: Unique user identifier (integer or UUID)
- `user.email`: User's email address
- `user.name`: User's display name
- `user.created_at`: ISO 8601 timestamp of account creation
- `access_token`: JWT access token (expires in 15 minutes)
- `refresh_token`: JWT refresh token (expires in 7 days)
- `token_type`: Always "bearer"

**Note**: `password_hash` is never included in response (security requirement)

### Error Responses

**400 Bad Request** (Malformed JSON):
```json
{
  "detail": "Invalid JSON format"
}
```

**422 Unprocessable Entity** (Validation Error - Invalid Email):
```json
{
  "detail": "Invalid email format"
}
```

**422 Unprocessable Entity** (Validation Error - Password Too Short):
```json
{
  "detail": "Password must be at least 8 characters"
}
```

**409 Conflict** (Duplicate Email):
```json
{
  "detail": "Email already registered"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Security Considerations

- Password is hashed with bcrypt (cost factor 12) before storage (NFR-001)
- Email uniqueness enforced at database level (FR-005)
- No rate limiting on signup (consider adding if abuse detected)

---

## Endpoint: POST /api/auth/signin

### Description

Authenticates a user with email and password. Returns user object and JWT tokens upon successful authentication.

### Specification Reference

- **User Story**: User Story 1 - User Authentication and Account Management (P1)
- **Functional Requirements**: FR-006, FR-007, FR-008, FR-009, FR-010
- **Success Criteria**: SC-001, SC-002

### Request

**Method**: `POST`
**Path**: `/api/auth/signin`
**Content-Type**: `application/json`
**Authentication**: None (public endpoint)

**Request Body Schema**:
```json
{
  "email": "string (required, email format)",
  "password": "string (required)"
}
```

**Request Body Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Response

**Success Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-11T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**JWT Token Claims**:
- `user_id`: User's unique identifier (FR-007)
- `exp`: Token expiration timestamp (FR-009: 15 minutes for access token)
- Signed with BETTER_AUTH_SECRET using HS256 algorithm (FR-008, NFR-002)

### Error Responses

**400 Bad Request** (Malformed JSON):
```json
{
  "detail": "Invalid JSON format"
}
```

**401 Unauthorized** (Invalid Credentials):
```json
{
  "detail": "Invalid email or password"
}
```

**Note**: Generic error message for security (don't reveal if email exists)

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Security Considerations

- Use constant-time password comparison to prevent timing attacks
- Return generic error message for failed authentication (security best practice)
- Rate limiting recommended to prevent brute force attacks (NFR-005)
- Response time target: <500ms under normal load (NFR-009)

---

## Endpoint: POST /api/auth/refresh

### Description

Issues a new access token using a valid refresh token. Allows users to maintain authenticated sessions without re-entering credentials.

### Specification Reference

- **User Story**: User Story 1 - User Authentication and Account Management (P1)
- **Functional Requirements**: FR-011
- **Success Criteria**: SC-002

### Request

**Method**: `POST`
**Path**: `/api/auth/refresh`
**Content-Type**: `application/json`
**Authentication**: None (refresh token provided in body)

**Request Body Schema**:
```json
{
  "refresh_token": "string (required, JWT format)"
}
```

**Request Body Example**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Response

**Success Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response Fields**:
- `access_token`: New JWT access token (expires in 15 minutes)
- `token_type`: Always "bearer"

**Note**: Refresh token is not rotated in this implementation (consider token rotation for enhanced security)

### Error Responses

**400 Bad Request** (Malformed JSON):
```json
{
  "detail": "Invalid JSON format"
}
```

**401 Unauthorized** (Invalid or Expired Refresh Token):
```json
{
  "detail": "Invalid or expired refresh token"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Security Considerations

- Validate refresh token signature and expiration (FR-013)
- Refresh token expires in 7 days (FR-010)
- Consider implementing token rotation for enhanced security (edge case: refresh token reuse)

---

## Endpoint: POST /api/auth/signout

### Description

Invalidates the user's session and tokens. In stateless JWT implementation, this is primarily a client-side operation (client discards tokens).

### Specification Reference

- **User Story**: User Story 1 - User Authentication and Account Management (P1)
- **Functional Requirements**: FR-012
- **Success Criteria**: SC-001

### Request

**Method**: `POST`
**Path**: `/api/auth/signout`
**Content-Type**: `application/json`
**Authentication**: Required (Bearer token)

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**: Empty (no body required)

### Response

**Success Response** (200 OK):
```json
{
  "detail": "Successfully signed out"
}
```

### Error Responses

**401 Unauthorized** (Missing or Invalid Token):
```json
{
  "detail": "Not authenticated"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

### Implementation Notes

- In stateless JWT implementation, signout is primarily client-side (client discards tokens)
- Server can optionally maintain a token blacklist for revoked tokens (not required for MVP)
- Frontend should clear tokens from localStorage/memory on signout

---

## Common Headers

### Request Headers

**All Authenticated Endpoints**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Public Endpoints** (signup, signin):
```
Content-Type: application/json
```

### Response Headers

**All Endpoints**:
```
Content-Type: application/json
Access-Control-Allow-Origin: <FRONTEND_URL from environment>
Access-Control-Allow-Credentials: true
```

---

## JWT Token Structure

### Access Token

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:
```json
{
  "user_id": 1,
  "exp": 1704988800
}
```

**Signature**: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), BETTER_AUTH_SECRET)

**Expiration**: 15 minutes from issuance (FR-009)

### Refresh Token

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:
```json
{
  "user_id": 1,
  "exp": 1705593600
}
```

**Signature**: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), BETTER_AUTH_SECRET)

**Expiration**: 7 days from issuance (FR-010)

---

## Frontend Integration

### Expected Frontend Behavior

1. **Signup Flow**:
   - POST /api/auth/signup with user data
   - Store access_token and refresh_token in localStorage or memory
   - Redirect to dashboard

2. **Signin Flow**:
   - POST /api/auth/signin with credentials
   - Store access_token and refresh_token
   - Redirect to dashboard

3. **Authenticated Requests**:
   - Include `Authorization: Bearer <access_token>` header
   - Handle 401 responses by refreshing token or redirecting to signin

4. **Token Refresh Flow**:
   - When access_token expires (401 response)
   - POST /api/auth/refresh with refresh_token
   - Store new access_token
   - Retry original request

5. **Signout Flow**:
   - POST /api/auth/signout (optional)
   - Clear tokens from storage
   - Redirect to signin page

### Frontend TypeScript Types

```typescript
// Request types
interface SignupRequest {
  email: string;
  password: string;
  name: string;
}

interface SigninRequest {
  email: string;
  password: string;
}

interface RefreshRequest {
  refresh_token: string;
}

// Response types
interface AuthResponse {
  user: {
    id: number;
    email: string;
    name: string;
    created_at: string;
  };
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface RefreshResponse {
  access_token: string;
  token_type: string;
}

interface ErrorResponse {
  detail: string;
}
```

---

## Testing Checklist

### Functional Tests

- [ ] Signup with valid data returns 201 with user and tokens
- [ ] Signup with duplicate email returns 409
- [ ] Signup with invalid email format returns 422
- [ ] Signup with short password returns 422
- [ ] Signin with valid credentials returns 200 with user and tokens
- [ ] Signin with invalid credentials returns 401
- [ ] Refresh with valid token returns 200 with new access token
- [ ] Refresh with expired token returns 401
- [ ] Signout with valid token returns 200

### Security Tests

- [ ] Password is hashed before storage (never stored plain text)
- [ ] JWT tokens are signed with BETTER_AUTH_SECRET
- [ ] Access token expires in 15 minutes
- [ ] Refresh token expires in 7 days
- [ ] Invalid JWT signature is rejected
- [ ] Expired JWT is rejected

### Performance Tests

- [ ] Signup completes in <500ms under normal load
- [ ] Signin completes in <500ms under normal load

---

## Summary

This contract defines 4 authentication endpoints: signup, signin, refresh, and signout. All endpoints follow RESTful conventions, return consistent JSON responses with "detail" field for errors, and integrate seamlessly with the Next.js frontend. JWT tokens follow Better Auth pattern with 15-minute access tokens and 7-day refresh tokens.
