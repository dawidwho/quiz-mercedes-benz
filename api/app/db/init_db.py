"""
Database initialization script.
"""

import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from app.db.base import Base
from app.db.session import engine

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize database tables."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        logger.info(
            "Please check your database configuration and ensure the database server is running."
        )
        raise
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")
