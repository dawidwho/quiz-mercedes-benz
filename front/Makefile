.PHONY: help up down logs build run test clean docker-build docker-run docker-stop shell

help:
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up:
	docker-compose -f compose/docker-compose.yml up -d

recreate:
	docker-compose -f compose/docker-compose.yml down -v
	docker-compose -f compose/docker-compose.yml up -d

down:
	docker-compose -f compose/docker-compose.yml down

logs:
	docker-compose -f compose/docker-compose.yml logs -f

build:
	docker-compose -f compose/docker-compose.yml build

run:
	docker-compose -f compose/docker-compose.yml up

dev:
	cd app && npm run dev

test:
	@echo "Running tests..."
	cd app && npm run typecheck

shell:
	docker-compose -f compose/docker-compose.yml exec react-app /bin/sh

clean:
	docker-compose -f compose/docker-compose.yml down -v
	docker-compose -f compose/docker-compose.yml down --rmi all --volumes --remove-orphans