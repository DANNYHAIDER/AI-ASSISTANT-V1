import os
import requests

SAP_API_BASE_URL = os.getenv("SAP_API_BASE_URL")
SAP_API_KEY = os.getenv("SAP_API_KEY")

def create_purchase_order(data):
    url = f"{SAP_API_BASE_URL}/purchase_orders"
    headers = {
        "Authorization": f"Bearer {SAP_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        return {"status": "purchase_order_created", "order_id": response.json().get("id")}
    else:
        return {"error": response.text}

