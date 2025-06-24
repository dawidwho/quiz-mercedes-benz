"""
Tests for sorting strategy pattern implementation.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.sorting import (
    SortStrategy,
    PeopleSortStrategy,
    PlanetsSortStrategy,
    SortStrategyFactory,
    DefaultSortStrategy,
)
from app.api.schemas import SortField, SortOrder
from app.db.models import People, Planets


class TestSortStrategy:
    """Test cases for sorting strategies."""

    def test_people_sort_strategy_can_handle(self):
        """Test that PeopleSortStrategy can handle People model."""
        strategy = PeopleSortStrategy()
        assert strategy.can_handle(People, SortField.NAME) is True
        assert strategy.can_handle(Planets, SortField.NAME) is False

    def test_planets_sort_strategy_can_handle(self):
        """Test that PlanetsSortStrategy can handle Planets model."""
        strategy = PlanetsSortStrategy()
        assert strategy.can_handle(Planets, SortField.NAME) is True
        assert strategy.can_handle(People, SortField.NAME) is False

    def test_default_sort_strategy_can_handle(self):
        """Test that DefaultSortStrategy can handle any model."""
        strategy = DefaultSortStrategy()
        assert strategy.can_handle(People, SortField.NAME) is True
        assert strategy.can_handle(Planets, SortField.NAME) is True


class TestSortStrategyFactory:
    """Test cases for SortStrategyFactory."""

    def test_factory_gets_correct_strategy(self):
        """Test that factory returns correct strategy for each model."""
        factory = SortStrategyFactory()

        # Test people strategy
        people_strategy = factory.get_strategy(People)
        assert isinstance(people_strategy, PeopleSortStrategy)

        # Test planets strategy
        planets_strategy = factory.get_strategy(Planets)
        assert isinstance(planets_strategy, PlanetsSortStrategy)

    def test_factory_registers_new_strategy(self):
        """Test that factory can register new strategies (Open-Closed Principle)."""
        factory = SortStrategyFactory()

        # Create a custom strategy
        class TestStrategy(SortStrategy):
            def can_handle(self, model, sort_field):
                return model == People

            def apply_sort(self, query, model, sort_field, sort_order):
                return query

        # Register the new strategy
        test_strategy = TestStrategy()
        factory.register_strategy("test", test_strategy)

        # Verify it's registered by checking if it's in the strategies dict
        assert "test" in factory._strategies
        assert factory._strategies["test"] == test_strategy

        # Test that the strategy can handle the model it's designed for
        assert test_strategy.can_handle(People, SortField.NAME) is True
        assert test_strategy.can_handle(Planets, SortField.NAME) is False


class TestSortFieldEnum:
    """Test cases for SortField enum."""

    def test_sort_field_values(self):
        """Test that SortField enum has correct values."""
        assert SortField.NAME == "name"
        assert SortField.HEIGHT == "height"
        assert SortField.MASS == "mass"
        assert SortField.DIAMETER == "diameter"
        assert SortField.POPULATION == "population"

    def test_sort_order_values(self):
        """Test that SortOrder enum has correct values."""
        assert SortOrder.ASC == "asc"
        assert SortOrder.DESC == "desc"
