from __future__ import annotations
import pandas as pd
import numpy as np


def correlation(df: pd.DataFrame) -> list[dict]:
    num = df.select_dtypes(include=np.number)
    if num.shape[1] < 2:
        return []
    corr = num.corr(numeric_only=True)
    rows=[]
    for i, a in enumerate(corr.columns):
        for j, b in enumerate(corr.columns):
            if j <= i: continue
            v = corr.loc[a,b]
            if pd.notna(v):
                rows.append({"a": str(a), "b": str(b), "correlation": float(v)})
    return sorted(rows, key=lambda x: abs(x["correlation"]), reverse=True)


def grouped_summary(df: pd.DataFrame, group_by: str, value: str) -> list[dict]:
    if group_by not in df.columns or value not in df.columns:
        raise KeyError("group_by/value column not found")
    return (df.groupby(group_by, dropna=False)[value]
              .agg(["count", "sum", "mean", "median"])
              .reset_index()
              .sort_values("sum", ascending=False)
              .to_dict(orient="records"))
