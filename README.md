# Faux Data Analyst Agent

A local-first professional data-analysis agent built with Python, LangChain/LangGraph, PyTorch, RAG, DuckDB, MCP, OpenRouter or Hugging Face, ReportLab, and optional notification channels.

## Core capabilities
- Analyze CSV, Excel, Parquet and SQLite-compatible business data.
- Use DuckDB for analytical SQL.
- Profile data and compute descriptive statistics.
- Detect anomalies with a PyTorch autoencoder.
- Build charts with Matplotlib/Seaborn.
- Retrieve metric definitions and domain guidance using local RAG/Chroma.
- Query public YouTube channel/video data using the YouTube Data API.
- Produce a professional PDF report.
- Send reports by email or Telegram locally; WhatsApp via Twilio when a public media URL is available.
- Expose selected analysis operations through MCP.
- Run through a CLI and FastAPI service.

## Quick start

### 1. Create the environment

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure secrets

Copy `.env.example` to `.env` and fill at least:
- `LLM_PROVIDER`
- `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`, or Hugging Face equivalents

### 3. Build the knowledge base

```bash
python scripts/index_knowledge.py
```

### 4. Run a local analysis

```bash
python scripts/run_analysis.py \
  --data data/sample_business.csv \
  --question "Analyze revenue, profit, margins and customer segments. Identify the biggest changes and recommend three actions."
```

Windows PowerShell users can put the arguments on one line.

### 5. Start the API

```bash
uvicorn app:app --reload --port 8000
```

Then visit `http://127.0.0.1:8000/docs`.

### 6. Start the MCP server (optional)

```bash
python mcp/server.py
```

The handbook explains how to connect it through LangChain MCP adapters.
