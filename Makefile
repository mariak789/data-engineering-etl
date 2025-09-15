.PHONY: run clean run-pg stop-pg flow

# run ETL locally with SQLite
run:
	python run.py

# remove generated artifacts
clean:
	rm -rf data/raw/* data/processed/* reports/* local.db

# switch to ETL_DATABASE_URL
run-pg:
	docker compose up -d db
	ETL_DATABASE_URL=postgresql+psycopg2://etl:etl@localhost:5432/etl_db python run.py

stop-pg:
	docker compose down -v