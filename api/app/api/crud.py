"""
CRUD operations for database models.
"""

import time
import logging
from typing import List, Optional, Type, TypeVar, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, asc, or_

from app.db.base import Base
from app.api.sorting import sort_factory
from app.api.schemas import SortField, SortOrder
from app.core.monitoring import log_search_operation, log_sort_operation

logger = logging.getLogger(__name__)
ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase:
    """
    Base class for CRUD operations.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi_paginated(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> Tuple[List[ModelType], int]:
        """Get multiple records with pagination and total count."""
        items = db.query(self.model).offset(skip).limit(limit).all()
        total = db.query(func.count(self.model.id)).scalar()
        return items, total

    def get_multi_paginated_with_sort(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[SortField] = None,
        sort_order: SortOrder = SortOrder.ASC,
    ) -> Tuple[List[ModelType], int]:
        """Get multiple records with pagination, sorting and total count using strategy pattern."""
        start_time = time.time()

        query = db.query(self.model)

        # Apply sorting using the strategy pattern
        if sort_by:
            query = sort_factory.apply_sort(query, self.model, sort_by, sort_order)
        else:
            # Default sorting by ID
            query = query.order_by(asc(self.model.id))

        items = query.offset(skip).limit(limit).all()
        total = db.query(func.count(self.model.id)).scalar()

        # Calculate execution time and log sort operation
        execution_time = (time.time() - start_time) * 1000

        # Determine resource type based on model
        resource_type = self._get_resource_type()

        # Log the sort operation
        if sort_by:
            log_sort_operation(
                resource_type=resource_type,
                sort_field=sort_by.value if hasattr(sort_by, "value") else str(sort_by),
                sort_order=(
                    sort_order.value
                    if hasattr(sort_order, "value")
                    else str(sort_order)
                ),
                results_count=len(items),
                total_count=total,
                page=(skip // limit) + 1,
                size=limit,
                execution_time_ms=execution_time,
            )

        return items, total

    def get_multi_paginated_with_search(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[SortField] = None,
        sort_order: SortOrder = SortOrder.ASC,
        search_params: Optional[dict] = None,
    ) -> Tuple[List[ModelType], int]:
        """Get multiple records with pagination, sorting, search and total count."""
        start_time = time.time()

        query = db.query(self.model)

        # Apply search filters
        if search_params:
            search_filters = []
            for field_name, search_value in search_params.items():
                if hasattr(self.model, field_name) and search_value:
                    # Case-insensitive partial match using ILIKE
                    field = getattr(self.model, field_name)
                    search_filters.append(field.ilike(f"%{search_value}%"))

            if search_filters:
                query = query.filter(or_(*search_filters))

        # Apply sorting using the strategy pattern
        if sort_by:
            query = sort_factory.apply_sort(query, self.model, sort_by, sort_order)
        else:
            # Default sorting by ID
            query = query.order_by(asc(self.model.id))

        # Get total count for pagination
        total_query = query
        total = total_query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000

        # Determine resource type based on model
        resource_type = self._get_resource_type()

        # Log search operation if search parameters were provided
        if search_params:
            log_search_operation(
                resource_type=resource_type,
                search_params=search_params,
                results_count=len(items),
                total_count=total,
                page=(skip // limit) + 1,
                size=limit,
                execution_time_ms=execution_time,
            )

        # Log sort operation if sorting was applied
        if sort_by:
            log_sort_operation(
                resource_type=resource_type,
                sort_field=sort_by.value if hasattr(sort_by, "value") else str(sort_by),
                sort_order=(
                    sort_order.value
                    if hasattr(sort_order, "value")
                    else str(sort_order)
                ),
                results_count=len(items),
                total_count=total,
                page=(skip // limit) + 1,
                size=limit,
                execution_time_ms=execution_time,
            )

        return items, total

    def create(self, db: Session, obj_in) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in) -> ModelType:
        """Update an existing record."""
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> ModelType:
        """Delete a record by ID."""
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj

    def _get_resource_type(self) -> str:
        """Determine the resource type based on the model."""
        model_name = self.model.__name__.lower()
        if "people" in model_name:
            return "people"
        elif "planets" in model_name:
            return "planets"
        else:
            return model_name
