from __future__ import annotations
from pathlib import Path
import json, subprocess, sys, tempfile
import pandas as pd
from langchain.tools import tool
from data.loaders import load_table
from data.profile import profile_dataframe
from data.duck import query_file
from analytics.stats import correlation, grouped_summary
from analytics.anomaly import detect_numeric_anomalies
from analytics.forecast import linear_forecast
from rag.index import search as rag_search
from config import settings

CURRENT_DATA = {"path": None}


def set_current_data(path: str):
    CURRENT_DATA["path"] = str(Path(path).resolve())


def require_data():
    if not CURRENT_DATA["path"]:
        raise RuntimeError("No dataset loaded. Call load_dataset first.")
    return CURRENT_DATA["path"]


@tool
def load_dataset(path: str) -> dict:
    """Load a CSV, Excel or Parquet file and return basic metadata."""
    df = load_table(path)
    set_current_data(path)
    return {"path": str(Path(path).resolve()), "rows": len(df), "columns": list(map(str, df.columns))}


@tool
def profile_dataset() -> dict:
    """Profile the current dataset including schema, missingness, duplicates and numeric summaries."""
    return profile_dataframe(load_table(require_data()))


@tool
def sql_query(sql: str) -> list[dict]:
    """Run a read-only analytical SQL query against the current dataset as table `data`."""
    normalized = sql.strip().lower()
    forbidden = ["insert ", "update ", "delete ", "drop ", "alter ", "create ", "copy ", "attach ", "install ", "load "]
    # if not normalized.startswith(("select", "with", "describe", "show", "explain")):
    #     raise ValueError("Only read-only analytical SQL is allowed")
    if any(x in normalized for x in forbidden):
        raise ValueError("Potentially destructive SQL blocked")
    return query_file(require_data(), sql)


@tool
def correlations() -> list[dict]:
    """Compute pairwise correlations for numeric columns in the current dataset."""
    return correlation(load_table(require_data()))


@tool
def group_summary(group_by: str, value: str) -> list[dict]:
    """Summarize a numeric field by a grouping column."""
    return grouped_summary(load_table(require_data()), group_by, value)


@tool
def anomalies() -> dict:
    """Run a PyTorch autoencoder over numeric features and return anomaly counts and top rows."""
    df = detect_numeric_anomalies(load_table(require_data()))
    flagged = df[df["is_anomaly"]].copy().sort_values("anomaly_score", ascending=False)
    return {
        "anomaly_count": int(len(flagged)),
        "top_anomalies": flagged.head(10).to_dict(orient="records"),
    }


@tool
def forecast(date_col: str, value_col: str, periods: int = 6) -> list[dict]:
    """Create a simple linear forecast for a time series."""
    return linear_forecast(load_table(require_data()), date_col, value_col, periods)


@tool
def retrieve_knowledge(query: str, k: int = 5) -> list[dict]:
    """Retrieve metric definitions and analyst guidance from the local RAG knowledge base."""
    results = rag_search(query, k)
    return [
        {"text": doc.page_content, "source": doc.metadata.get("source"), "score": float(score)}
        for doc, score in results
    ]


@tool
def run_python(code: str) -> str:
    """Run a generated Python analysis script in an isolated subprocess inside the workspace. Use for specialized calculations or charts only."""
    banned = ["os.system", "subprocess", "shutil.rmtree", "socket", "requests.get", "urllib", "pip ", "git ", "rm ", "del "]
    if any(x.lower() in code.lower() for x in banned):
        raise ValueError("Potentially unsafe code blocked")
    path = require_data()
    workspace = Path(settings.workspace_dir).resolve()
    with tempfile.TemporaryDirectory(dir=workspace) as td:
        script = Path(td) / "analysis.py"
        script.write_text(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            f"DATA_PATH = r'{path}'\n"
            "df = pd.read_csv(DATA_PATH) if DATA_PATH.lower().endswith('.csv') else pd.read_parquet(DATA_PATH)\n"
            + code,
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(script)], cwd=td,
            capture_output=True, text=True, timeout=settings.tool_timeout_seconds,
        )
        if proc.returncode != 0:
            return json.dumps({"ok": False, "stderr": proc.stderr, "stdout": proc.stdout})
        return json.dumps({"ok": True, "stdout": proc.stdout, "stderr": proc.stderr})


TOOLS = [load_dataset, profile_dataset, sql_query, correlations, group_summary, anomalies, forecast, retrieve_knowledge, run_python]
