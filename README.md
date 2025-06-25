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

# To run

I like to use the following command: make clean && make up

- Warning: Command make clean is a "down -v --remove-orphans", so it removes all not used volumes

# Up

make up

# Run tests

make test

# Clean up everything (removes containers, volumes, images)

make clean

# Recreate services (down + up)

make recreate

# Access container shells

make api-shell # Access API container
make front-shell # Access frontend container
