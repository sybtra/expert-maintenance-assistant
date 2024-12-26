from fastapi import Depends
import requests
# from config import Config, get_config

def ingest_documents(collection_name, uid, files):
    url = f"http://localhost:8000/ingest/{collection_name}"
    files_data = [("files", file) for file in files]
    data = {"uid": uid}
    response = requests.post(url, data=data, files=files_data)
    if response.status_code == 200:
        return f"Ingestion réussie : {response.json()['message']}"
    else:
        return f"Erreur : {response.json()}"