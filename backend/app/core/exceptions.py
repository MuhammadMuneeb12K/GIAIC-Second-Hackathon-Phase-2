"""
Custom Exception Classes for the API.

This module defines custom exceptions used throughout the application
for consistent error handling and HTTP status code mapping.
"""


class AuthenticationError(Exception):
    """
    Raised when authentication fails.

    This exception should be raised when:
    - Invalid credentials are provided
    - JWT token is invalid or expired
    - User is not authenticated

    Maps to HTTP 401 Unauthorized.
    """
    pass


class AuthorizationError(Exception):
    """
    Raised when user is authenticated but not authorized for the action.

    This exception should be raised when:
    - User tries to access resources they don't own
    - User lacks required permissions

    Maps to HTTP 403 Forbidden.
    """
    pass


class ValidationError(Exception):
    """
    Raised when input validation fails.

    This exception should be raised when:
    - Request data doesn't match expected schema
    - Business logic validation fails

    Maps to HTTP 422 Unprocessable Entity.
    """
    pass


class NotFoundError(Exception):
    """
    Raised when a requested resource is not found.

    This exception should be raised when:
    - Resource doesn't exist
    - User tries to access another user's resource (for security)

    Maps to HTTP 404 Not Found.
    """
    pass


class ConflictError(Exception):
    """
    Raised when a request conflicts with existing data.

    This exception should be raised when:
    - Duplicate email registration
    - Unique constraint violations

    Maps to HTTP 409 Conflict.
    """
    pass
