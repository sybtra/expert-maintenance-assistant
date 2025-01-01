from fastapi import Depends
import requests
# from config import Config, get_config

def chat_with_collection(collection_name, query):
    url = f"http://localhost:8000/chat/{collection_name}"
    params = {
        "query": query
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        return f"Erreur : {response.json()}"