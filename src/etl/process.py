from __future__ import annotations
from pathlib import Path
import pandas as pd
from .utils import load_json, dated_dir

NEEDED = ["State", "Year", "Population"]

def process_to_csv(raw_path: str | Path) -> Path:
    """Get raw JSON → select fields → rename → clean → add population_mln → CSV"""
    payload = load_json(raw_path)
    rows = payload.get("data", [])
    df = pd.DataFrame(rows)

    df = df[NEEDED].copy()
    df.rename(columns={"State": "state", "Year": "year", "Population": "population"}, inplace=True)

    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df.dropna(subset=["state", "year", "population"], inplace=True)

    df["population_mln"] = df["population"] / 1_000_000

    out = dated_dir("data/processed") / "data.csv"
    df.to_csv(out, index=False)
    return out