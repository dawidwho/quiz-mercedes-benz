"""
Tests for people endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.api.schemas import PeopleCreate


def test_create_people(client: TestClient):
    """Test creating a new people."""
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

    response = client.post("/api/people/", json=people_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == people_data["name"]
    assert data["height"] == people_data["height"]
    assert "id" in data


def test_read_people(client: TestClient):
    """Test reading people list."""
    response = client.get("/api/people/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_people_by_id(client: TestClient):
    """Test reading a specific people by ID."""
    # First create a people
    people_data = {"name": "Leia Organa", "height": "150"}
    create_response = client.post("/api/people/", json=people_data)
    people_id = create_response.json()["id"]

    # Then read it by ID
    response = client.get(f"/api/people/{people_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == people_id
    assert data["name"] == people_data["name"]


def test_update_people(client: TestClient):
    """Test updating a people."""
    # First create a people
    people_data = {"name": "Han Solo", "height": "180"}
    create_response = client.post("/api/people/", json=people_data)
    people_id = create_response.json()["id"]

    # Then update it
    update_data = {"height": "185"}
    response = client.put(f"/api/people/{people_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["height"] == update_data["height"]


def test_delete_people(client: TestClient):
    """Test deleting a people."""
    # First create a people
    people_data = {"name": "Chewbacca", "height": "228"}
    create_response = client.post("/api/people/", json=people_data)
    people_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/api/people/{people_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/api/people/{people_id}")
    assert get_response.status_code == 404


def test_read_nonexistent_people(client: TestClient):
    """Test reading a non-existent people."""
    response = client.get("/api/people/999")
    assert response.status_code == 404
