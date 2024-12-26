from fastapi import Depends
import requests
# from config import Config, get_config

def chat_with_collection(collection_name, messages):
    url = f"http://localhost:8000/chat/{collection_name}"
    headers = {"Content-Type": "application/json"}
    payload = [{"role": "user", "content": message} for message in messages.split("\n")]
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return response["response"]
    else:
        return f"Erreur : {response.json()}"