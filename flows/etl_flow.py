from __future__ import annotations
from pathlib import Path
from prefect import flow, task
from src.etl.fetch import fetch_raw
from src.etl.process import process_to_csv
from src.etl.load_db import load_csv_to_sqlite
from src.etl.analytics import run_queries

@task
def t_fetch() -> Path:
    return fetch_raw()

@task
def t_process(raw_path: Path) -> Path:
    return process_to_csv(raw_path)

@task
def t_load(csv_path: Path) -> str:
    return load_csv_to_sqlite(csv_path)

@task
def t_analytics(db_path: str) -> Path:
    return run_queries(db_path)

@flow(name="mini-etl-flow")
def mini_etl_flow():
    raw = t_fetch()
    csv = t_process(raw)
    db  = t_load(csv)
    report = t_analytics(db)
    return str(report)

if __name__ == "__main__":
    mini_etl_flow()