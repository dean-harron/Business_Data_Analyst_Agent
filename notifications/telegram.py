from pathlib import Path
import requests
from config import settings

def send_telegram_document(chat_id: str, pdf_path: str, caption: str=""):
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")
    url=f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendDocument"
    with Path(pdf_path).open("rb") as f:
        r=requests.post(url, data={"chat_id":chat_id,"caption":caption}, files={"document":(Path(pdf_path).name,f,"application/pdf")}, timeout=60)
    r.raise_for_status()
    return r.json()
