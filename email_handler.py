from app.ai_engine import extract_tasks_from_text
from app.basecamp_handler import assign_task_to_basecamp

def handle_incoming_email(data):
    email_body = data.get('body', '')
    tasks = extract_tasks_from_text(email_body)
    assigned_results = []
    for task in tasks:
        result = assign_task_to_basecamp(task)
        assigned_results.append(result)
    return assigned_results




