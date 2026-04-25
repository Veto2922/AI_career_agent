import os
from dotenv import load_dotenv
from pageindex import PageIndexClient
from src.retrieval_block.tree_retrieval import TreeRetrieval
from loguru import logger

_tree_retrieval_instance = None

def get_tree_retrieval() -> TreeRetrieval:
    global _tree_retrieval_instance
    if _tree_retrieval_instance is None:
        load_dotenv()
        api_key = os.getenv("Page_index_api")
        if not api_key:
            logger.error("PageIndex API key is missing in environment variables.")
            raise ValueError("PageIndex API key is missing.")
        
        logger.info("Initializing PageIndexClient and TreeRetrieval service...")
        pi_client = PageIndexClient(api_key=api_key)
        _tree_retrieval_instance = TreeRetrieval(pi_client)
        logger.info("TreeRetrieval service initialized successfully.")
        
    return _tree_retrieval_instance
