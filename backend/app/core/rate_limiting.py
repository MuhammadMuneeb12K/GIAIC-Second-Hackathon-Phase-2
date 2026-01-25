"""
Rate Limiting Middleware (Optional Enhancement).

This module provides rate limiting for authentication endpoints to prevent
brute force attacks (NFR-005).

Installation required: pip install slowapi

Usage:
    Uncomment the code below and add slowapi to requirements.txt
"""

# Uncomment to enable rate limiting:
#
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
#
# # Create limiter instance
# limiter = Limiter(key_func=get_remote_address)
#
# # Add to FastAPI app in main.py:
# # app.state.limiter = limiter
# # app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
#
# # Apply to auth endpoints in routes/auth.py:
# # @router.post("/signup")
# # @limiter.limit("5/minute")
# # def signup(request: Request, ...):
# #     ...
#
# # @router.post("/signin")
# # @limiter.limit("5/minute")
# # def signin(request: Request, ...):
# #     ...

# Note: Rate limiting is recommended for production but not required for MVP.
# The specification (NFR-005) recommends it but doesn't mandate it.
