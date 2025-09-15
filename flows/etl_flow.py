from __future__ import annotations

from pathlib import Path
from prefect import flow, task

from src.etl.fetch import fetch_raw
from src.etl.process import process_to_csv
from src.etl.load_db import load_csv_to_db, get_active_db_url
from src.etl.analytics import run_queries


@task(name="t_fetch")
def t_fetch() -> Path:
    return fetch_raw()


@task(name="t_process")
def t_process(raw_path: Path) -> Path:
    return process_to_csv(raw_path)


@task(name="t_load")
def t_load(csv_path: Path) -> str:
    # returns DB URL actually used (Postgres if ETL_DATABASE_URL set, else SQLite)
    return load_csv_to_db(csv_path)


@task(name="t_analytics")
def t_analytics(db_url: str) -> Path:
    return run_queries(db_url)


@flow(name="mini-etl-flow")
def mini_etl_flow():
    raw = t_fetch()
    csv = t_process(raw)
    db_url = t_load(csv)
    report = t_analytics(db_url)

    return {"db_url": db_url, "report": str(report)}


if __name__ == "__main__":
    mini_etl_flow()