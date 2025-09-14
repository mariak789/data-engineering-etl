from __future__ import annotations
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_sqlite(csv_path: str | Path, db_path: str | Path = "local.db", table: str = "population") -> str:
    """load CSV to SQLite; if exists - rewrite the table"""
    df = pd.read_csv(csv_path)
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
    return str(db_path)