#!/bin/bash

# Script to load Star Wars API data into the database
# This script runs the Python data loader from within the Docker container

set -e

echo "Starting SWAPI data loading process..."

# Check if we're running inside Docker container
if [ -f /.dockerenv ]; then
    echo "Running inside Docker container..."
    cd /app
    python docker/scripts/load_swapi_data.py
else
    echo "Running locally..."
    cd "$(dirname "$0")/../.."
    python docker/scripts/load_swapi_data.py
fi

echo "Data loading completed!" 