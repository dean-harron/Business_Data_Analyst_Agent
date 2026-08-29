from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def build_core_charts(df: pd.DataFrame, output_dir: str) -> list[str]:
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    paths=[]
    numeric = list(df.select_dtypes(include="number").columns)
    if numeric:
        col=numeric[0]
        p=out / "distribution.png"
        plt.figure(figsize=(8,4.5))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribution of {col}")
        plt.tight_layout(); plt.savefig(p, dpi=180); plt.close(); paths.append(str(p))
    if len(numeric)>=2:
        p=out / "correlation_heatmap.png"
        plt.figure(figsize=(7,5))
        sns.heatmap(df[numeric].corr(), annot=True, fmt=".2f", cmap="vlag", center=0)
        plt.title("Numeric Correlation Matrix")
        plt.tight_layout(); plt.savefig(p, dpi=180); plt.close(); paths.append(str(p))
    return paths


def chart_grouped(rows: list[dict], group_col: str, value_col: str, output_dir: str) -> str:
    out=Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    df=pd.DataFrame(rows)
    p=out / f"grouped_{group_col}_{value_col}.png"
    plt.figure(figsize=(9,5))
    sns.barplot(data=df, x=group_col, y="sum")
    plt.xticks(rotation=35, ha="right")
    plt.title(f"{value_col} by {group_col}")
    plt.tight_layout(); plt.savefig(p, dpi=180); plt.close()
    return str(p)
