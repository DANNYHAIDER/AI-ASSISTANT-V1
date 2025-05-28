from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.email_handler import check_task_status

scheduler = BackgroundScheduler()
scheduler.start()

def followup_task(task):
    status = check_task_status(task)
    if status != 'completed':
        # Logic to send follow-up email or notification
        print(f"Following up on task: {task}")

def schedule_followup(task, delay_hours=24):
    run_time = datetime.now() + timedelta(hours=delay_hours)
    scheduler.add_job(followup_task, 'date', run_date=run_time, args=[task])
    print(f"Scheduled follow-up for task: {task} at {run_time}")
