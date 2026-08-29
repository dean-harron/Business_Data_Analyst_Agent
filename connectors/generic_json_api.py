from __future__ import annotations
import requests
import pandas as pd

def fetch_json_table(url: str, params: dict | None = None, records_path: str | None = None) -> pd.DataFrame:
    r=requests.get(url, params=params or {}, timeout=30)
    r.raise_for_status()
    data=r.json()
    if records_path:
        for part in records_path.split('.'):
            data=data[part]
    if not isinstance(data, list):
        raise ValueError("Expected a list of records")
    return pd.json_normalize(data)
