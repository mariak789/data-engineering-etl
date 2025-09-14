from __future__ import annotations
import requests
from pathlib import Path
from .utils import dated_dir, save_json

BASE_URL = "https://jsonplaceholder.typicode.com/users"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_raw() -> Path:
    """GET users from JSONPlaceholder and save in data/raw/YYYY-MM-DD/response.json"""
    r = requests.get(BASE_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list) or not data:
        raise RuntimeError("Unexpected payload shape from JSONPlaceholder /users")
    out = dated_dir("data/raw") / "response.json"
    save_json({"source_url": r.url, "data": data}, out)
    return out