#!/usr/bin/env python3
"""
Test script for monitoring and logging functionality.
"""

import requests
import time
import json
from typing import Dict, Any

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"


def test_search_operations():
    """Test search operations and verify logging."""
    print("Testing search operations...")

    # Test people search
    search_params = {"name": "Luke", "page": 1, "size": 10}

    response = requests.get(f"{BASE_URL}/people/", params=search_params)
    print(f"People search response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")

    if response.status_code == 200:
        data = response.json()
        print(f"Found {data.get('total', 0)} people matching 'Luke'")

    # Test planets search
    planet_search_params = {"name": "Tatooine", "page": 1, "size": 10}

    response = requests.get(f"{BASE_URL}/planets/", params=planet_search_params)
    print(f"Planets search response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Found {data.get('total', 0)} planets matching 'Tatooine'")


def test_sort_operations():
    """Test sort operations and verify logging."""
    print("\nTesting sort operations...")

    # Test people sorting
    sort_params = {"sort_by": "name", "sort_order": "asc", "page": 1, "size": 10}

    response = requests.get(f"{BASE_URL}/people/", params=sort_params)
    print(f"People sort response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Retrieved {len(data.get('items', []))} people sorted by name")

    # Test planets sorting
    planet_sort_params = {
        "sort_by": "population",
        "sort_order": "desc",
        "page": 1,
        "size": 10,
    }

    response = requests.get(f"{BASE_URL}/planets/", params=planet_sort_params)
    print(f"Planets sort response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Retrieved {len(data.get('items', []))} planets sorted by population")


def test_monitoring_endpoints():
    """Test monitoring endpoints."""
    print("\nTesting monitoring endpoints...")

    # Test metrics endpoint
    try:
        response = requests.get(f"{BASE_URL}/monitoring/metrics")
        print(f"Metrics endpoint status: {response.status_code}")

        if response.status_code == 200:
            metrics = response.json()
            print("Metrics retrieved successfully:")
            print(f"  Search metrics: {metrics.get('search_metrics', {})}")
            print(f"  Sort metrics: {metrics.get('sort_metrics', {})}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error accessing metrics endpoint: {e}")

    # Test search metrics endpoint
    try:
        response = requests.get(f"{BASE_URL}/monitoring/metrics/search")
        print(f"Search metrics endpoint status: {response.status_code}")

        if response.status_code == 200:
            search_metrics = response.json()
            print(f"Search metrics: {json.dumps(search_metrics, indent=2)}")
    except Exception as e:
        print(f"Error accessing search metrics endpoint: {e}")

    # Test sort metrics endpoint
    try:
        response = requests.get(f"{BASE_URL}/monitoring/metrics/sort")
        print(f"Sort metrics endpoint status: {response.status_code}")

        if response.status_code == 200:
            sort_metrics = response.json()
            print(f"Sort metrics: {json.dumps(sort_metrics, indent=2)}")
    except Exception as e:
        print(f"Error accessing sort metrics endpoint: {e}")


def test_monitoring_health():
    """Test monitoring health endpoint."""
    print("\nTesting monitoring health...")

    try:
        response = requests.get(f"{BASE_URL}/monitoring/health")
        print(f"Monitoring health status: {response.status_code}")

        if response.status_code == 200:
            health = response.json()
            print(f"Monitoring health: {json.dumps(health, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error accessing monitoring health endpoint: {e}")


def main():
    """Run all monitoring tests."""
    print("Starting monitoring and logging tests...")
    print("=" * 50)

    # Wait a moment for the server to be ready
    time.sleep(2)

    try:
        # Test basic operations
        test_search_operations()
        test_sort_operations()

        # Wait a moment for logs to be processed
        time.sleep(1)

        # Test monitoring endpoints
        test_monitoring_endpoints()
        test_monitoring_health()

        print("\n" + "=" * 50)
        print("Monitoring tests completed!")
        print("\nCheck the application logs to see the structured logging output.")
        print("You can also access the monitoring endpoints to view metrics.")

    except Exception as e:
        print(f"Error during testing: {e}")
        print("Make sure the API server is running on http://localhost:8000")


if __name__ == "__main__":
    main()
