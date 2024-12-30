from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List

from utils.DocumentExtractor import  DocumentExtractor
from utils.app_langchain.data_parser import parse_data
from utils.app_langchain.process_vector import process_vector

router = APIRouter()


@router.post("/ingest", tags=["Documents"])
async def process_ingest(
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
    extractor = DocumentExtractor()

    try:
        content = await extractor.extract_content(files)
        parsed_data = parse_data(content)
        vectorstore = await process_vector(parsed_data)

        return {"content": vectorstore._collection_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
