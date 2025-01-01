import requests

def chat_with_collection(message, history, collection_name):
    """
    Fonction adaptée pour gr.ChatInterface qui maintient l'appel à FastAPI.
    Args:
        message: Le message actuel de l'utilisateur
        history: L'historique des messages [(user_message, bot_message), ...]
        collection_name: Nom de la collection à utiliser
    """
    url = f"http://localhost:8000/chat/{collection_name}"
    try:
        response = requests.post(url, json=message)
        if response.status_code == 200:
            return response.text
        else:
            return f"Erreur : {response.json()}"
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"
