from apscheduler.schedulers.background import BackgroundScheduler
from app.whatsapp_handler import send_whatsapp_message

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_followup(task):
    if "assignee" in task:
        scheduler.add_job(
            lambda: send_whatsapp_message(task["assignee"], f"Reminder for task: {task['task_id']}"),
            trigger="interval",
            hours=48
        )
