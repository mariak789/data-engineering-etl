# Data Engineering Pipeline

## Stack
- Python 3.10+
- requests, pandas
- SQLAlchemy
- SQLite / PostgreSQL
- Prefect

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


### 2. With Docker + PostgreSQL
```bash
make stop-pg    # stop container if running
make run-pg     # start Postgres and run ETL


### Default connection:
- ETL_DATABASE_URL=postgresql+psycopg2://etl:etl@localhost:5434/etl_db

---

### Verify DB contents
```bash
psql "postgresql://etl:etl@localhost:5434/etl_db" -c '\dt'
psql "postgresql://etl:etl@localhost:5434/etl_db" -c 'SELECT COUNT(*) FROM users;'


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

### Raw JSON saved
![Raw JSON](docs/screenshots/raw_json.png)

---

### Processed CSV
![Processed CSV](docs/screenshots/processed_csv.png)

---

### SQLite table preview
![SQLite query and table](docs/screenshots/sqlite_table.png)


