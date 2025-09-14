from __future__ import annotations
from pathlib import Path
from sqlalchemy import create_engine, text
import json
from .utils import dated_dir

def run_queries(db_path: str | Path = "local.db", table: str = "users") -> Path:
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.begin() as conn:
        avg_username_len = conn.execute(text(f"""
            SELECT ROUND(AVG(username_len), 2) AS avg_username_len
            FROM {table}
        """)).mappings().one()

        unique_cities = conn.execute(text(f"""
            SELECT COUNT(DISTINCT city) AS unique_cities
            FROM {table}
            WHERE city IS NOT NULL AND city <> ''
        """)).mappings().one()

        top_companies = conn.execute(text(f"""
            SELECT company, COUNT(*) AS users_count
            FROM {table}
            GROUP BY company
            ORDER BY users_count DESC, company ASC
            LIMIT 5
        """)).mappings().all()

    report = {
        "avg_username_len": float(avg_username_len["avg_username_len"]),
        "unique_cities": int(unique_cities["unique_cities"]),
        "top_companies_by_users": [dict(r) for r in top_companies],
    }

    out = dated_dir("reports") / "report.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return out