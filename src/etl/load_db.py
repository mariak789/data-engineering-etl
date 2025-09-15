from __future__ import annotations
from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine

def _engine_from_env_or_sqlite(db_path: str | Path = "local.db"):
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return create_engine(db_url)
    return create_engine(f"sqlite:///{db_path}")

def load_csv_to_sqlite(csv_path: str | Path, db_path: str | Path = "local.db", table: str = "users") -> str:
    """Load CSV into DB. Uses DATABASE_URL if set, otherwise local SQLite."""
    df = pd.read_csv(csv_path)
    engine = _engine_from_env_or_sqlite(db_path)
    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
    return str(db_path)