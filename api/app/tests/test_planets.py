"""
Tests for planets endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.api.schemas import PlanetsCreate


def test_create_planets(client: TestClient):
    """Test creating a new planets."""
    planets_data = {
        "name": "Tatooine",
        "diameter": "10465",
        "rotation_period": "23",
        "orbital_period": "304",
        "gravity": "1 standard",
        "population": "200000",
        "climate": "arid",
        "terrain": "desert",
        "surface_water": "1",
    }

    response = client.post("/api/planets/", json=planets_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == planets_data["name"]
    assert data["diameter"] == planets_data["diameter"]
    assert "id" in data


def test_read_planets(client: TestClient):
    """Test reading planets list."""
    response = client.get("/api/planets/")
    assert response.status_code == 200
    data = response.json()
    # Check that it's a paginated response object
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert "pages" in data
    assert "has_next" in data
    assert "has_prev" in data
    assert isinstance(data["items"], list)


def test_read_planets_by_id(client: TestClient):
    """Test reading a specific planets by ID."""
    # First create a planets
    planets_data = {"name": "Alderaan", "diameter": "12500"}
    create_response = client.post("/api/planets/", json=planets_data)
    planets_id = create_response.json()["id"]

    # Then read it by ID
    response = client.get(f"/api/planets/{planets_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == planets_id
    assert data["name"] == planets_data["name"]


def test_update_planets(client: TestClient):
    """Test updating a planets."""
    # First create a planets
    planets_data = {"name": "Yavin IV", "diameter": "10200"}
    create_response = client.post("/api/planets/", json=planets_data)
    planets_id = create_response.json()["id"]

    # Then update it
    update_data = {"diameter": "10500"}
    response = client.put(f"/api/planets/{planets_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["diameter"] == update_data["diameter"]


def test_delete_planets(client: TestClient):
    """Test deleting a planets."""
    # First create a planets
    planets_data = {"name": "Hoth", "climate": "frozen"}
    create_response = client.post("/api/planets/", json=planets_data)
    planets_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/api/planets/{planets_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/api/planets/{planets_id}")
    assert get_response.status_code == 404


def test_read_nonexistent_planets(client: TestClient):
    """Test reading a non-existent planets."""
    response = client.get("/api/planets/999")
    assert response.status_code == 404
