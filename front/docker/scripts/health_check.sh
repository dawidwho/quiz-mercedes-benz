#!/bin/sh

# Health check for React Router dev server
# Check if the application is responding on port 5173

echo "Starting health check for React app on port 5173..."

# Try to connect to the application using 0.0.0.0 instead of localhost
if wget --no-verbose --tries=1 --spider http://0.0.0.0:5173/; then
    echo "Health check passed: React app is responding"
    exit 0
else
    echo "Health check failed: React app is not responding on port 5173"
    exit 1
fi 