"""
People router with CRUD endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps, schemas, crud
from app.db.models import People as PeopleModel

router = APIRouter(prefix="/people", tags=["people"])

# Create CRUD instance
people_crud = crud.CRUDBase(PeopleModel)


@router.get("/", response_model=schemas.PaginatedResponse[schemas.People])
def read_people(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: schemas.SortField = Query(
        None, description="Field to sort by (name, height, mass, etc.)"
    ),
    sort_order: schemas.SortOrder = Query(
        schemas.SortOrder.ASC, description="Sort order (asc or desc)"
    ),
    name: Optional[str] = Query(
        None, description="Search by name (case-insensitive partial match)"
    ),
    height: Optional[str] = Query(
        None, description="Search by height (case-insensitive partial match)"
    ),
    mass: Optional[str] = Query(
        None, description="Search by mass (case-insensitive partial match)"
    ),
    hair_color: Optional[str] = Query(
        None, description="Search by hair color (case-insensitive partial match)"
    ),
    skin_color: Optional[str] = Query(
        None, description="Search by skin color (case-insensitive partial match)"
    ),
    eye_color: Optional[str] = Query(
        None, description="Search by eye color (case-insensitive partial match)"
    ),
    birth_year: Optional[str] = Query(
        None, description="Search by birth year (case-insensitive partial match)"
    ),
    gender: Optional[str] = Query(
        None, description="Search by gender (case-insensitive partial match)"
    ),
    db: Session = Depends(deps.get_db),
):
    """Retrieve people with pagination, sorting, and search."""
    skip = (page - 1) * size

    # Build search parameters from query parameters
    search_params = {}
    if name:
        search_params["name"] = name
    if height:
        search_params["height"] = height
    if mass:
        search_params["mass"] = mass
    if hair_color:
        search_params["hair_color"] = hair_color
    if skin_color:
        search_params["skin_color"] = skin_color
    if eye_color:
        search_params["eye_color"] = eye_color
    if birth_year:
        search_params["birth_year"] = birth_year
    if gender:
        search_params["gender"] = gender

    people, total = people_crud.get_multi_paginated_with_search(
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
        items=people,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev,
    )


@router.post("/", response_model=schemas.People, status_code=status.HTTP_201_CREATED)
def create_people(people: schemas.PeopleCreate, db: Session = Depends(deps.get_db)):
    """Create new people."""
    return people_crud.create(db=db, obj_in=people)


@router.get("/{people_id}", response_model=schemas.People)
def read_people_by_id(people_id: int, db: Session = Depends(deps.get_db)):
    """Get a specific people by ID."""
    people = people_crud.get(db=db, id=people_id)
    if people is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="People not found"
        )
    return people


@router.put("/{people_id}", response_model=schemas.People)
def update_people(
    people_id: int, people: schemas.PeopleUpdate, db: Session = Depends(deps.get_db)
):
    """Update people."""
    db_people = people_crud.get(db=db, id=people_id)
    if db_people is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="People not found"
        )
    return people_crud.update(db=db, db_obj=db_people, obj_in=people)


@router.delete("/{people_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_people(people_id: int, db: Session = Depends(deps.get_db)):
    """Delete people."""
    people = people_crud.get(db=db, id=people_id)
    if people is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="People not found"
        )
    people_crud.remove(db=db, id=people_id)
    return None
