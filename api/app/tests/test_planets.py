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


def test_search_planets_by_name(client: TestClient):
    """Test searching planets by name with case-insensitive partial matching."""
    # Create test data
    planets_data_1 = {"name": "Tatooine", "climate": "arid"}
    planets_data_2 = {"name": "Alderaan", "climate": "temperate"}
    planets_data_3 = {"name": "Yavin IV", "climate": "tropical"}

    client.post("/api/planets/", json=planets_data_1)
    client.post("/api/planets/", json=planets_data_2)
    client.post("/api/planets/", json=planets_data_3)

    # Test search by "tatoo" (should find "Tatooine")
    response = client.get("/api/planets/?name=tatoo")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any("Tatooine" in planet["name"] for planet in data["items"])

    # Test search by "TATOO" (case-insensitive)
    response = client.get("/api/planets/?name=TATOO")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any("Tatooine" in planet["name"] for planet in data["items"])

    # Test search by "yavin" (partial match)
    response = client.get("/api/planets/?name=yavin")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any("Yavin" in planet["name"] for planet in data["items"])


def test_search_planets_by_climate(client: TestClient):
    """Test searching planets by climate field."""
    # Create test data
    planets_data_1 = {"name": "Tatooine", "climate": "arid"}
    planets_data_2 = {"name": "Hoth", "climate": "frozen"}
    planets_data_3 = {"name": "Naboo", "climate": "temperate"}

    client.post("/api/planets/", json=planets_data_1)
    client.post("/api/planets/", json=planets_data_2)
    client.post("/api/planets/", json=planets_data_3)

    # Test search by "arid" climate
    response = client.get("/api/planets/?climate=arid")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any(planet["climate"] == "arid" for planet in data["items"])

    # Test search by "frozen" climate
    response = client.get("/api/planets/?climate=frozen")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any(planet["climate"] == "frozen" for planet in data["items"])


def test_search_planets_by_multiple_fields(client: TestClient):
    """Test searching planets by multiple fields."""
    # Create test data
    planets_data_1 = {"name": "Tatooine", "climate": "arid", "terrain": "desert"}
    planets_data_2 = {"name": "Hoth", "climate": "frozen", "terrain": "tundra"}

    client.post("/api/planets/", json=planets_data_1)
    client.post("/api/planets/", json=planets_data_2)

    # Test search by name and climate
    response = client.get("/api/planets/?name=tatooine&climate=arid")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert any(
        planet["name"] == "Tatooine" and planet["climate"] == "arid"
        for planet in data["items"]
    )


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
