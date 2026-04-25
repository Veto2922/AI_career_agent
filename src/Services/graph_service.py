from src.graph_block.graph import compile_graph
from src.Services.retrieval_service import get_tree_retrieval
from loguru import logger

_graph_instance = None

def get_compiled_graph():
    global _graph_instance
    if _graph_instance is None:
        try:
            logger.info("Compiling LangGraph...")
            tree_retrieval = get_tree_retrieval()
            _graph_instance = compile_graph(tree_retrieval)
            logger.info("LangGraph compiled and ready.")
        except Exception as e:
            logger.error(f"Failed to compile LangGraph: {e}")
            raise e
    return _graph_instance
