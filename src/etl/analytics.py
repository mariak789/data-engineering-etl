from __future__ import annotations
from pathlib import Path
from sqlalchemy import create_engine, text
import json
from datetime import date


def run_queries(db_url: str, table: str = "users", out_dir: str | Path = "reports") -> Path:
    """
    Run SQL analytics against the provided DB URL (Postgres or SQLite)
    and write a JSON report. Returns path to the report.
    """
    out_dir = Path(out_dir) / date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "report.json"

    engine = create_engine(db_url)

    queries = {
    "avg_username_len": f"""
        SELECT AVG(LENGTH(username)) AS avg_len
        FROM {table}
    """,
    "unique_cities": f"""
        SELECT COUNT(DISTINCT city) AS cnt
        FROM {table}
        WHERE city IS NOT NULL AND city <> ''
    """,
    "top_companies": f"""
        SELECT company, COUNT(*) AS users_count
        FROM {table}
        GROUP BY company
        ORDER BY users_count DESC, company ASC
        LIMIT 5
    """,
}

    result = {}
    with engine.begin() as conn:
        # avg_username_len (single row)
        row = conn.execute(text(queries["avg_username_len"])).mappings().one()
        result["avg_username_len"] = float(row["avg_len"]) if row["avg_len"] is not None else 0.0

        # unique_cities (single row)
        row = conn.execute(text(queries["unique_cities"])).mappings().one()
        result["unique_cities"] = int(row["cnt"])

        # top_companies (list)
        rows = conn.execute(text(queries["top_companies"])).mappings().all()
        result["top_companies_by_users"] = [dict(r) for r in rows]

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return out_path