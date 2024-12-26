from fastapi import APIRouter, HTTPException, Depends

from llama_index.core.llms import ChatMessage
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.supabase import SupabaseVectorStore

import json

from config import Config, get_config

router = APIRouter()


SYSTEM_PROMPT = """
**System Prompt:**

`Fill in the gaps: Add conversation context to last user's message`

**Inputs:**

1. `messages`: A list of conversation messages, containing both user and assistant messages.
2. `last_message`: The most recent user's message in the conversation.

**Requested Output:**

1. A modified version of the last user's message that incorporates the conversation context.
2. Do not explain the modifications or provide additional information.
3. Return a single string.

**Task:**

**Analyze Conversation Context**:

1. Identify key terms, entities, and concepts mentioned in the conversation messages.
3. Extract relevant context, such as specific dates, numbers, or technical terms.

**Merge Extracted Information**:

1. Combine the relevant information into last message.
2. Do not answer the user's message directly or introduce new information.

**Refine the Message**:

1. Make the message more coherent and clear.

**Example Input:**

```
messages=[
    {
        "role": "system",
        "content": "you are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Explain the importance of fast language models"
    },
    {
        "role": "assistant",
        "content": "Fast language models are important because they allow for quicker training and deployment of models."
    },
    {
        "role": "user",
        "content": "Can you provide more details?"
    }
]

last_message={
    "role": "user",
    "content": "Can you provide more details?"
}
```

**Example Output:**

"Can you provide more details on the importance of fast language models, as it allows for quicker training and deployment of models?"
"""


async def complete_last_message(request: list[ChatMessage], config: Config = Depends(get_config)):
    """
    POST Endpoint generate a question from a conversation

    Arguments:
        request [list[ChatMessage]] -- [message or list of messages to process]

    Raises:
        HTTPException: [handles http exceptions]

    Returns:
        [str] -- [Response from llm model]
    """

    messages = [
        ChatMessage(
            role="system", content=SYSTEM_PROMPT
        )
    ]

    conversation = []
    for message in request:
        conversation.append({"role": message.role.value, "content": message.content})

    query = f"{json.dumps(conversation)}\nlast_message={conversation[-1]['content']}"
    messages.append(ChatMessage(role="user", content=query))
    
    try:
        response = config.llm.chat(messages)
        return response.message

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e


@router.post("/chat/{collection_name}", tags=["Chat"])
async def process_contextual_chat(
    request: list[ChatMessage],
    collection_name: str,
    config: Config = Depends(get_config),
):
    """
    Endpoint to process chat with a collection context

    Arguments:
        request [ChatMessage] -- [message or list of messages to process]
        collection_name [str] -- [Collection name in Supabase for the vector store]

    Raises:
        HTTPException: [handles HTTP exceptions]

    Returns:
        [str] -- [Response from the LLM]
    """

    try:
        message = await complete_last_message(request, config)

        config.supabase.schema("vecs").table(collection_name).select("*").limit(
            1
        ).execute()
        vector_store = SupabaseVectorStore(
            postgres_connection_string=config.SUPABASE_PG_CONNECTION_STRING,
            collection_name=collection_name,
        )

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        query_engine = index.as_query_engine(llm=config.llm)
        response = query_engine.query(message.content)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e
