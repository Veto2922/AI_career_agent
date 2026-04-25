from langchain.messages import ToolMessage
from src.graph_block.tools.career_tools import tools_by_name
from loguru import logger

def generator_tool_node(state):
    """
    Executes the tool calls requested by the LLM.
    """
    try:
        logger.info("Starting generator_tool_node")
        result = []
        # Accessing messages using dot notation as state is a GraphState Pydantic model
        messages = getattr(state, "messages", [])
        if not messages:
            logger.warning("No messages found in state.")
            return {"messages": []}
            
        last_message = messages[-1]
        
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            logger.warning("No tool calls found in the last message.")
            return {"messages": []}

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            logger.info(f"Invoking tool: {tool_name}")
            tool = tools_by_name[tool_name]
            observation = tool.invoke(tool_call["args"])
            result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
            
        return {"messages": result}
    except Exception as e:
        logger.error(f"Error in generator_tool_node: {e}")
        return {"messages": []}
