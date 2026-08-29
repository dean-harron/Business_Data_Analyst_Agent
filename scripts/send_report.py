import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from notifications.emailer import send_email
from notifications.telegram import send_telegram_document
from notifications.whatsapp import send_whatsapp_report
from config import settings

parser=argparse.ArgumentParser()
parser.add_argument("--pdf", required=True)
parser.add_argument("--email")
parser.add_argument("--telegram-chat-id")
parser.add_argument("--whatsapp", action="store_true")
args=parser.parse_args()

if args.email:
    send_email(args.email, "Faux Data Analyst Report", "Please find the attached analysis report.", args.pdf)
    print("Email sent")
if args.telegram_chat_id:
    send_telegram_document(args.telegram_chat_id, args.pdf, "Faux Data Analyst report")
    print("Telegram sent")
if args.whatsapp:
    msg=send_whatsapp_report("Your analysis report is ready.", settings.whatsapp_public_media_url)
    print("WhatsApp sent", msg.sid)
