#!/usr/bin/env python3
"""
Simple script to create database tables manually.
This can be used if you need to create tables without running the full data loader.
"""

import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://quiz_user:quiz_password@postgres:5432/quiz_db"
)

# Create database engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

# Create base class for models
Base = declarative_base()


# Define models
class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    height = Column(String, nullable=True)
    mass = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    skin_color = Column(String, nullable=True)
    eye_color = Column(String, nullable=True)
    birth_year = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Planets(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    diameter = Column(String, nullable=True)
    rotation_period = Column(String, nullable=True)
    orbital_period = Column(String, nullable=True)
    gravity = Column(String, nullable=True)
    population = Column(String, nullable=True)
    climate = Column(String, nullable=True)
    terrain = Column(String, nullable=True)
    surface_water = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def create_tables():
    """Create all database tables."""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        print("Tables created:")
        print("  - people")
        print("  - planets")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_tables()
