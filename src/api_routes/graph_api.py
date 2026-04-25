from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from src.api_routes.apis_schemas.graph_schemas import (
    UserMessage,
    ChatResponse,
)
from src.Services.graph_service import get_compiled_graph
from src.Services.retrieval_service import get_tree_retrieval
from loguru import logger
import uuid

router = APIRouter(prefix="/graph", tags=["Graph Agent"])

retrieval_service = get_tree_retrieval()
agent = get_compiled_graph()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(message: UserMessage):
    """
    Send a message to the LangGraph agent and get a response.
    """
    thread_id = message.thread_id or str(uuid.uuid4())
    logger.info(f"Received message for thread {thread_id}: {message.content[:50]}...")

    try:
        # Get document titles as required by the graph state
        docs_titles = retrieval_service.get_docs_titles()

        # Initial state - Include user_query and docs_titles as expected by the graph nodes
        inputs = {
            "messages": [HumanMessage(content=message.content)],
            "user_query": message.content,
            "docs_titles": docs_titles,
        }
        config = {"configurable": {"thread_id": thread_id}}

        # Invoke agent
        result = await agent.ainvoke(inputs, config=config)

        # Extract last message or relevant output
        # Based on GraphState, the messages list will contain the conversation
        last_message = result["messages"][-1]

        response_content = ""
        if hasattr(last_message, "content"):
            content = last_message.content
            if isinstance(content, str):
                response_content = content
            elif isinstance(content, list):
                # Extract text from list of blocks (e.g., from multimodal inputs/outputs)
                texts = []
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        texts.append(block["text"])
                    elif isinstance(block, str):
                        texts.append(block)
                response_content = " ".join(texts) if texts else str(content)
            else:
                response_content = str(content)
        else:
            response_content = str(last_message)

        return {
            "thread_id": thread_id,
            "response": response_content,
            "full_state": {
                k: v for k, v in result.items() if k != "messages"
            },  # Return other state bits but exclude bulky messages
        }
        logger.info(f"Response for thread {thread_id}: {response_content}")
    except Exception as e:
        logger.error(f"Error in chat with agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
