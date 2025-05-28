from fastapi import FastAPI, Request
from app.email_handler import handle_incoming_email
from app.followup_scheduler import schedule_followup
from app.basecamp_handler import start_basecamp_oauth_flow, handle_basecamp_oauth_callback
from app.gmail_handler import (
    start_gmail_oauth_flow, handle_gmail_oauth_callback,
    read_recent_emails, send_gmail_reply, process_and_assign_gmail_tasks
)

app = FastAPI()

@app.post("/email")
def receive_email(data: dict):
    task = handle_incoming_email(data)
    schedule_followup(task)
    return {"status": "task_created", "task": task}

@app.get("/basecamp/oauth/start")
def basecamp_oauth_start():
    return start_basecamp_oauth_flow()

@app.get("/basecamp/oauth/callback")
def basecamp_oauth_callback(code: str):
    return handle_basecamp_oauth_callback(code)

@app.get("/gmail/oauth/start")
def gmail_oauth_start():
    return start_gmail_oauth_flow()

@app.get("/gmail/oauth/callback")
def gmail_oauth_callback(code: str):
    return handle_gmail_oauth_callback(code)

@app.get("/gmail/emails")
def gmail_read_emails():
    return read_recent_emails()

@app.post("/gmail/send")
def gmail_send_reply(data: dict):
    return send_gmail_reply(data.get("to"), data.get("subject"), data.get("body"))

@app.get("/gmail/tasks")
def gmail_extract_tasks():
    return process_and_assign_gmail_tasks()


