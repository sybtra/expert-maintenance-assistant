from fastapi import APIRouter, HTTPException, Depends

from config import Config, get_config

from supabase import Client

router = APIRouter()


def does_collection_exists(collection_name: str, supabase: Client):
    return (
        supabase.schema("vecs").table(collection_name).select("*").execute().data
        != []
    )


@router.delete("/collections/{collection_name}/documents/{document_id}", tags=["Documents"])
async def delete_document(
    collection_name: str,
    document_id: str,
    config: Config = Depends(get_config),
):
    """
    DELETE Endpoint to remove a document from a collection

    Arguments:
        collection_name [str] -- [name of the collection containing the document]
        document_id [str] -- [unique identifier of the document to be deleted]

    Raises:
        HTTPException: [handles http exceptions]
    Returns:
        [dict] -- [message indicating successful deletion]
    """

    if not does_collection_exists(collection_name, config.supabase):
        raise HTTPException(
            status_code=404, detail=f"Collection {collection_name} does not exist"
        )

    config.supabase.schema("vecs").table(collection_name).delete().eq(
        "metadata->>doc_id", document_id
    ).execute()

    if not does_collection_exists(collection_name, config.supabase):
        config.supabase.schema("vecs").rpc(
            "drop_table_if_exists", {"table_name": collection_name}
        ).execute()

    return {
        "message": f"Document {document_id} deleted successfully from collection {collection_name}"
    }
