import requests
from app.config import TWILIO_API_KEY

WHATSAPP_API_URL = "https://api.twilio.com/..."

def send_whatsapp_message(to, message):
    payload = {
        "to": to,
        "body": message
    }
    headers = {"Authorization": f"Bearer {TWILIO_API_KEY}"}
    requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
