"""
Sorting strategy pattern implementation following Open-Closed Principle.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type
from sqlalchemy.orm import Query
from sqlalchemy import desc, asc
from app.api.schemas import SortField, SortOrder


class SortStrategy(ABC):
    """Abstract base class for sorting strategies."""

    @abstractmethod
    def can_handle(self, model: Any, sort_field: SortField) -> bool:
        """Check if this strategy can handle the given model and sort field."""
        pass

    @abstractmethod
    def apply_sort(
        self, query: Query, model: Any, sort_field: SortField, sort_order: SortOrder
    ) -> Query:
        """Apply sorting to the query."""
        pass


class PeopleSortStrategy(SortStrategy):
    """Sorting strategy for People model."""

    def can_handle(self, model: Any, sort_field: SortField) -> bool:
        """Check if this strategy can handle People model sorting."""
        from app.db.models import People

        return isinstance(model, type) and issubclass(model, People)

    def apply_sort(
        self, query: Query, model: Any, sort_field: SortField, sort_order: SortOrder
    ) -> Query:
        """Apply sorting to People query."""
        # Map sort fields to model attributes
        field_mapping = {
            SortField.NAME: model.name,
            SortField.HEIGHT: model.height,
            SortField.MASS: model.mass,
            SortField.HAIR_COLOR: model.hair_color,
            SortField.SKIN_COLOR: model.skin_color,
            SortField.EYE_COLOR: model.eye_color,
            SortField.BIRTH_YEAR: model.birth_year,
            SortField.GENDER: model.gender,
        }

        if sort_field in field_mapping:
            sort_column = field_mapping[sort_field]
            if sort_order == SortOrder.DESC:
                return query.order_by(desc(sort_column))
            else:
                return query.order_by(asc(sort_column))

        # Default sorting by ID if field not found
        return query.order_by(asc(model.id))


class PlanetsSortStrategy(SortStrategy):
    """Sorting strategy for Planets model."""

    def can_handle(self, model: Any, sort_field: SortField) -> bool:
        """Check if this strategy can handle Planets model sorting."""
        from app.db.models import Planets

        return isinstance(model, type) and issubclass(model, Planets)

    def apply_sort(
        self, query: Query, model: Any, sort_field: SortField, sort_order: SortOrder
    ) -> Query:
        """Apply sorting to Planets query."""
        # Map sort fields to model attributes
        field_mapping = {
            SortField.NAME: model.name,
            SortField.DIAMETER: model.diameter,
            SortField.ROTATION_PERIOD: model.rotation_period,
            SortField.ORBITAL_PERIOD: model.orbital_period,
            SortField.GRAVITY: model.gravity,
            SortField.POPULATION: model.population,
            SortField.CLIMATE: model.climate,
            SortField.TERRAIN: model.terrain,
            SortField.SURFACE_WATER: model.surface_water,
        }

        if sort_field in field_mapping:
            sort_column = field_mapping[sort_field]
            if sort_order == SortOrder.DESC:
                return query.order_by(desc(sort_column))
            else:
                return query.order_by(asc(sort_column))

        # Default sorting by ID if field not found
        return query.order_by(asc(model.id))


# Example of extending the system with a new strategy (Open-Closed Principle)
class CustomSortStrategy(SortStrategy):
    """Example of a custom sorting strategy that could be added without modifying existing code."""

    def can_handle(self, model: Any, sort_field: SortField) -> bool:
        """Check if this strategy can handle custom model sorting."""
        # This could be for a new model type
        return False  # Placeholder

    def apply_sort(
        self, query: Query, model: Any, sort_field: SortField, sort_order: SortOrder
    ) -> Query:
        """Apply custom sorting logic."""
        # Custom sorting implementation
        return query.order_by(asc(model.id))


class SortStrategyFactory:
    """Factory for creating sorting strategies."""

    def __init__(self):
        self._strategies: Dict[str, SortStrategy] = {}
        self._register_default_strategies()

    def _register_default_strategies(self):
        """Register default sorting strategies."""
        self.register_strategy("people", PeopleSortStrategy())
        self.register_strategy("planets", PlanetsSortStrategy())

    def register_strategy(self, name: str, strategy: SortStrategy):
        """Register a new sorting strategy."""
        self._strategies[name] = strategy

    def get_strategy(self, model: Any) -> SortStrategy:
        """Get the appropriate strategy for the given model."""
        for strategy in self._strategies.values():
            if strategy.can_handle(model, SortField.NAME):  # Use NAME as a test field
                return strategy

        # Return a default strategy that sorts by ID
        return DefaultSortStrategy()

    def apply_sort(
        self, query: Query, model: Any, sort_field: SortField, sort_order: SortOrder
    ) -> Query:
        """Apply sorting using the appropriate strategy."""
        strategy = self.get_strategy(model)
        return strategy.apply_sort(query, model, sort_field, sort_order)


class DefaultSortStrategy(SortStrategy):
    """Default sorting strategy that sorts by ID."""

    def can_handle(self, model: Any, sort_field: SortField) -> bool:
        """Default strategy can handle any model."""
        return True

    def apply_sort(
        self, query: Query, model: Any, sort_field: SortField, sort_order: SortOrder
    ) -> Query:
        """Apply default sorting by ID."""
        if sort_order == SortOrder.DESC:
            return query.order_by(desc(model.id))
        else:
            return query.order_by(asc(model.id))


# Global factory instance
sort_factory = SortStrategyFactory()


# Example of how to extend the system (Open-Closed Principle demonstration)
def register_custom_sorting_strategy():
    """
    Example function showing how to extend the sorting system
    without modifying existing code (Open-Closed Principle).
    """
    # This could be called from anywhere to add new sorting strategies
    custom_strategy = CustomSortStrategy()
    sort_factory.register_strategy("custom", custom_strategy)
