from __future__ import annotations
import pandas as pd
import numpy as np


def linear_forecast(df: pd.DataFrame, date_col: str, value_col: str, periods: int = 6) -> list[dict]:
    temp = df[[date_col, value_col]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp[value_col] = pd.to_numeric(temp[value_col], errors="coerce")
    temp = temp.dropna().sort_values(date_col)
    if len(temp) < 3:
        raise ValueError("Need at least 3 observations")
    y = temp[value_col].to_numpy(dtype=float)
    x = np.arange(len(y), dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    future_x = np.arange(len(y), len(y)+periods)
    freq = pd.infer_freq(temp[date_col]) or "ME"
    future_dates = pd.date_range(temp[date_col].iloc[-1], periods=periods+1, freq=freq)[1:]
    return [{"date": d.strftime("%Y-%m-%d"), "forecast": float(intercept+slope*fx)} for d, fx in zip(future_dates, future_x)]
