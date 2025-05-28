from fastapi import FastAPI
from app.email_handler import handle_incoming_email
from app.followup_scheduler import schedule_followup

app = FastAPI()

@app.post("/email")
def receive_email(data: dict):
    task = handle_incoming_email(data)
    schedule_followup(task)
    return {"status": "task_created", "task": task}
