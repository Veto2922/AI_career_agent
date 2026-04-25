from langchain.messages import HumanMessage, SystemMessage
from src.graph_block.schemas.graph_state import GraphState
from src.graph_block.prompts.docs_titles_prompt import Docs_titles_SYSTEM_PROMPT
from src.Services.llm_services.llm_factory import LLMFactory
from src.graph_block.schemas.docs_title_node_schema import DocsTitleNodeSchema
from loguru import logger

docs_titles_node_llm = LLMFactory.create("groq")
docs_titles_node_llm = docs_titles_node_llm.with_structured_output(DocsTitleNodeSchema)


def Docs_titles_node(state: GraphState):
    """
    Selects the most relevant documents based on their titles and descriptions.
    """
    try:
        logger.info("Starting Docs_titles_node")
        user_query = HumanMessage(content=state.user_query)

        response = docs_titles_node_llm.invoke(
            [
                SystemMessage(
                    content=Docs_titles_SYSTEM_PROMPT.format(
                        docs_titles=state.docs_titles
                    )
                ),
                user_query,
            ]
        )

        json_res = response.model_dump()
        selected_indexes = json_res.get("selected_indexes", [])
        logger.info(f"Docs Title Node Output: {selected_indexes}")

        return {"selected_docs_indexes": selected_indexes}
    except Exception as e:
        logger.error(f"Error in Docs_titles_node: {e}")
        return {"selected_docs_indexes": []}
