#!/usr/bin/env python3
"""
Simple test script to demonstrate the search functionality.
Run this after starting the API server.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"


def test_search_functionality():
    """Test the search functionality with various examples."""

    print("🔍 Testing Search Functionality")
    print("=" * 50)

    # Test 1: Search people by name (case-insensitive partial match)
    print("\n1. Searching people by name='sky' (should find Luke Skywalker):")
    response = requests.get(f"{BASE_URL}/people/?name=sky")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results")
        for person in data["items"]:
            print(f"   - {person['name']}")
    else:
        print(f"   Error: {response.status_code}")

    # Test 2: Search people by name (case-insensitive)
    print("\n2. Searching people by name='SKY' (uppercase):")
    response = requests.get(f"{BASE_URL}/people/?name=SKY")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results")
        for person in data["items"]:
            print(f"   - {person['name']}")
    else:
        print(f"   Error: {response.status_code}")

    # Test 3: Search people by multiple fields
    print("\n3. Searching people by name='luke' and hair_color='blond':")
    response = requests.get(f"{BASE_URL}/people/?name=luke&hair_color=blond")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results")
        for person in data["items"]:
            print(f"   - {person['name']} (hair: {person.get('hair_color', 'N/A')})")
    else:
        print(f"   Error: {response.status_code}")

    # Test 4: Search planets by name
    print("\n4. Searching planets by name='tatoo' (should find Tatooine):")
    response = requests.get(f"{BASE_URL}/planets/?name=tatoo")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results")
        for planet in data["items"]:
            print(f"   - {planet['name']}")
    else:
        print(f"   Error: {response.status_code}")

    # Test 5: Search planets by climate
    print("\n5. Searching planets by climate='arid':")
    response = requests.get(f"{BASE_URL}/planets/?climate=arid")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results")
        for planet in data["items"]:
            print(f"   - {planet['name']} (climate: {planet.get('climate', 'N/A')})")
    else:
        print(f"   Error: {response.status_code}")

    # Test 6: Search with pagination
    print("\n6. Searching people by name='luke' with pagination (page=1, size=5):")
    response = requests.get(f"{BASE_URL}/people/?name=luke&page=1&size=5")
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results on page {data['page']}")
        print(f"   Total results: {data['total']}")
        print(f"   Total pages: {data['pages']}")
        for person in data["items"]:
            print(f"   - {person['name']}")
    else:
        print(f"   Error: {response.status_code}")

    # Test 7: Search with sorting
    print("\n7. Searching people by name='luke' with sorting by name (desc):")
    response = requests.get(
        f"{BASE_URL}/people/?name=luke&sort_by=name&sort_order=desc"
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   Found {len(data['items'])} results")
        for person in data["items"]:
            print(f"   - {person['name']}")
    else:
        print(f"   Error: {response.status_code}")


if __name__ == "__main__":
    try:
        test_search_functionality()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Make sure the server is running on http://localhost:8000")
        print("   You can start it with: cd api && make run")
    except Exception as e:
        print(f"❌ Error: {e}")
