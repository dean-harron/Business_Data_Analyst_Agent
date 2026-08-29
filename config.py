from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_provider: str = "openrouter"
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-5.2"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_http_referer: str = "http://localhost:8000"
    openrouter_app_title: str = "Faux Data Analyst Agent"
    hf_token: str | None = None
    hf_model: str = "meta-llama/Llama-3.1-8B-Instruct"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_dir: str = "./workspace/chroma"
    rag_collection: str = "analyst_knowledge"
    workspace_dir: str = "./workspace"
    output_dir: str = "./outputs"
    max_agent_steps: int = 30
    tool_timeout_seconds: int = 120
    youtube_api_key: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    email_from: str | None = None
    smtp_use_tls: bool = True
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    whatsapp_from: str | None = None
    whatsapp_to: str | None = None
    whatsapp_public_media_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
Path(settings.workspace_dir).mkdir(parents=True, exist_ok=True)
Path(settings.output_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
