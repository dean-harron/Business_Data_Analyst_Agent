from pathlib import Path
import json
from mcp.server import MCPServer
from data.loaders import load_table
from data.profile import profile_dataframe
from data.duck import query_file

mcp = MCPServer("faux-data-analyst")

@mcp.tool()
def profile_csv(path: str) -> dict:
    """Profile a tabular dataset for analyst use."""
    return profile_dataframe(load_table(path))

@mcp.tool()
def run_readonly_sql(path: str, sql: str) -> list[dict]:
    """Run a read-only SQL query against a CSV/Parquet file."""
    low=sql.strip().lower()
    if not low.startswith(("select", "with", "describe", "show", "explain")):
        raise ValueError("Read-only SELECT/WITH/DESCRIBE/SHOW/EXPLAIN queries only")
    return query_file(path, sql)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
