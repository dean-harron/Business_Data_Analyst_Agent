from pathlib import Path
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from config import settings
from agent.orchestrator import run_full_analysis

app=FastAPI(title="Faux Data Analyst Agent", version="0.1.0")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/analyze")
async def analyze(file: UploadFile=File(...), question: str=Form(...)):
    suffix=Path(file.filename or "data.csv").suffix.lower()
    if suffix not in {".csv", ".xlsx", ".xls", ".parquet"}:
        raise HTTPException(400, "Only CSV, Excel and Parquet are supported")
    dest=Path(settings.workspace_dir) / f"{uuid.uuid4().hex}{suffix}"
    dest.write_bytes(await file.read())
    try:
        result=run_full_analysis(question, str(dest))
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc
    return {"report_path": result["report_path"], "report": result["report"]}

@app.get("/report")
def report():
    path=Path(settings.output_dir)/"analysis_report.pdf"
    if not path.exists():
        raise HTTPException(404,"No report yet")
    return FileResponse(path, media_type="application/pdf", filename=path.name)
