import os
import requests
from urllib.parse import urlencode
from app.ai_engine import extract_tasks_from_text

BASECAMP_CLIENT_ID = os.getenv("BASECAMP_CLIENT_ID")
BASECAMP_CLIENT_SECRET = os.getenv("BASECAMP_CLIENT_SECRET")
BASECAMP_REDIRECT_URI = os.getenv("BASECAMP_REDIRECT_URI")

AUTH_URL = "https://launchpad.37signals.com/authorization/new"
TOKEN_URL = "https://launchpad.37signals.com/authorization/token"
API_BASE = "https://3.basecampapi.com"

access_token = None

def start_basecamp_oauth_flow():
    params = {
        "type": "web_server",
        "client_id": BASECAMP_CLIENT_ID,
        "redirect_uri": BASECAMP_REDIRECT_URI,
        "state": "random_state_string",
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return {"auth_url": url}

def handle_basecamp_oauth_callback(code):
    global access_token
    data = {
        "type": "web_server",
        "client_id": BASECAMP_CLIENT_ID,
        "client_secret": BASECAMP_CLIENT_SECRET,
        "redirect_uri": BASECAMP_REDIRECT_URI,
        "code": code
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    return {"status": "authorized"}

def assign_task_to_basecamp(task):
    global access_token
    if not access_token:
        return {"error": "Not authorized"}
    # Replace these with your actual Basecamp project and bucket IDs
    project_id = os.getenv("BASECAMP_PROJECT_ID")
    todo_list_id = os.getenv("BASECAMP_TODO_LIST_ID")
    url = f"{API_BASE}/{project_id}/buckets/{todo_list_id}/todosets.json"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "AI-Assistant-App (youremail@example.com)"
    }
    task_payload = {
        "name": task,
        "description": "Automatically assigned by AI Assistant",
        "due_on": None
    }
    response = requests.post(url, json=task_payload, headers=headers)
    if response.status_code == 201:
        return {"status": "task_assigned", "task": task}
    else:
        return {"error": response.text}

