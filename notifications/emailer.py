from email.message import EmailMessage
from pathlib import Path
import smtplib
from config import settings

def send_email(to: str, subject: str, body: str, attachment: str | None = None):
    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password or not settings.email_from:
        raise RuntimeError("SMTP settings are incomplete")
    msg=EmailMessage()
    msg["From"]=settings.email_from
    msg["To"]=to
    msg["Subject"]=subject
    msg.set_content(body)
    if attachment:
        p=Path(attachment)
        msg.add_attachment(p.read_bytes(), maintype="application", subtype="pdf", filename=p.name)
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_use_tls:
            server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg)
