"""
Tests for AI insights endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_simulate_ai_insight_people_post(client: TestClient):
    """Test AI insight generation for people using POST."""
    # First create a test person
    people_data = {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
    }
    client.post("/api/people/", json=people_data)

    # Test AI insight generation
    insight_request = {"name": "Luke Skywalker", "entity_type": "people"}

    response = client.post("/api/simulate-ai-insight/", json=insight_request)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Luke Skywalker"
    assert data["entity_type"] == "people"
    assert "insight" in data
    assert "confidence_score" in data
    assert "generated_at" in data
    assert "model_version" in data
    assert data["model_version"] == "v1.0"
    assert 0.75 <= data["confidence_score"] <= 0.98


def test_simulate_ai_insight_planets_post(client: TestClient):
    """Test AI insight generation for planets using POST."""
    # First create a test planet
    planet_data = {
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
    client.post("/api/planets/", json=planet_data)

    # Test AI insight generation
    insight_request = {"name": "Tatooine", "entity_type": "planets"}

    response = client.post("/api/simulate-ai-insight/", json=insight_request)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Tatooine"
    assert data["entity_type"] == "planets"
    assert "insight" in data
    assert "confidence_score" in data
    assert "generated_at" in data
    assert "model_version" in data
    assert data["model_version"] == "v1.0"
    assert 0.75 <= data["confidence_score"] <= 0.98


def test_simulate_ai_insight_people_get(client: TestClient):
    """Test AI insight generation for people using GET."""
    # First create a test person
    people_data = {
        "name": "Leia Organa",
        "height": "150",
        "mass": "49",
        "hair_color": "brown",
        "skin_color": "light",
        "eye_color": "brown",
        "birth_year": "19BBY",
        "gender": "female",
    }
    client.post("/api/people/", json=people_data)

    # Test AI insight generation using GET
    response = client.get(
        "/api/simulate-ai-insight/?name=Leia%20Organa&entity_type=people"
    )
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Leia Organa"
    assert data["entity_type"] == "people"
    assert "insight" in data
    assert "confidence_score" in data
    assert "generated_at" in data
    assert "model_version" in data


def test_simulate_ai_insight_planets_get(client: TestClient):
    """Test AI insight generation for planets using GET."""
    # First create a test planet
    planet_data = {
        "name": "Alderaan",
        "diameter": "12500",
        "rotation_period": "24",
        "orbital_period": "364",
        "gravity": "1 standard",
        "population": "2000000000",
        "climate": "temperate",
        "terrain": "grasslands, mountains",
        "surface_water": "40",
    }
    client.post("/api/planets/", json=planet_data)

    # Test AI insight generation using GET
    response = client.get("/api/simulate-ai-insight/?name=Alderaan&entity_type=planets")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Alderaan"
    assert data["entity_type"] == "planets"
    assert "insight" in data
    assert "confidence_score" in data
    assert "generated_at" in data
    assert "model_version" in data


def test_simulate_ai_insight_invalid_entity_type(client: TestClient):
    """Test AI insight generation with invalid entity type."""
    insight_request = {"name": "Test Entity", "entity_type": "invalid_type"}

    response = client.post("/api/simulate-ai-insight/", json=insight_request)
    assert response.status_code == 400
    assert (
        "entity_type must be either 'people' or 'planets'" in response.json()["detail"]
    )


def test_simulate_ai_insight_nonexistent_entity(client: TestClient):
    """Test AI insight generation for non-existent entity."""
    insight_request = {"name": "Nonexistent Person", "entity_type": "people"}

    response = client.post("/api/simulate-ai-insight/", json=insight_request)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Nonexistent Person"
    assert data["entity_type"] == "people"
    assert "insight" in data
    assert data["confidence_score"] == 0.3  # Lower confidence for non-existent entities
    assert "not currently available in our database" in data["insight"]


def test_simulate_ai_insight_nonexistent_planet(client: TestClient):
    """Test AI insight generation for non-existent planet."""
    insight_request = {"name": "Nonexistent Planet", "entity_type": "planets"}

    response = client.post("/api/simulate-ai-insight/", json=insight_request)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Nonexistent Planet"
    assert data["entity_type"] == "planets"
    assert "insight" in data
    assert data["confidence_score"] == 0.3  # Lower confidence for non-existent entities
    assert "not currently catalogued in our database" in data["insight"]


def test_simulate_ai_insight_missing_parameters_get(client: TestClient):
    """Test AI insight generation with missing parameters using GET."""
    # Test missing name
    response = client.get("/api/simulate-ai-insight/?entity_type=people")
    assert response.status_code == 422  # Validation error

    # Test missing entity_type
    response = client.get("/api/simulate-ai-insight/?name=Test")
    assert response.status_code == 422  # Validation error
