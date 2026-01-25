"""
Database Connection and Session Management.

This module handles:
- SQLModel engine creation with connection pooling
- Database session management for dependency injection
- Database initialization (create tables)
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.config import settings


# Create database engine with connection pooling
# For production, use proper connection pool settings
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging in development
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Maximum overflow connections
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    This function should be called at application startup to ensure
    all tables exist. It's idempotent - safe to call multiple times.

    Note: In production, use proper migration tools like Alembic.
    """
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.

    Yields a database session that is automatically closed after use.
    Use this as a dependency in FastAPI endpoints.

    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db session here
            pass

    Yields:
        Session: SQLModel database session

    Ensures:
        - Session is properly closed after request
        - Transactions are committed or rolled back appropriately
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
