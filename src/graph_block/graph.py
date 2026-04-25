import os
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from loguru import logger

from src.graph_block.schemas.graph_state import GraphState
from src.graph_block.nodes.router_node import router_node
from src.graph_block.nodes.docs_titles_node import Docs_titles_node
from src.graph_block.nodes.docs_toc_node import create_docs_toc_node
from src.graph_block.nodes.generator_node import create_generator_node
from src.graph_block.nodes.tools_node import generator_tool_node

def should_continue(state: GraphState) -> Literal["generator_tool_node", "__end__"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call."""
    try:
        messages = state.messages
        if not messages:
            return END
            
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            logger.info("Tool calls detected, moving to tool node.")
            return "generator_tool_node"

        logger.info("No tool calls, ending workflow.")
        return END
    except Exception as e:
        logger.error(f"Error in should_continue edge: {e}")
        return END

def need_retrieve(state: GraphState) -> Literal["Docs_titles_node", "generator_node"]:
    """Decides based on router output whether to retrieve documents or go straight to generation."""
    try:
        if state.router_outputs.get('need_retrieval'):
            logger.info("Retrieval needed.")
            return "Docs_titles_node"
        
        logger.info("Direct generation.")
        return "generator_node"
    except Exception as e:
        logger.error(f"Error in need_retrieve edge: {e}")
        return "generator_node"

def compile_graph(tree_retrieval):
    """
    Builds and compiles the LangGraph agent.
    """
    try:
        logger.info("Compiling the LangGraph agent.")
        
        # Initialize nodes with tree_retrieval service
        Docs_toc_node = create_docs_toc_node(tree_retrieval)
        generator_node = create_generator_node(tree_retrieval)

        # Build workflow
        workflow = StateGraph(GraphState)

        # Add nodes
        workflow.add_node("router_node", router_node)
        workflow.add_node("Docs_titles_node", Docs_titles_node)
        workflow.add_node("Docs_toc_node", Docs_toc_node)
        workflow.add_node("generator_node", generator_node)
        workflow.add_node("generator_tool_node", generator_tool_node)

        # Add edges
        workflow.add_edge(START, "router_node")

        workflow.add_conditional_edges(
            "router_node",
            need_retrieve,
            {"Docs_titles_node": "Docs_titles_node", "generator_node": "generator_node"}
        )
        
        workflow.add_edge("Docs_titles_node", "Docs_toc_node")
        workflow.add_edge("Docs_toc_node", "generator_node")

        workflow.add_conditional_edges(
            "generator_node",
            should_continue,
            {"generator_tool_node": "generator_tool_node", "__end__": END}
        )

        workflow.add_edge("generator_tool_node", "generator_node")

        # Compile
        checkpointer = InMemorySaver()
        agent = workflow.compile(checkpointer=checkpointer)
        
        logger.info("Graph compiled successfully.")
        return agent
    except Exception as e:
        logger.error(f"Failed to compile graph: {e}")
        raise
