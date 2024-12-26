from fastapi import APIRouter, Depends, HTTPException

from config import Config, get_config

router = APIRouter()

@router.delete("/collections/{collection_name}", tags=["Documents"])
async def delete_collection(collection_name: str, config: Config = Depends(get_config)):
    """
    DELETE Endpoint to remove a collection

    Arguments:
        collection_name [str] -- [name of the collection to be deleted]

    Raises:
        HTTPException: [handles http exceptions]
    Returns:
        [dict] -- [message indicating successful deletion]
    """

    config.supabase.schema("vecs").rpc("drop_table_if_exists", {"table_name": collection_name}).execute()

    return {"message": f"Collection {collection_name} deleted successfully"}
