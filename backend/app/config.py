"""
Application Configuration using Pydantic Settings.

This module defines the configuration settings for the FastAPI application,
loading values from environment variables with validation.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are validated at startup to ensure the application
    has the required configuration before accepting requests.
    """

    # Database Configuration
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL database connection string"
    )

    # Authentication Configuration
    BETTER_AUTH_SECRET: str = Field(
        ...,
        min_length=32,
        description="Secret key for JWT token signing (minimum 32 characters)"
    )

    # CORS Configuration
    FRONTEND_URL: str = Field(
        ...,
        description="Frontend origin URL for CORS configuration"
    )

    # Token Expiration Configuration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        description="Access token expiration time in minutes"
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )

    # JWT Algorithm
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )

    @validator("BETTER_AUTH_SECRET")
    def validate_secret_length(cls, v):
        """Ensure the secret key is at least 32 characters for security."""
        if len(v) < 32:
            raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters long")
        return v

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        """Ensure database URL is provided and in valid SQLAlchemy format."""
        if not v or v.strip() == "":
            raise ValueError("DATABASE_URL must be provided")

        # Check for common formatting errors
        if v.startswith("psql ") or v.startswith("'") or v.endswith("'"):
            raise ValueError(
                "DATABASE_URL appears to be in shell command format. "
                "Remove 'psql' prefix and quotes. "
                "Expected format: postgresql://user:pass@host:port/dbname"
            )

        # Ensure it starts with a valid database scheme
        valid_schemes = ["postgresql://", "postgresql+psycopg2://", "sqlite://"]
        if not any(v.startswith(scheme) for scheme in valid_schemes):
            raise ValueError(
                f"DATABASE_URL must start with one of: {', '.join(valid_schemes)}"
            )

        return v

    @validator("FRONTEND_URL")
    def validate_frontend_url(cls, v):
        """Ensure frontend URL is provided and not empty."""
        if not v or v.strip() == "":
            raise ValueError("FRONTEND_URL must be provided")
        return v

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
