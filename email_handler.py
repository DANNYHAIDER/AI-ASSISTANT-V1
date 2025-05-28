import os
import requests
import base64
import openai
from urllib.parse import urlencode
from app.followup_scheduler import schedule_followup
from app.basecamp_handler import assign_task_to_basecamp
from app.sap_handler import assign_task_to_sap

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_REDIRECT_URI = os.getenv("GMAIL_REDIRECT_URI")
GMAIL_SCOPE = "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send"

GMAIL_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GMAIL_TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API_URL = "https://gmail.googleapis.com/gmail/v1"

openai.api_key = os.getenv("OPENAI_API_KEY")

gmail_token = None

def start_gmail_oauth_flow():
    params = urlencode({
        "client_id": GMAIL_CLIENT_ID,
        "redirect_uri": GMAIL_REDIRECT_URI,
        "response_type": "code",
        "scope": GMAIL_SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    })
    return {"auth_url": f"{GMAIL_AUTH_URL}?{params}"}

def handle_gmail_oauth_callback(code):
    global gmail_token
    response = requests.post(GMAIL_TOKEN_URL, data={
        "code": code,
        "client_id": GMAIL_CLIENT_ID,
        "client_secret": GMAIL_CLIENT_SECRET,
        "redirect_uri": GMAIL_REDIRECT_URI,
        "grant_type": "authorization_code"
    })
    gmail_token = response.json().get("access_token")
    return {"access_token": gmail_token}

def read_recent_emails():
    headers = {"Authorization": f"Bearer {gmail_token}"}
    messages_resp = requests.get(f"{GMAIL_API_URL}/users/me/messages", headers=headers)
    message_ids = [m['id'] for m in messages_resp.json().get("messages", [])[:5]]
    emails = []
    for mid in message_ids:
        detail_resp = requests.get(f"{GMAIL_API_URL}/users/me/messages/{mid}?format=full", headers=headers)
        payload = detail_resp.json()
        snippet = payload.get("snippet", "")
        email_data = {
            "id": mid,
            "snippet": snippet,
            "payload": payload
        }
        emails.append(email_data)
    return {"emails": emails}

def send_gmail_reply(to, subject, body):
    headers = {"Authorization": f"Bearer {gmail_token}", "Content-Type": "application/json"}
    message = f"From: me\nTo: {to}\nSubject: {subject}\n\n{body}"
    message_bytes = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")
    payload = {"raw": message_bytes}
    response = requests.post(f"{GMAIL_API_URL}/users/me/messages/send", headers=headers, json=payload)
    return response.json()

def process_and_assign_gmail_tasks():
    headers = {"Authorization": f"Bearer {gmail_token}"}
    messages_resp = requests.get(f"{GMAIL_API_URL}/users/me/messages", headers=headers)
    message_ids = [m['id'] for m in messages_resp.json().get("messages", [])[:5]]
    auto_replies = []
    for mid in message_ids:
        detail_resp = requests.get(f"{GMAIL_API_URL}/users/me/messages/{mid}?format=full", headers=headers)
        payload = detail_resp.json()
        snippet = payload.get("snippet", "")
        prompt = f"Extract a task and write a professional reply to this email:\n\n{snippet}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts tasks and writes email replies."},
                {"role": "user", "content": prompt}
            ]
        )
        reply_text = response.choices[0].message.content
        auto_replies.append({"email_id": mid, "reply": reply_text})

        # Assign to Basecamp and SAP
        task_summary = reply_text.split("\n")[0]
        assign_task_to_basecamp(task_summary)
        assign_task_to_sap(task_summary)

        # Schedule follow-up
        schedule_followup({"email_id": mid, "task": task_summary})

        # Optionally send reply
        # send_gmail_reply(parsed_recipient, "Re: Your Task", reply_text)

    return {"auto_replies": auto_replies}


