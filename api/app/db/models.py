"""
Database models.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base


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
