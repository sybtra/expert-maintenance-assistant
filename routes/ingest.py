from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List


from utils.app_langchain.data_parser import parse_data
from utils.app_langchain.process_vector import process_vector
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os
router = APIRouter()


@router.post("/ingest/{collection_name}", tags=["Documents"])
async def process_ingest(
    collection_name: str,
    files: List[UploadFile] = File(...),
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

    try:
        embeddings = OllamaEmbeddings(model=os.getenv("APP_MODEL"))

        if os.path.exists(os.getenv("DB_NAME")):
            Chroma(persist_directory=os.getenv("DB_NAME"), embedding_function=embeddings, collection_name=collection_name).delete_collection()

        for file in files:
            parsed_data = await parse_data(file)
            await process_vector(parsed_data, collection_name=collection_name)

        return {"Message": f"Collection {collection_name} successfully created for {len(files)} files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
