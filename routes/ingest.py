from fastapi import APIRouter, HTTPException, File, UploadFile, Body, Depends
from typing import List
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore
from langchain_ollama import OllamaEmbeddings

from config import Config, get_config
import os
from utils.DocumentExtractor import  DocumentExtractor
from utils.app_langchain.data_parser import parse_data
from utils.app_langchain.process_vector import process_vector
from langchain_chroma import Chroma

router = APIRouter()


@router.post("/ingest", tags=["Documents"])
async def process_ingest(
    # collection_name: str,
    # uid: str = Body(...),
    files: List[UploadFile] = File(...),
    config: Config = Depends(get_config),
):
    """
    POST Endpoint to ingest multiple files

    Arguments:
        collection_name [str] -- [name of the collection in the database]
        uid [str] -- [unique identifier for the ingestion (query parameter)]
        files [UploadFile] -- [list of files to ingest]

    Raises:
        HTTPException: [handles http exceptions]
    Returns:
        [dict] -- [message]
    """
    extractor = DocumentExtractor()

    try:
        embeddings = OllamaEmbeddings(model=get_config().APP_MODEL)

        if os.path.exists(config.DB_NAME):
            Chroma(persist_directory=config.DB_NAME, embedding_function=embeddings).delete_collection()
        content = await extractor.extract_content(files)
        parsed_data = parse_data(content)
        vectorstore = await process_vector(parsed_data)

        return {"content": vectorstore._collection_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
