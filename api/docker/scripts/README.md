# Docker Scripts

This directory contains utility scripts for the API container.

## Scripts

### `health_check.sh`

Health check script that verifies the API is running and exits the container if health fails.

### `load_swapi_data.py`

Python script to load people and planets data from the Star Wars API (SWAPI) into the database.
**Note**: This version relies on the app module structure and may have import issues in Docker.

### `load_swapi_data.sh`

Shell script wrapper for the Python data loader (now uses the standalone version).

### `create_tables.py`

Simple script to create database tables manually without loading data.

## Usage

### Loading SWAPI Data

#### Option 1: Automatic Loading via Docker (Recommended)

The data loading script is now integrated into the Docker container startup process. To enable automatic data loading:

1. **Set the environment variable in your `.env` file:**

   ```bash
   LOAD_SWAPI_DATA=true
   ```

2. **Start the containers:**
   ```bash
   docker-compose up
   ```

The container will:

- Wait for the database to be ready
- Create database tables (if they don't exist)
- Load SWAPI data if `LOAD_SWAPI_DATA=true` (using the standalone script)
- Start the FastAPI application

#### Option 2: Manual Execution

To load Star Wars data into your database manually, you can use either:

1. **Using the shell wrapper (recommended):**

   ```bash
   ./docker/scripts/load_swapi_data.sh
   ```

2. **Direct Python execution (standalone version):**

   ```bash
   python docker/scripts/load_swapi_data.py
   ```

3. **From within a running Docker container:**
   ```bash
   docker exec -it <container_name> ./docker/scripts/load_swapi_data.sh
   ```

### Database Migrations

#### Creating Tables Only

If you only want to create the database tables without loading data:

```bash
# From within a running Docker container
docker exec -it <container_name> python docker/scripts/create_tables.py
```

#### Manual Migration Steps

If you encounter table-related errors, you can run these steps manually:

1. **Create tables:**

   ```bash
   docker exec -it <container_name> python docker/scripts/create_tables.py
   ```

2. **Load data:**
   ```bash
   docker exec -it <container_name> python docker/scripts/load_swapi_data.py
   ```

This will show you:

- The Python path
- Current working directory
- Status of each import

### What the script does:

1. **Creates database tables** (if they don't exist)
2. **Fetches data from SWAPI endpoints:**

   - `https://swapi.py4e.com/api/people/` - All people/characters
   - `https://swapi.py4e.com/api/planets/` - All planets

3. **Transforms the data** to match your database schema

4. **Inserts the data** into your local database using the existing CRUD operations

5. **Provides progress feedback** showing which records are being inserted

### Requirements

- The API container must be running
- Database must be accessible
- `requests` library (added to requirements.txt)

### Environment Variables

- `LOAD_SWAPI_DATA`: Set to `true` to enable automatic data loading on container startup (default: `false`)
- `DATABASE_URL`: Database connection string (automatically set in Docker)

### Data Mapping

The script maps SWAPI fields to your database schema:

**People:**

- `name` → `name`
- `height` → `height`
- `mass` → `mass`
- `hair_color` → `hair_color`
- `skin_color` → `skin_color`
- `eye_color` → `eye_color`
- `birth_year` → `birth_year`
- `gender` → `gender`

**Planets:**

- `name` → `name`
- `diameter` → `diameter`
- `rotation_period` → `rotation_period`
- `orbital_period` → `orbital_period`
- `gravity` → `gravity`
- `population` → `population`
- `climate` → `climate`
- `terrain` → `terrain`
- `surface_water` → `surface_water`

### Error Handling

The script includes error handling for:

- Network timeouts and connection issues
- Database insertion errors
- Invalid data transformations

If any record fails to insert, the script will continue with the next record and report the error.

### Troubleshooting

#### Table Does Not Exist Errors

If you see `relation "planets" does not exist` or similar errors:

1. **Create tables manually:**

   ```bash
   docker exec -it <container_name> python docker/scripts/create_tables.py
   ```

2. **Then run the data loader:**
   ```bash
   docker exec -it <container_name> python docker/scripts/load_swapi_data.py
   ```

#### Import Errors

If you see `ModuleNotFoundError: No module named 'app'`:

1. **Use the standalone version** (recommended):

   ```bash
   python docker/scripts/load_swapi_data.py
   ```

2. **Check if you're running from the correct directory:**

   ```bash
   docker exec -it <container_name> pwd
   # Should show: /app
   ```

3. **Verify the app directory structure:**
   ```bash
   docker exec -it <container_name> ls -la /app
   ```

#### Database Connection Issues

If the script can't connect to the database:

1. **Check if the database is running:**

   ```bash
   docker-compose ps
   ```

2. **Check database logs:**

   ```bash
   docker-compose logs postgres
   ```

3. **Verify environment variables:**
   ```bash
   docker exec -it <container_name> env | grep POSTGRES
   ```

### Script Versions

#### Original Version (`load_swapi_data.py`)

- Uses the app module structure
- May have import issues in Docker containers
- Requires proper Python path setup

### Docker Integration Details

The Dockerfile now includes:

- An entrypoint script that waits for the database to be ready
- Conditional execution of the data loading script based on `LOAD_SWAPI_DATA` environment variable
- Proper script permissions and execution setup
- Database table creation is handled by the standalone script
