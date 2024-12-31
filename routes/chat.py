import loguru
from typing import Union, List
from fastapi import APIRouter, HTTPException, Depends
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains import ConversationalRetrievalChain
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
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=OllamaEmbeddings(model=config.APP_MODEL),
            persist_directory=config.DB_NAME
        )
        # retriever = vector_store.as_retriever(
        #     search_type="mmr",
        #     search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
        # )
        retriever = vector_store.as_retriever()
        conversation_chain = ConversationalRetrievalChain.from_llm(llm=config.llm, retriever=retriever, memory=memory)
        query = ""

        messages = []
        for message in request:
            query = message.content
            # messages.append({"role": message.role, "content": message.content})
        response = conversation_chain.invoke({"question":query})

        return response["answer"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") from e