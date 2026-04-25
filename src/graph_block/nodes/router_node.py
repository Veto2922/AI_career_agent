from langchain.messages import AIMessage, HumanMessage, SystemMessage
from src.graph_block.schemas.graph_state import GraphState
from src.graph_block.prompts.router_prompt import Router_SYSTEM_PROMPT
from src.Services.llm_services.llm_factory import LLMFactory
from src.graph_block.schemas.route_node_schema import RouteNodeSchema
from loguru import logger

route_node_llm = LLMFactory.create("groq")
route_node_llm = route_node_llm.with_structured_output(RouteNodeSchema)


def router_node(state: GraphState):
    """
    Decides if the query needs retrieval or can be answered directly.
    """
    try:
        logger.info("Starting router_node")
        docs_titles_names = [doc["name"] for doc in state.docs_titles]
        user_query = HumanMessage(content=state.user_query)

        response = route_node_llm.invoke(
            [
                SystemMessage(
                    content=Router_SYSTEM_PROMPT.format(
                        docs_titles_names=docs_titles_names
                    )
                ),
                user_query,
            ]
        )

        json_res = response.model_dump()
        logger.info(f"Router output: {json_res}")

        return {"router_outputs": json_res}
    except Exception as e:
        logger.error(f"Error in router_node: {e}")
        # Default fallback: skip retrieval if something goes wrong
        return {"router_outputs": {"need_retrieval": False}}
