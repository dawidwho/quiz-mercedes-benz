#!/bin/sh

# Health check for React Router dev server
# Check if the application is responding on port 6969

if wget --no-verbose --tries=1 --spider http://localhost:6969/; then
    echo "Health check passed: React app is responding"
    exit 0
else
    echo "Health check failed: React app is not responding"
    exit 1
fi 