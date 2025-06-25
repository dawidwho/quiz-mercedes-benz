#!/usr/bin/env python3
"""
Simple test script for the AI insights endpoint.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api"


def test_ai_insights():
    """Test the AI insights endpoint."""

    print("Testing AI Insights Endpoint")
    print("=" * 50)

    # Test 1: AI insight for people (POST)
    print("\n1. Testing AI insight for people (POST)")
    people_request = {"name": "Luke Skywalker", "entity_type": "people"}

    try:
        response = requests.post(
            f"{BASE_URL}/simulate-ai-insight/", json=people_request
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Name: {data['name']}")
            print(f"Entity Type: {data['entity_type']}")
            print(f"Confidence Score: {data['confidence_score']}")
            print(f"Model Version: {data['model_version']}")
            print(f"Insight: {data['insight'][:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: AI insight for planets (POST)
    print("\n2. Testing AI insight for planets (POST)")
    planets_request = {"name": "Tatooine", "entity_type": "planets"}

    try:
        response = requests.post(
            f"{BASE_URL}/simulate-ai-insight/", json=planets_request
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Name: {data['name']}")
            print(f"Entity Type: {data['entity_type']}")
            print(f"Confidence Score: {data['confidence_score']}")
            print(f"Model Version: {data['model_version']}")
            print(f"Insight: {data['insight'][:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 3: AI insight for people (GET)
    print("\n3. Testing AI insight for people (GET)")
    try:
        response = requests.get(
            f"{BASE_URL}/simulate-ai-insight/?name=Leia%20Organa&entity_type=people"
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Name: {data['name']}")
            print(f"Entity Type: {data['entity_type']}")
            print(f"Confidence Score: {data['confidence_score']}")
            print(f"Model Version: {data['model_version']}")
            print(f"Insight: {data['insight'][:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 4: AI insight for non-existent entity
    print("\n4. Testing AI insight for non-existent entity")
    nonexistent_request = {"name": "Nonexistent Person", "entity_type": "people"}

    try:
        response = requests.post(
            f"{BASE_URL}/simulate-ai-insight/", json=nonexistent_request
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Name: {data['name']}")
            print(f"Entity Type: {data['entity_type']}")
            print(f"Confidence Score: {data['confidence_score']}")
            print(f"Model Version: {data['model_version']}")
            print(f"Insight: {data['insight'][:100]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 5: Invalid entity type
    print("\n5. Testing invalid entity type")
    invalid_request = {"name": "Test", "entity_type": "invalid_type"}

    try:
        response = requests.post(
            f"{BASE_URL}/simulate-ai-insight/", json=invalid_request
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print(f"Error: {response.json()['detail']}")
        else:
            print(f"Unexpected response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_ai_insights()
