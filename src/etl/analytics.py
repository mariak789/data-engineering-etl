from __future__ import annotations
from pathlib import Path
from sqlalchemy import create_engine, text
import json
from .utils import dated_dir

def run_queries(db_path: str | Path = "local.db", table: str = "population") -> Path:
    """GET latest year → AVG, COUNT DISTINCT, TOP-5 → save JSON-report."""
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.begin() as conn:
        latest_year = conn.execute(text(f"SELECT MAX(year) FROM {table}")).scalar_one()

        avg_pop = conn.execute(text(f"""
            SELECT ROUND(AVG(population), 2) AS avg_population
            FROM {table} WHERE year = :y
        """), {"y": latest_year}).mappings().one()

        unique_states = conn.execute(text(f"""
            SELECT COUNT(DISTINCT state) AS unique_states
            FROM {table} WHERE year = :y
        """), {"y": latest_year}).mappings().one()

        top5 = conn.execute(text(f"""
            SELECT state, population
            FROM {table} WHERE year = :y
            ORDER BY population DESC
            LIMIT 5
        """), {"y": latest_year}).mappings().all()

    report = {
        "year": int(latest_year),
        "avg_population": float(avg_pop["avg_population"]),
        "unique_states": int(unique_states["unique_states"]),
        "top5_states": [dict(r) for r in top5],
    }

    out = dated_dir("reports") / "report.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return out