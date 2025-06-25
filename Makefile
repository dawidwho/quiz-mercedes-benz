.PHONY: help up down logs build run test clean docker-build docker-run docker-stop shell api-up api-down api-logs api-build api-run api-dev api-test api-shell api-clean front-up front-down front-logs front-build front-run front-dev front-test front-shell front-clean

help:
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@echo '  Combined targets:'
	@echo '    up              - Start both API and frontend services'
	@echo '    down            - Stop both API and frontend services'
	@echo '    logs            - Show logs from both services'
	@echo '    build           - Build both API and frontend services'
	@echo '    run             - Run both services in foreground'
	@echo '    test            - Run tests for both services'
	@echo '    clean           - Clean up both services'
	@echo '  API targets:'
	@echo '    api-up          - Start API service only'
	@echo '    api-down        - Stop API service only'
	@echo '    api-logs        - Show API logs'
	@echo '    api-build       - Build API service'
	@echo '    api-run         - Run API service in foreground'
	@echo '    api-dev         - Run API in development mode'
	@echo '    api-test        - Run API tests'
	@echo '    api-shell       - Access API container shell'
	@echo '    api-clean       - Clean up API service'
	@echo '  Frontend targets:'
	@echo '    front-up        - Start frontend service only'
	@echo '    front-down      - Stop frontend service only'
	@echo '    front-logs      - Show frontend logs'
	@echo '    front-build     - Build frontend service'
	@echo '    front-run       - Run frontend service in foreground'
	@echo '    front-dev       - Run frontend in development mode'
	@echo '    front-test      - Run frontend tests'
	@echo '    front-shell     - Access frontend container shell'
	@echo '    front-clean     - Clean up frontend service'

# Combined targets
up: api-up front-up

down: api-down front-down

logs:
	@echo "=== API Logs ==="
	@make api-logs
	@echo ""
	@echo "=== Frontend Logs ==="
	@make front-logs

build: api-build front-build

run: api-run front-run

test: api-test front-test

clean: api-clean front-clean clean-all

# API targets
api-up:
	@echo "Starting API service..."
	cd api && make up

api-down:
	@echo "Stopping API service..."
	cd api && make down

api-logs:
	cd api && make logs

api-build:
	@echo "Building API service..."
	cd api && make build

api-run:
	cd api && make run

api-dev:
	@echo "Starting API in development mode..."
	cd api && make dev

api-test:
	@echo "Running API tests..."
	cd api && make test

api-shell:
	cd api && make shell

api-clean:
	@echo "Cleaning up API service..."
	cd api && make clean

# Frontend targets
front-up:
	@echo "Starting frontend service..."
	cd front && make up

front-up-6969:
	@echo "Starting frontend service on port 6969..."
	cd front && FRONTEND_PORT=6969 make up

front-down:
	@echo "Stopping frontend service..."
	cd front && make down

front-logs:
	cd front && make logs

front-build:
	@echo "Building frontend service..."
	cd front && make build

front-run:
	cd front && make run

front-dev:
	@echo "Starting frontend in development mode..."
	cd front && make dev

front-test:
	@echo "Running frontend tests..."
	cd front && make test

front-shell:
	cd front && make shell

front-clean:
	@echo "Cleaning up frontend service..."
	cd front && make clean

# Additional utility targets
# TODO: This is a hack to clean all containers and volumes, it should be improved
clean-all:
	@echo "Cleaning all containers and volumes..."
	cd front && docker-compose -f compose/docker-compose.yml down --rmi all --volumes --remove-orphans
	cd api && docker-compose -f compose/docker-compose.yml down --rmi all --volumes --remove-orphans
	cd front && docker volume prune -f
	cd api && docker volume prune -f

recreate: down up

recreate-6969: down front-up-6969
