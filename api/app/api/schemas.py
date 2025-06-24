"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel
from typing import Optional, List, Generic, TypeVar
from enum import Enum
from datetime import datetime

T = TypeVar("T")


class SortOrder(str, Enum):
    """Sort order enumeration."""

    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    """Sortable fields enumeration."""

    # People fields
    NAME = "name"
    HEIGHT = "height"
    MASS = "mass"
    HAIR_COLOR = "hair_color"
    SKIN_COLOR = "skin_color"
    EYE_COLOR = "eye_color"
    BIRTH_YEAR = "birth_year"
    GENDER = "gender"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

    # Planet fields
    DIAMETER = "diameter"
    ROTATION_PERIOD = "rotation_period"
    ORBITAL_PERIOD = "orbital_period"
    GRAVITY = "gravity"
    POPULATION = "population"
    CLIMATE = "climate"
    TERRAIN = "terrain"
    SURFACE_WATER = "surface_water"


class PaginationParams(BaseModel):
    """Pagination parameters for requests."""

    page: int = 1
    size: int = 10


class SortParams(BaseModel):
    """Sorting parameters for requests."""

    sort_by: Optional[SortField] = None
    sort_order: SortOrder = SortOrder.ASC


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema."""

    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
