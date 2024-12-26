from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from routes import ingest, delete_collection, delete_document, chat, chat_collection
import gradio as gr
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
app.include_router(delete_document.router)
app.include_router(delete_collection.router)

app.include_router(chat.router)
app.include_router(chat_collection.router)
