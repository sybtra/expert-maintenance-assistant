from fastapi import APIRouter, HTTPException, File, UploadFile, Body, Depends
from typing import List
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore

from config import Config, get_config

router = APIRouter()


@router.post("/ingest/{collection_name}", tags=["Documents"])
async def process_ingest(
    collection_name: str,
    uid: str = Body(...),
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

    try:
        documents = []
        for file in files:
            content = file.file.read()
            documents.append(
                Document(text=content, metadata={"filename": file.filename, "uid": uid})
            )

        if len(documents) == 0:
            raise HTTPException(status_code=400, detail=f"No files found")
        vector_store = SupabaseVectorStore(
            postgres_connection_string=(config.SUPABASE_PG_CONNECTION_STRING),
            # name of the collection in the database, as a table with a vector schema
            collection_name=collection_name,
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_documents(documents, storage_context=storage_context)

        return {
            "message": f"User {uid} successfully ingested {len(files)} files into collection {collection_name}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
