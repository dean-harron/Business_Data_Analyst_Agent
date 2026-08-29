from twilio.rest import Client
from config import settings

def send_whatsapp_report(body: str, media_url: str | None = None):
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        raise RuntimeError("Twilio credentials are missing")
    if not settings.whatsapp_from or not settings.whatsapp_to:
        raise RuntimeError("WhatsApp from/to are missing")
    client=Client(settings.twilio_account_sid, settings.twilio_auth_token)
    kwargs={"from_":settings.whatsapp_from,"to":settings.whatsapp_to,"body":body}
    if media_url:
        kwargs["media_url"]=[media_url]
    return client.messages.create(**kwargs)
