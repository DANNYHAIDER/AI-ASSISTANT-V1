import openai
from app.basecamp_handler import create_task
from app.sap_handler import maybe_create_po
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def handle_incoming_email(data):
    content = data["body"]
    prompt = f"Extract task from this email: {content}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        task_info = response["choices"][0]["message"]["content"]
    except Exception as e:
        task_info = "Error parsing task"
    task = create_task(task_info)
    maybe_create_po(task_info)
    return task
