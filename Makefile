PG_PORT ?= 5434

.PHONY: run clean run-pg stop-pg flow

# run ETL locally with SQLite
run:
	python run.py

# remove generated artifacts
clean:
	rm -rf data/raw/* data/processed/* reports/* local.db

run-pg:
	docker compose up -d db
	@echo "Waiting for Postgres to be healthy..."
	@cid=$$(docker compose ps -q db); \
	i=0; \
	while [ "$$(docker inspect -f '{{.State.Health.Status}}' $$cid)" != "healthy" ]; do \
		i=$$((i+1)); \
		if [ $$i -gt 120 ]; then echo "\nTimeout waiting for Postgres health" && exit 1; fi; \
		sleep 1; printf "."; \
	done; echo
	ETL_DATABASE_URL=postgresql+psycopg2://etl:etl@localhost:$(PG_PORT)/etl_db python run.py
	
stop-pg:
	docker compose down -v