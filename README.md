# quiz-mercedes-benz

This is a technical challenge from Mercedes Benz

## First Time Setup

Before running the application, you need to set up your environment variables for api and front:

1. Navigate to the `compose` folder
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file with your specific configuration values

## Available Commands

# Build both services

make build

# Run tests

make test

# Clean up everything (removes containers, volumes, images)

make clean

# Recreate services (down + up)

make recreate

# Access container shells

make api-shell # Access API container
make front-shell # Access frontend container
