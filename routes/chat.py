from fastapi import APIRouter, HTTPException, Depends

from llama_index.core.llms import ChatMessage
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore

from config import Config, get_config

router = APIRouter()


@router.post("/chat", tags=["Chat"])
async def process_chat(
    request: list[ChatMessage],
    config: Config = Depends(get_config),
):
    """POST Endpoint to process chat


    Arguments:
        request [ChatMessage] -- [message or list of messages to process]

    Raises:
        HTTPException: [handles http exceptions]

    Returns:
        [ChatMessage] -- [Response from llm model]
    """

    try:
        messages = [ChatMessage(role=msg.role, content=msg.content) for msg in request]
        response = config.llm.chat(messages)
        response_dict = response.message.dict()
        del response_dict["additional_kwargs"]
        return response_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e