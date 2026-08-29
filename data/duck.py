from pathlib import Path
import duckdb
import pandas as pd
from .loaders import load_table


def _escape_sql_string(s: str) -> str:
    return s.replace("'", "''")


def query_file(path: str, sql: str) -> list[dict]:
    # Expose a table called data. The SQL is executed in an isolated DuckDB connection.
    suffix = Path(path).suffix.lower()
    con = duckdb.connect(database=":memory:")
    try:
        if suffix == ".csv":
            source = f"read_csv_auto('{_escape_sql_string(path)}')"
        elif suffix == ".parquet":
            source = f"read_parquet('{_escape_sql_string(path)}')"
        elif suffix in {".xlsx", ".xls"}:
            df = load_table(path)
            con.register("data", df)
            return con.execute(sql).df().to_dict(orient="records")
        else:
            raise ValueError("Unsupported file type")
        con.execute(f"CREATE VIEW data AS SELECT * FROM {source}")
        return con.execute(sql).df().to_dict(orient="records")
    finally:
        con.close()
