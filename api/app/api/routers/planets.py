"""
Planets router with CRUD endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps, schemas, crud
from app.db.models import Planets as PlanetsModel

router = APIRouter(prefix="/planets", tags=["planets"])

# Create CRUD instance
planets_crud = crud.CRUDBase(PlanetsModel)


@router.get("/", response_model=schemas.PaginatedResponse[schemas.Planets])
def read_planets(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: schemas.SortField = Query(
        None, description="Field to sort by (name, diameter, population, etc.)"
    ),
    sort_order: schemas.SortOrder = Query(
        schemas.SortOrder.ASC, description="Sort order (asc or desc)"
    ),
    name: Optional[str] = Query(
        None, description="Search by name (case-insensitive partial match)"
    ),
    diameter: Optional[str] = Query(
        None, description="Search by diameter (case-insensitive partial match)"
    ),
    rotation_period: Optional[str] = Query(
        None, description="Search by rotation period (case-insensitive partial match)"
    ),
    orbital_period: Optional[str] = Query(
        None, description="Search by orbital period (case-insensitive partial match)"
    ),
    gravity: Optional[str] = Query(
        None, description="Search by gravity (case-insensitive partial match)"
    ),
    population: Optional[str] = Query(
        None, description="Search by population (case-insensitive partial match)"
    ),
    climate: Optional[str] = Query(
        None, description="Search by climate (case-insensitive partial match)"
    ),
    terrain: Optional[str] = Query(
        None, description="Search by terrain (case-insensitive partial match)"
    ),
    surface_water: Optional[str] = Query(
        None, description="Search by surface water (case-insensitive partial match)"
    ),
    db: Session = Depends(deps.get_db),
):
    """Retrieve planets with pagination, sorting, and search."""
    skip = (page - 1) * size

    # Build search parameters from query parameters
    search_params = {}
    if name:
        search_params["name"] = name
    if diameter:
        search_params["diameter"] = diameter
    if rotation_period:
        search_params["rotation_period"] = rotation_period
    if orbital_period:
        search_params["orbital_period"] = orbital_period
    if gravity:
        search_params["gravity"] = gravity
    if population:
        search_params["population"] = population
    if climate:
        search_params["climate"] = climate
    if terrain:
        search_params["terrain"] = terrain
    if surface_water:
        search_params["surface_water"] = surface_water

    planets, total = planets_crud.get_multi_paginated_with_search(
        db,
        skip=skip,
        limit=size,
        sort_by=sort_by,
        sort_order=sort_order,
        search_params=search_params if search_params else None,
    )

    pages = (total + size - 1) // size  # Calculate total pages
    has_next = page < pages
    has_prev = page > 1

    return schemas.PaginatedResponse(
        items=planets,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev,
    )


@router.post("/", response_model=schemas.Planets, status_code=status.HTTP_201_CREATED)
def create_planets(planets: schemas.PlanetsCreate, db: Session = Depends(deps.get_db)):
    """Create new planets."""
    return planets_crud.create(db=db, obj_in=planets)


@router.get("/{planets_id}", response_model=schemas.Planets)
def read_planets_by_id(planets_id: int, db: Session = Depends(deps.get_db)):
    """Get a specific planets by ID."""
    planets = planets_crud.get(db=db, id=planets_id)
    if planets is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planets not found"
        )
    return planets


@router.put("/{planets_id}", response_model=schemas.Planets)
def update_planets(
    planets_id: int, planets: schemas.PlanetsUpdate, db: Session = Depends(deps.get_db)
):
    """Update planets."""
    db_planets = planets_crud.get(db=db, id=planets_id)
    if db_planets is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planets not found"
        )
    return planets_crud.update(db=db, db_obj=db_planets, obj_in=planets)


@router.delete("/{planets_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_planets(planets_id: int, db: Session = Depends(deps.get_db)):
    """Delete planets."""
    planets = planets_crud.get(db=db, id=planets_id)
    if planets is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planets not found"
        )
    planets_crud.remove(db=db, id=planets_id)
    return None
