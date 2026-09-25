# Data Analyst Agent

A local-first professional business data-analysis agent built with Python, LangChain/LangGraph, PyTorch, RAG, DuckDB, MCP, OpenRouter or Hugging Face, ReportLab, and optional notification channels.

## Core capabilities

- Analyze CSV, Excel, Parquet, and SQLite-compatible business data.
- Use DuckDB for analytical SQL.
- Profile data and compute descriptive statistics.
- Detect anomalies with a PyTorch autoencoder.
- Build charts with Matplotlib and Seaborn.
- Retrieve metric definitions and domain guidance using local RAG/Chroma.
- Query public YouTube channel and video data using the YouTube Data API.
- Produce a professional PDF report.
- Send reports by email or Telegram locally; use WhatsApp via Twilio when a public media URL is available.
- Expose selected analysis operations through MCP.
- Run through a CLI and FastAPI service.

## Quick start

### 1. Create the environment

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure secrets

Copy `.env.example` to `.env` and fill in at least:

- `LLM_PROVIDER`
- `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`, or the equivalent Hugging Face settings

### 3. Build the knowledge base

```bash
python scripts/index_knowledge.py
```

### 4. Run a local analysis

On macOS/Linux:

```bash
python scripts/run_analysis.py \\
  --data data/sample_business.csv \\
  --question "Analyze revenue, profit, margins and customer segments. Identify the biggest changes and recommend three actions."
```

Windows PowerShell users can put the arguments on one line:

```powershell
python scripts/run_analysis.py --data data/sample_business.csv --question "Analyze revenue, profit, margins and customer segments. Identify the biggest changes and recommend three actions."
```

### 5. Start the API

```bash
uvicorn app:app --reload --port 8000
```

Then visit <http://127.0.0.1:8000/docs>.

### 6. Start the MCP server (optional)

```bash
python mcp/server.py
```

See the project documentation for instructions on connecting the server through LangChain MCP adapters.

## Business-intelligence reporting behavior

The MVP includes a deterministic business-analysis layer in `agent/business_analysis.py`.

It calculates recognized business metrics directly from the loaded dataset and supplies evidence to report generation. This prevents the report from becoming a discussion of JSON or schema compliance when a dataset and business question are available. The LLM may improve the narrative wording, but the deterministic business evidence remains the fallback source of truth.

## Important note

This is an experimental prototype of the data analyst agent and should not be treated as a final product. Some parts of the codebase may need correction, and additional features may be required before it is production-ready.

## License

MIT License. Copyright © 2026 Dean Harron.
