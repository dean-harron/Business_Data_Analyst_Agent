from __future__ import annotations
import pandas as pd
import numpy as np


def profile_dataframe(df: pd.DataFrame) -> dict:
    profile = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(map(str, df.columns)),
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
        "missing": {str(k): int(v) for k, v in df.isna().sum().items()},
        "missing_pct": {str(k): float(v / max(len(df), 1) * 100) for k, v in df.isna().sum().items()},
        "duplicates": int(df.duplicated().sum()),
        "numeric_summary": {},
        "categorical_summary": {},
    }
    for col in df.select_dtypes(include=np.number).columns:
        s = df[col].dropna()
        profile["numeric_summary"][str(col)] = {
            "mean": float(s.mean()) if len(s) else None,
            "median": float(s.median()) if len(s) else None,
            "std": float(s.std()) if len(s) > 1 else 0.0,
            "min": float(s.min()) if len(s) else None,
            "max": float(s.max()) if len(s) else None,
        }
    for col in df.select_dtypes(exclude=np.number).columns:
        counts = df[col].astype(str).value_counts(dropna=False).head(10)
        profile["categorical_summary"][str(col)] = {str(k): int(v) for k, v in counts.items()}
    return profile
