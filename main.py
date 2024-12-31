from fastapi import FastAPI
from routes import ingest, chat
import dotenv
dotenv.load_dotenv()

app = FastAPI()

tags_metadata = [
    {
        "name": "Documents",
        "description": "Collections & Documents API",
    },
    {
        "name": "Chat",
        "description": "Chat API",
    },
]

app.openapi_tags = tags_metadata

app.include_router(ingest.router)
# app.include_router(delete_document.router)
# app.include_router(delete_collection.router)

app.include_router(chat.router)
# app.include_router(chat_collection.router)
