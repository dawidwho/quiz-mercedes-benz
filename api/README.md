# Mercedes-Benz Quiz API

A FastAPI-based quiz application for Mercedes-Benz enthusiasts.

## Quick Start with Make Commands

### Prerequisites

- Docker
- Docker Compose
- Make

### Setup

1. **Copy the environment file:**

   ```bash
   cp env.example ./../compose/.env
   ```

2. **Edit the `.env` file** with your desired configuration:

   ```bash
   # Application Settings
   APP_NAME=Mercedes-Benz Quiz API
   APP_VERSION=1.0.0
   APP_PORT=8000
   DEBUG=true

   # Security
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

   # Database Configuration
   DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
   POSTGRES_DB=quiz_db
   POSTGRES_USER=quiz_user
   POSTGRES_PASSWORD=quiz_password
   POSTGRES_PORT=5432

   ```

3. **Start the services:**

   ```bash
   make up
   ```

4. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Root Endpoint: http://localhost:8000/

### Available Services

- **FastAPI App**: Runs on port 8000 (configurable via APP_PORT)
- **PostgreSQL**: Database on port 5432 (configurable via POSTGRES_PORT)

### Environment Variables

All configuration is handled through environment variables in the `.env` file:

| Variable            | Description                   | Default                                     |
| ------------------- | ----------------------------- | ------------------------------------------- |
| `APP_NAME`          | Application name              | Mercedes-Benz Quiz API                      |
| `APP_VERSION`       | Application version           | 1.0.0                                       |
| `APP_PORT`          | Port for the FastAPI app      | 8000                                        |
| `DEBUG`             | Debug mode                    | true                                        |
| `SECRET_KEY`        | Secret key for security       | (required)                                  |
| `ALLOWED_HOSTS`     | Comma-separated allowed hosts | localhost,127.0.0.1,0.0.0.0                 |
| `CORS_ORIGINS`      | Comma-separated CORS origins  | http://localhost:3000,http://127.0.0.1:3000 |
| `DATABASE_URL`      | PostgreSQL connection string  | (auto-generated)                            |
| `POSTGRES_DB`       | PostgreSQL database name      | quiz_db                                     |
| `POSTGRES_USER`     | PostgreSQL username           | quiz_user                                   |
| `POSTGRES_PASSWORD` | PostgreSQL password           | quiz_password                               |
| `POSTGRES_PORT`     | PostgreSQL port               | 5432                                        |
| `STAR_WARS_API_URL` | Star Wars API base URL        | https://swapi.py4e.com/api/                 |

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /questions` - Get all quiz questions
- `GET /questions/{id}` - Get specific question
- `POST /submit-answer` - Submit quiz answer
- `GET /categories` - Get question categories

### Available Make Commands

Use these make commands to manage the application:

| Command         | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `make help`     | Show all available commands                                  |
| `make up`       | Start services in detached mode                              |
| `make run`      | Start services with logs (development mode)                  |
| `make down`     | Stop services                                                |
| `make logs`     | View service logs                                            |
| `make build`    | Build containers                                             |
| `make recreate` | Recreate containers with fresh volumes                       |
| `make clean`    | Stop services and remove all containers, images, and volumes |

### Development

To run in development mode with auto-reload:
