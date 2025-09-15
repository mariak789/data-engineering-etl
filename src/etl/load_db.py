from __future__ import annotations
from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine


def get_active_db_url(db_path: str | Path = "local.db") -> str:
    """
    Return SQLAlchemy URL for the active DB:
    - If ETL_DATABASE_URL is set -> use it (Postgres)
    - Else fallback to local SQLite file.
    """
    db_url = os.getenv("ETL_DATABASE_URL")
    if db_url:
        return db_url
    return f"sqlite:///{db_path}"


def load_csv_to_db(
    csv_path: str | Path,
    db_path: str | Path = "local.db",
    table: str = "users",
) -> str:
    """
    Load CSV into the active DB and return the DB URL used.
    """
    df = pd.read_csv(csv_path)
    url = get_active_db_url(db_path)
    engine = create_engine(url)

    with engine.begin() as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)

    return url