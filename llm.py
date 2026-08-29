from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
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
            raise RuntimeError("HF_TOKEN is not configured")
        endpoint = HuggingFaceEndpoint(
            repo_id=settings.hf_model,
            huggingfacehub_api_token=settings.hf_token,
            temperature=0.1,
            max_new_tokens=3000,
        )
        return ChatHuggingFace(llm=endpoint)
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
