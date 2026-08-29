from pathlib import Path
import pandas as pd

SUPPORTED = {".csv", ".xlsx", ".xls", ".parquet"}

def load_table(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if p.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {p.suffix}")
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p)
    return pd.read_parquet(p)
