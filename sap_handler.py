import requests
from app.config import SAP_API_KEY

def maybe_create_po(task_info):
    if "purchase" in task_info.lower():
        # Simplified SAP PO creation logic - add authentication and error handling
        response = requests.post("https://sap-service-layer.com/PO", json={"task": task_info})
        return response.json()
    return None
