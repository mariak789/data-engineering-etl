# Data Engineering Pipeline

## Stack
- Python 3.10+
- requests, pandas
- SQLAlchemy
- SQLite / PostgreSQL
- Prefect (bonus)

## API used
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/users)

## Fields Selected and Processed
- **Selected from API**:
  - `id`
  - `name`
  - `username`
  - `email`
  - `address.city`
  - `company.name`

- **Renamed**:
  - `id` → `user_id`
  - `address.city` → `city`
  - `company.name` → `company`

- **Cleaned**:
  - removed rows without `user_id` or `email`
  - trimmed spaces in `email`
  - converted `user_id` to integer

- **Enriched**:
  - `email_domain` (part after `@`)
  - `username_len` (length of username)

---

## Data flow
`JSONPlaceholder API` → **raw JSON** → clean/enrich → **CSV** → load to DB (SQLite/Postgres) → run SQL → **JSON report**.

---

## How to run

### 1. Local (SQLite)
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python run.py
```

### 2. With Docker + PostgreSQL
```bash
make stop-pg    # stop container if running
make run-pg     # start Postgres and run ETL
```

#### Default connection:
- ETL_DATABASE_URL=postgresql+psycopg2://etl:etl@localhost:5434/etl_db


#### Verify DB contents
```bash
docker compose exec -T db psql -U etl -d etl_db -c '\dt'
docker compose exec -T db psql -U etl -d etl_db -c 'SELECT COUNT(*) FROM users;'
```

---

### 3. Prefect Flow
```bash
python -m flows.etl_flow
```


## Artifacts

- **Raw data**: `data/raw/YYYY-MM-DD/response.json`
- **Processed data**: `data/processed/YYYY-MM-DD/data.csv`
- **Database**: `local.db` (SQLite database)
- **Reports**: `reports/YYYY-MM-DD/report.json`

## Screenshots

#### Raw JSON saved
![Raw JSON](docs/screenshots/raw_json.png)

#### Processed CSV
![Processed CSV](docs/screenshots/processed_csv.png)

#### SQLite table preview
![SQLite query and table](docs/screenshots/sqlite_table.png)

#### Report JSON
![Raw JSON](docs/screenshots/report_json.png)

---

### Troubleshooting
- Port conflict → set PG_PORT in .env (default 5434)
- Role/DB missing → run inside container:
```bash
docker compose exec -T db psql -U postgres -c "CREATE USER etl WITH PASSWORD 'etl';"
docker compose exec -T db psql -U postgres -c "CREATE DATABASE etl_db OWNER etl;"
docker compose exec -T db psql -U postgres -d etl_db -c "GRANT ALL PRIVILEGES ON DATABASE etl_db TO etl;"
```


### Optional Bonus
- Makefile for easy run/clean
- docker-compose.yml with PostgreSQL
- Mini Prefect DAG (flows/etl_flow.py)


