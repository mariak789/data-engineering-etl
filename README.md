# Data Engineering Pipeline

## Stack
Python 3.10+, requests, pandas, SQLAlchemy, SQLite.

## Data flow
JSONPlaceholder API → save raw JSON → clean/enrich → save CSV → load to SQLite → run SQL → `reports/report.json`.

## How to run
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py

## Artifacts

- **Raw data**: `data/raw/YYYY-MM-DD/response.json`
- **Processed data**: `data/processed/YYYY-MM-DD/data.csv`
- **Database**: `local.db` (SQLite database)
- **Reports**: `reports/YYYY-MM-DD/report.json`

## Source

- Source API: https://jsonplaceholder.typicode.com/users (public fake API, no key).
- Kept fields: user_id, name, username, email, city, company.
- Calculated fields: email_domain, username_len.