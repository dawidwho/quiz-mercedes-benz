# Quiz Mercedes Benz API

A FastAPI-based REST API with a clean, modular structure.

## Project Structure

```
api/app/
├── main.py              # FastAPI application entry point
├── health.py            # Health check endpoints
├── api/                 # API layer
│   ├── deps.py          # Common dependencies
│   ├── schemas.py       # Pydantic models
│   ├── crud.py          # CRUD operations
│   └── routers/         # API endpoints
│       ├── people.py    # People endpoints
│       └── planets.py   # Planets endpoints
├── core/                # Core functionality
│   ├── config.py        # Application settings
│   ├── security.py      # Authentication & security
│   └── logging.py       # Logging configuration
├── db/                  # Database layer
│   ├── base.py          # SQLAlchemy base
│   ├── models.py        # Database models
│   ├── session.py       # Database session
│   └── init_db.py       # Database initialization
└── tests/               # Test suite
    ├── conftest.py      # Pytest configuration
    ├── test_people.py   # People endpoint tests
    └── test_planets.py  # Planets endpoint tests
```

## Features

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation
- **Pytest**: Testing framework
- **Loguru**: Structured logging
- **JWT**: Authentication support
- **CORS**: Cross-origin resource sharing

## API Endpoints

### Base URLs

- **API Documentation**: `/api/docs`
- **Health Check**: `/health`
- **Root**: `/`

### People Endpoints

- `GET /api/people/` - List all people
- `POST /api/people/` - Create new person
- `GET /api/people/{id}` - Get person by ID
- `PUT /api/people/{id}` - Update person
- `DELETE /api/people/{id}` - Delete person

### Planets Endpoints

- `GET /api/planets/` - List all planets
- `POST /api/planets/` - Create new planet
- `GET /api/planets/{id}` - Get planet by ID
- `PUT /api/planets/{id}` - Update planet
- `DELETE /api/planets/{id}` - Delete planet

## Database Configuration

The application supports both SQLite (for local development) and PostgreSQL (for production/Docker).

### Option 1: SQLite (Local Development)

```env
DATABASE_URL=sqlite:///./app.db
```

### Option 2: PostgreSQL (Docker/Production)

```env
DATABASE_URL=postgresql://quiz_user:quiz_password@postgres:5432/quiz_db
POSTGRES_DB=quiz_db
POSTGRES_USER=quiz_user
POSTGRES_PASSWORD=quiz_password
POSTGRES_PORT=5432
```

## Configuration

Environment variables can be set in a `.env` file:

```env
PROJECT_NAME=Quiz Mercedes Benz API
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here
BACKEND_CORS_ORIGINS=["*"]
STAR_WARS_API_URL=https://swapi.dev/api/
```

## Running the Application

### Docker (PostgreSQL)

1. Navigate to the compose directory:

```bash
cd api/compose
```

2. Start the services:

```bash
docker-compose up
```

3. Access the API documentation:
   - Swagger UI: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

## Running Tests

```bash
cd api
pytest app/tests/ -v
```

## Customization

To add new models:

1. Update `db/models.py` with your new model
2. Add schemas in `api/schemas.py`
3. Create a new router in `api/routers/`
4. Include the router in `main.py`
5. Add tests in `tests/`

## Database

The application automatically creates tables on startup. Supported databases:

- **SQLite**: Default for local development
- **PostgreSQL**: Recommended for production/Docker

## Dependencies

Key dependencies include:

- `fastapi==0.104.1` - Web framework
- `pydantic==2.5.0` - Data validation
- `pydantic-settings==2.1.0` - Settings management
- `sqlalchemy==2.0.23` - Database ORM
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `loguru==0.7.2` - Logging
- `python-jose[cryptography]==3.3.0` - JWT handling
- `passlib[bcrypt]==1.7.4` - Password hashing

## Troubleshooting

### Database Connection Issues

#### PostgreSQL Connection Error

If you see "no password supplied" error:

1. Ensure PostgreSQL is running
2. Check your `.env` file has correct credentials
3. For Docker: Make sure both app and database containers are running

#### SQLite Issues

For local development, ensure you have write permissions in the api directory.

### Pydantic Import Errors

If you encounter `PydanticImportError` related to `BaseSettings`, ensure you have `pydantic-settings` installed:

```bash
pip install pydantic-settings==2.1.0
```

### Database Issues

If you encounter database-related errors, ensure SQLAlchemy is properly installed:

```bash
pip install sqlalchemy==2.0.23
```
