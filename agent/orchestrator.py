from pathlib import Path
import json
from agent.agent import run_agent
from agent.report_writer import write_report
from agent.tools import set_current_data
from data.loaders import load_table
from data.profile import profile_dataframe
from reporting.charts import build_core_charts
from reporting.report import build_pdf_report
from config import settings


def run_full_analysis(question: str, data_path: str) -> dict:
    set_current_data(data_path)
    profile=profile_dataframe(load_table(data_path))
    agent_result=run_agent(question, data_path)
    messages=agent_result.get("messages", [])
    analysis_text="\n".join(str(getattr(m,"content",m)) for m in messages[-8:])
    # Use a fresh local RAG query from the question; the agent may have done this as well.
    evidence_text=""
    report_obj=write_report(analysis_text, evidence_text, profile)
    charts=build_core_charts(load_table(data_path), settings.output_dir)
    report_path=str(Path(settings.output_dir) / "analysis_report.pdf")
    build_pdf_report(report_obj.model_dump(), charts, report_path)
    return {
        "report_path": report_path,
        "profile": profile,
        "analysis": analysis_text,
        "report": report_obj.model_dump(),
    }
