.PHONY: help build up logs down shell migration-autogenerate migration-upgrade migration-downgrade

COMPOSE_FILE := ./config/docker/docker-compose.yml
APP_ENV_FILE := ./config/env/.env.app

export ENV_FILE = ../env/.env.app
export ${APP_ENV_FILE}

help: ## Shows help for each of the Makefile command.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Builds an application docker image.
	@docker build -f ./config/docker/Dockerfile -t post-service --build-arg GID=$(shell id -g) --build-arg UID=$(shell id -u) .

up: ## Starts the application.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) up -d

logs: ## Shows logs of the application container.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) logs -f app

down: ## Stops and removes application containers.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) down

shell: ## Connects to the application container shell.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) exec -it app sh

migration-autogenerate: ## Generates the alembic migration file.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) run --rm app-migration bash -c 'cd /app/migrations && alembic revision --autogenerate'

migration-upgrade: ## Runs migration files.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) run --rm app-migration bash -c 'cd /app/migrations && alembic upgrade head'

migration-downgrade: ## Runs downgrade operation for the last migration.
	@docker compose -f $(COMPOSE_FILE) --env-file $(APP_ENV_FILE) run --rm app-migration bash -c 'cd /app/migrations && alembic downgrade -1'
