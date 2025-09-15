.PHONY: run clean run-pg stop-pg flow

# run ETL locally with SQLite
run:
	python run.py

# remove generated artifacts
clean:
	rm -rf data/raw/* data/processed/* reports/* local.db

# start PostgreSQL in Docker and run ETL against it (uses DATABASE_URL)
run-pg:
	docker compose up -d db
	DATABASE_URL=postgresql+psycopg2://etl:etl@localhost:5432/etl_db python run.py

# stop and remove PostgreSQL container/volume
stop-pg:
	docker compose down -v