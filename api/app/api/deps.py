"""
Common dependencies for API endpoints.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Dependency to get database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
