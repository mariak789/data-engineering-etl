from __future__ import annotations
from src.etl.fetch import fetch_raw
from src.etl.process import process_to_csv
from src.etl.load_db import load_csv_to_sqlite
from src.etl.analytics import run_queries

def main():
    print("1) Fetching raw data...")
    raw_path = fetch_raw()
    print(f"   Saved raw: {raw_path}")

    print("2) Processing → CSV...")
    csv_path = process_to_csv(raw_path)
    print(f"   Saved CSV: {csv_path}")

    print("3) Loading → SQLite...")
    db_path = load_csv_to_sqlite(csv_path)  
    print(f"   DB file: {db_path}")

    print("4) Running SQL analytics...")
    report_path = run_queries(db_path)      
    print(f"   Report: {report_path}")

    print("\nDone ✅")

if __name__ == "__main__":
    main()