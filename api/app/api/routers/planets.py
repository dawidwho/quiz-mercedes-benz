"""
Planets router with CRUD endpoints.
"""

from typing import List
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
    sort_by: str = Query(
        None, description="Field to sort by (name, diameter, population, etc.)"
    ),
    sort_order: schemas.SortOrder = Query(
        schemas.SortOrder.ASC, description="Sort order (asc or desc)"
    ),
    db: Session = Depends(deps.get_db),
):
    """Retrieve planets with pagination and sorting."""
    skip = (page - 1) * size
    planets, total = planets_crud.get_multi_paginated_with_sort(
        db, skip=skip, limit=size, sort_by=sort_by, sort_order=sort_order
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
