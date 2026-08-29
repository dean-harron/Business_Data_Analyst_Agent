from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model=settings.openrouter_model,
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    temperature=0.1,
)


from langchain.tools import tool

@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers exactly"""
    return a + b

#Data Loaders

from pathlib import Path
import pandas as pd

SUPPORTED = {".csv", ".xslx", ".xls", ".parquet"}

def load_table(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if p.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {p.suffix}")
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    if p.suffix.lower() in {".xslx", "xls"}:
        return pd.read_excel(p)
    return pd.read_parquet(p)

# Local RAG (Retrieval Augumented Generation)

from pathlib import Path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from configs import settings

def embeddings():
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)

def get_store():
    return Chroma(
        collection_name=settings.rag_collection,
        embedding_function=embeddings(),
        persist_directory=settings.chroma_dir,
    )

def index_directory(directory: str = "knowledge") -> int:
    paths = sorted(Path(directory).glob("**/.md")) + sorted(Path(directory).glob("**/*.txt"))
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    docs=[]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)
        docs.extend(Document(page_content=c, metadata={"source": str(path)}) for c in chunks)
    if not docs:
        return 0
    store = get_store()
    store.add_documents(docs)
    return len(docs)

def search(query: str, k: int = 5):
    store = get_store()
    return store.similarity_search_with_score(query, k=k)


## Agent tools

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
        raise RuntimeError("No dataset loaded. call load_dataset first.")
    return CURRENT_DATA["path"]

@tool
def load_dataset(path:str) -> dict:
    """Load a CSV, Excel or Parquet file and return basic metadata."""
    df = load_table(path)
    set_current_data(path=)
    return {"path": str(Path(path).resolve()), "rows": len(df), "columns": list(map(str, df.columns))}

@tool
def profile_dataset() -> dict:
    """Profile the current dataset including schema, missingness, duplicates and numeric summaries."""
    return profile_dataframe(load_table(require_data()))

@tool
def sql_query(sql: str) -> list[dict]:
    """Run a read-only analytical SQL query against the current dataset as table `data`."""
    normalized = sql.strip().lower()
    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "copy", "attach", "install", "load"]
    if not normalized.startswith(("select", "with", "describe", "show", "explain")):
        raise ValueError("Only read-only analytical SQL is allowed")
    if any(x in normalized for x in forbidden):
        raise ValueError("Potentially destructive SQL blocked")
    return query_file(require_data(), sql)

@tool
def correlations() -> list[dict]:
    """Compute pairwise correlations for numeric columns in the current dataset."""
    return correlation(load_table(require_data()))
    pass


## LLM Layer

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndPoint, ChatHuggingFace
from config import settings

def get_chat_model():
    provider = settings.llm_provider.lower().strip()
    if provider == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")
        return ChatOpenAI(
            model=settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=0.1,
            max_tokens=3000,
            default_headers={
                "HTTP-Referer": settings.openrouter_http_referer,
                "X-Title": settings.openrouter_app_title,
            },
        )
    
    if provider in {"huggingface", "hf"}:
        if not settings.hf_token:
            raise  RuntimeError("HF_TOKEN is not configured")
        endpoint = HuggingFaceEndPoint(
            repo_id=settings.hf_model,
            huggingfacehub_api_token=settings.hf_token,
            temperature=0.1,
            max_new_tokens=3000,
        )
        return ChatHuggingFace(llm=endpoint)
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")


## Complete Agent

from langchain.agents import create_agent
from config import settings
from ll import get_chat_model
from agent.prompts import SYSTEM_PROMPT
from agent.tools import TOOLS

def build_agent():
    model = get_chat_model()
    return create_agent(model=model, tools=TOOLS, system_prompt=SYSTEM_PROMPT)

def run_agent(question: str, data_path: str):
    agent = build_agent()
    results = agent.invoke({
        "messages": [
            {"role": user, "content": f"Dataset path: {data_path}\nBusiness question: {question}"}
        ]
    })
    return results