#!/bin/bash

# Health check script that exits the container if health fails
if ! curl -f http://localhost:8000/health; then
    echo "Health check failed - exiting container"
    exit 1
fi

echo "Health check passed"
exit 0 