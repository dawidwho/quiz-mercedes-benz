"""
People router with CRUD endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps, schemas, crud
from app.db.models import People as PeopleModel

router = APIRouter(prefix="/people", tags=["people"])

# Create CRUD instance
people_crud = crud.CRUDBase(PeopleModel)


@router.get("/", response_model=List[schemas.People])
def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """Retrieve people."""
    people = people_crud.get_multi(db, skip=skip, limit=limit)
    return people


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
