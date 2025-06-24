"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel
from typing import Optional, List


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    class Config:
        from_attributes = True


class PeopleBase(BaseSchema):
    """Base schema for people."""

    name: str
    height: Optional[str] = None
    mass: Optional[str] = None
    hair_color: Optional[str] = None
    skin_color: Optional[str] = None
    eye_color: Optional[str] = None
    birth_year: Optional[str] = None
    gender: Optional[str] = None


class PeopleCreate(PeopleBase):
    """Schema for creating people."""

    pass


class PeopleUpdate(BaseSchema):
    """Schema for updating people."""

    name: Optional[str] = None
    height: Optional[str] = None
    mass: Optional[str] = None
    hair_color: Optional[str] = None
    skin_color: Optional[str] = None
    eye_color: Optional[str] = None
    birth_year: Optional[str] = None
    gender: Optional[str] = None


class People(PeopleBase):
    """Schema for people responses."""

    id: int


class PlanetsBase(BaseSchema):
    """Base schema for planets."""

    name: str
    diameter: Optional[str] = None
    rotation_period: Optional[str] = None
    orbital_period: Optional[str] = None
    gravity: Optional[str] = None
    population: Optional[str] = None
    climate: Optional[str] = None
    terrain: Optional[str] = None
    surface_water: Optional[str] = None


class PlanetsCreate(PlanetsBase):
    """Schema for creating planets."""

    pass


class PlanetsUpdate(BaseSchema):
    """Schema for updating planets."""

    name: Optional[str] = None
    diameter: Optional[str] = None
    rotation_period: Optional[str] = None
    orbital_period: Optional[str] = None
    gravity: Optional[str] = None
    population: Optional[str] = None
    climate: Optional[str] = None
    terrain: Optional[str] = None
    surface_water: Optional[str] = None


class Planets(PlanetsBase):
    """Schema for planets responses."""

    id: int
