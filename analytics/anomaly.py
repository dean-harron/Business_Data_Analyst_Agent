from __future__ import annotations
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.preprocessing import StandardScaler

class Autoencoder(nn.Module):
    def __init__(self, n_features: int):
        super().__init__()
        hidden = max(4, min(32, n_features * 2))
        latent = max(2, min(8, n_features))
        self.net = nn.Sequential(
            nn.Linear(n_features, hidden), nn.ReLU(),
            nn.Linear(hidden, latent), nn.ReLU(),
            nn.Linear(latent, hidden), nn.ReLU(),
            nn.Linear(hidden, n_features),
        )
    def forward(self, x):
        return self.net(x)


def detect_numeric_anomalies(df: pd.DataFrame, epochs: int = 60) -> pd.DataFrame:
    numeric = df.select_dtypes(include=np.number).copy()
    if numeric.shape[1] == 0 or len(numeric) < 10:
        out = df.copy()
        out["anomaly_score"] = 0.0
        out["is_anomaly"] = False
        return out
    numeric = numeric.replace([np.inf, -np.inf], np.nan).fillna(numeric.median(numeric_only=True))
    scaler = StandardScaler()
    x = torch.tensor(scaler.fit_transform(numeric), dtype=torch.float32)
    model = Autoencoder(x.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(epochs):
        opt.zero_grad()
        y = model(x)
        loss = ((y - x) ** 2).mean()
        loss.backward()
        opt.step()
    with torch.no_grad():
        scores = ((model(x) - x) ** 2).mean(dim=1).numpy()
    threshold = float(np.quantile(scores, 0.98))
    out = df.copy()
    out["anomaly_score"] = scores
    out["is_anomaly"] = scores >= threshold
    return out
