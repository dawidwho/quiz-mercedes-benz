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
- `GET /api/people/` - Get all people with pagination, sorting, and search
- `GET /api/people/{id}` - Get specific person by ID
- `POST /api/people/` - Create new person
- `PUT /api/people/{id}` - Update person
- `DELETE /api/people/{id}` - Delete person
- `GET /api/planets/` - Get all planets with pagination, sorting, and search
- `GET /api/planets/{id}` - Get specific planet by ID
- `POST /api/planets/` - Create new planet
- `PUT /api/planets/{id}` - Update planet
- `DELETE /api/planets/{id}` - Delete planet
- `POST /api/simulate-ai-insight/` - Generate AI insights for people or planets
- `GET /api/simulate-ai-insight/` - Generate AI insights for people or planets (GET version)

### Monitoring and Logging

The application includes comprehensive monitoring and logging capabilities for tracking search and sort operations.

#### Monitoring Endpoints

- `GET /api/monitoring/metrics` - Get all monitoring metrics
- `GET /api/monitoring/metrics/search` - Get search-specific metrics
- `GET /api/monitoring/metrics/sort` - Get sort-specific metrics
- `GET /api/monitoring/health` - Get monitoring service health status

#### Logged Events

The system automatically logs the following events:

1. **Search Operations**:

   - Search parameters used
   - Results count and total count
   - Execution time
   - Resource type (people/planets)
   - Page and size information

2. **Sort Operations**:

   - Sort field and order
   - Results count and total count
   - Execution time
   - Resource type (people/planets)
   - Page and size information

3. **API Requests**:

   - HTTP method and path
   - Status code
   - Execution time
   - Client IP and user agent

4. **Errors**:
   - Error type and message
   - Request context
   - Stack trace information

#### Metrics Tracking

The monitoring system tracks:

- **Search Metrics**:

  - Total number of searches
  - Searches by resource type (people/planets)
  - Popular search terms
  - Average execution time

- **Sort Metrics**:
  - Total number of sorts
  - Sorts by resource type (people/planets)
  - Popular sort fields
  - Sort order distribution (asc/desc)
  - Average execution time

#### Example Usage

```bash
# Get all metrics
curl http://localhost:8000/api/monitoring/metrics

# Get search metrics only
curl http://localhost:8000/api/monitoring/metrics/search

# Get sort metrics only
curl http://localhost:8000/api/monitoring/metrics/sort

# Check monitoring health
curl http://localhost:8000/api/monitoring/health
```

#### Log Output

The application uses structured logging with loguru. Logs are written to both:

- Console (stdout)
- File (`app.log` with rotation)

Example log output:

```
INFO     Search event - app.core.monitoring:log_search_event:89
         event_type=search
         event_data={'event_type': 'search', 'timestamp': '2024-01-15T10:30:00', 'resource_type': 'people', 'search_params': {'name': 'Luke'}, 'results_count': 1, 'total_count': 1, 'page': 1, 'size': 10, 'execution_time_ms': 45.2}
         metrics={'total_searches': 5, 'searches_by_resource': {'people': 3, 'planets': 2}, 'popular_search_terms': {'name:luke': 2}, 'average_execution_time': 42.1}
```

#### Testing Monitoring

Run the monitoring test script to verify functionality:

```bash
python test_monitoring.py
```

This script will:

1. Perform sample search and sort operations
2. Test all monitoring endpoints
3. Display metrics and health information

### AI Insights Endpoint

The `/api/simulate-ai-insight/` endpoint simulates AI-generated descriptions for people and planets from the Star Wars universe.

#### Usage

**POST Method:**

```bash
curl -X POST "http://localhost:8000/api/simulate-ai-insight/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Luke Skywalker",
    "entity_type": "people"
  }'
```

**GET Method:**

```bash
curl "http://localhost:8000/api/simulate-ai-insight/?name=Luke%20Skywalker&entity_type=people"
```

#### Parameters

- `name` (string, required): The name of the person or planet
- `entity_type` (string, required): Either "people" or "planets"

#### Response Format

```json
{
  "name": "Luke Skywalker",
  "entity_type": "people",
  "insight": "Based on my analysis of Luke Skywalker's profile, this individual exhibits remarkable characteristics...",
  "confidence_score": 0.87,
  "generated_at": "2024-01-15T10:30:00",
  "model_version": "v1.0"
}
```

#### Features

- **Contextual Insights**: Generates realistic AI-like descriptions based on actual data from the database
- **Fallback Handling**: Provides generic insights for entities not found in the database
- **Confidence Scoring**: Returns realistic confidence scores (0.75-0.98 for found entities, 0.3 for not found)
- **Multiple Formats**: Supports both POST (JSON body) and GET (query parameters) methods
- **Error Handling**: Validates entity types and provides appropriate error messages

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
