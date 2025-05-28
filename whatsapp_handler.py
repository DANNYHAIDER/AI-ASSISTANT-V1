import os
import requests

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

def send_whatsapp_message(to_number, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": to_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(WHATSAPP_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return {"status": "message_sent"}
    else:
        return {"error": response.text}

