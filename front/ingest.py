import requests

def ingest_documents(collection_name, files):
    url = f"http://localhost:8000/ingest/{collection_name}"
    
    try:
        # On n'a pas besoin de manipuler les fichiers, on les envoie directement
        files_data = [
            ('files', file)
            for file in files
        ]
        
        response = requests.post(url, files=files_data)
        
        if response.status_code == 200:
            return f"Ingestion réussie : {response.json()['Message']}"
        else:
            return f"Erreur : {response.json()}"
            
    except Exception as e:
        return f"Erreur lors de l'envoi : {str(e)}"