from __future__ import annotations
import requests
from pathlib import Path
from .utils import dated_dir, save_json

BASE_URL = "https://datausa.io/api/data"

def fetch_raw() -> Path:
    """GET last population data through states and save in data/raw/YYYY-MM-DD/response.json"""
    params = {"drilldowns": "State", "measures": "Population", "year": "latest"}
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    out = dated_dir("data/raw") / "response.json"
    save_json(r.json(), out)
    return out