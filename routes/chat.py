import loguru
from typing import Union, List
from fastapi import APIRouter, HTTPException, Depends

# from llama_index.core.llms import ChatMessage
# from llama_index.core import VectorStoreIndex
# from llama_index.vector_stores.supabase import SupabaseVectorStore
from config import Config, get_config
from utils.message_schema import  Message

router = APIRouter()

@router.post("/chat/{collection_name}", tags=["Chat"])
async def process_chat(
    collection_name: str,
    request: list[Message],
    config: Config = Depends(get_config),
):
    """POST Endpoint to process chat


    Arguments:
        request [Message] -- [message or list of messages to process]

    Raises:
        HTTPException: [handles http exceptions]

    Returns:
        [ChatMessage] -- [Response from llm model]
    """

    try:
        messages = []
        for message in request:
            messages.append({"role": message.role, "content": message.content})

        response = config.llm.invoke(messages)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e