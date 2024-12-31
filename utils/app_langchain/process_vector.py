__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

async def process_vector(data, collection_name):
        embeddings = OllamaEmbeddings(model=os.getenv("APP_MODEL"))
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(data)
        vectorstore = Chroma.from_documents(collection_name=collection_name, documents=chunks, embedding=embeddings, persist_directory=os.getenv("DB_NAME"))
        return vectorstore
