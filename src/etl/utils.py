from __future__ import annotations
from pathlib import Path
from datetime import date
import json

def today_str() -> str:
    return date.today().strftime("%Y-%m-%d")

def dated_dir(root: str | Path) -> Path:
    p = Path(root) / today_str()
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_json(obj, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def load_json(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)