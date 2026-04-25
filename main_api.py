import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from src.api_routes.base_api import router as base_router
from src.api_routes.data_ingestion_api import router as data_ingestion_router
from src.api_routes.retrieval_api import router as retrieval_router

from src.api_routes.graph_api import router as graph_router

# Configuration for Loguru
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)
logger.add("logs/api.log", rotation="10 MB", retention="10 days", level="DEBUG")

app = FastAPI(
    title="AI Career Agent API",
    description="FastAPI for AI Career Agent including Data Ingestion, Retrieval, and LangGraph Agent.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(base_router)
app.include_router(data_ingestion_router)
app.include_router(retrieval_router)
app.include_router(graph_router)


if __name__ == "__main__":
    uvicorn.run("main_api:app", host="127.0.0.1", port=8000, reload=True)
