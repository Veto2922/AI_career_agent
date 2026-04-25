from fastapi import APIRouter, HTTPException
from src.api_routes.apis_schemas.retrieval_schemas import (
    DocIndicesRequest,
    RetrieveRequest,
    TitlesResponse,
    TOCResponse,
    RetrievalContentResponse,
)
from src.Services.retrieval_service import get_tree_retrieval
from loguru import logger

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])


retrieval_service = get_tree_retrieval()


@router.get("/docs-titles", response_model=TitlesResponse)
async def get_docs_titles():
    """
    Get titles of all available documents.
    """
    logger.info("Fetching document titles.")
    try:
        titles = retrieval_service.get_docs_titles()
        return {"titles": titles}
    except Exception as e:
        logger.error(f"Error fetching docs titles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/toc", response_model=TOCResponse)
async def get_toc(request: DocIndicesRequest):
    """
    Get Table of Contents for specific document indices.
    """
    logger.info(f"Fetching TOC for indices: {request.doc_indices}")
    try:
        toc = retrieval_service.get_toc(request.doc_indices)
        return {"toc": toc}
    except Exception as e:
        logger.error(f"Error fetching TOC: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/retrieve", response_model=RetrievalContentResponse)
async def retrieve_content(request: RetrieveRequest):
    """
    Retrieve related content from documents using target IDs.
    """
    logger.info(f"Retrieving content for {len(request.target_docs)} documents.")
    try:
        # Convert Pydantic models to list of dicts as expected by the service
        target_docs_dict = [doc.model_dump() for doc in request.target_docs]
        content = retrieval_service.retrieve(target_docs_dict)
        return {"content": content}
    except Exception as e:
        logger.error(f"Error retrieving content: {e}")
        raise HTTPException(status_code=500, detail=str(e))
