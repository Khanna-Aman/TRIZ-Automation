COMPOSE?=11-02-docker-compose.yml

.PHONY: up down build logs ps restart restart-% import-triz

up:
	docker compose -f $(COMPOSE) up -d

e2e: build up

build:
	docker compose -f $(COMPOSE) build

down:
	docker compose -f $(COMPOSE) down

logs:
	docker compose -f $(COMPOSE) logs -f orchestrator

ps:
	docker compose -f $(COMPOSE) ps

restart:
	docker compose -f $(COMPOSE) up -d --force-recreate --no-deps orchestrator

restart-%:
	docker compose -f $(COMPOSE) up -d --force-recreate --no-deps $*

import-triz:
	@echo "Importing TRIZ sample data into Postgres..."
	POSTGRES_URL=postgresql://iia:iia@localhost:5432/iia \
		python services/triz/import_triz_matrix.py \
			--principles services/triz/sample/principles.json \
			--parameters services/triz/sample/parameters.json \
			--matrix services/triz/sample/matrix.csv

