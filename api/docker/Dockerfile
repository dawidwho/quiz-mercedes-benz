FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Make scripts executable
RUN chmod +x /app/docker/scripts/health_check.sh
RUN chmod +x /app/docker/scripts/load_swapi_data.sh

# Create entrypoint script
RUN echo '#!/bin/bash\n\
    set -e\n\
    \n\
    # Wait for database to be ready\n\
    echo "Waiting for database to be ready..."\n\
    while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do\n\
    echo "Database is not ready yet. Waiting..."\n\
    sleep 2\n\
    done\n\
    echo "Database is ready!"\n\
    \n\
    # Check if data loading is enabled\n\
    if [ "$LOAD_SWAPI_DATA" = "true" ]; then\n\
    echo "Loading SWAPI data..."\n\
    /app/docker/scripts/load_swapi_data.sh\n\
    else\n\
    echo "Skipping SWAPI data loading (LOAD_SWAPI_DATA not set to true)"\n\
    fi\n\
    \n\
    # Start the application\n\
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload\n\
    ' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"] 