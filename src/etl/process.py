from __future__ import annotations
from pathlib import Path
import pandas as pd
from .utils import load_json, dated_dir

KEEP = [
    "id", "name", "username", "email",
    "address.city",
    "company.name",
]

RENAME = {
    "id": "user_id",
    "address.city": "city",
    "company.name": "company",
}

def process_to_csv(raw_path: str | Path) -> Path:
    """Raw JSON (/users) to normalized CSV """
    payload = load_json(raw_path)
    rows = payload.get("data", [])
    df = pd.json_normalize(rows)

    df = df[KEEP].copy()
    df.rename(columns=RENAME, inplace=True)

    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce").astype("Int64")
    df["email"] = df["email"].astype(str).str.strip()
    df.dropna(subset=["user_id", "email"], inplace=True)

    df["email_domain"] = df["email"].str.split("@").str[-1].str.lower()
    df["username_len"] = df["username"].astype(str).str.len()

    out = dated_dir("data/processed") / "data.csv"
    df.to_csv(out, index=False)
    return out