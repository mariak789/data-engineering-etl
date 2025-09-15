from __future__ import annotations
from src.etl.fetch import fetch_raw
from src.etl.process import process_to_csv
from src.etl.load_db import load_csv_to_db, get_active_db_url
from src.etl.analytics import run_queries


def main():
    print("1) Fetching raw data...")
    raw_path = fetch_raw()
    print(f"   Saved raw: {raw_path}")

    print("2) Processing → CSV...")
    csv_path = process_to_csv(raw_path)
    print(f"   Saved CSV: {csv_path}")

    # Decide target DB from env
    db_url = get_active_db_url("local.db")
    target = "PostgreSQL" if db_url.startswith("postgresql") else "SQLite"

    print(f"3) Loading → {target}...")
    used_url = load_csv_to_db(csv_path)  # returns actual URL used
    if used_url.startswith("sqlite:///"):
        print(f"   DB file: {used_url.replace('sqlite:///','')}")
    else:
        print(f"   DB URL: {used_url}")

    print("4) Running SQL analytics...")
    report_path = run_queries(used_url)
    print(f"   Report: {report_path}")

    print("\nDone ✅")


if __name__ == "__main__":
    main()