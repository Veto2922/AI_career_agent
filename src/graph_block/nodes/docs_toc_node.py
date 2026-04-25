from langchain.messages import HumanMessage, SystemMessage
from src.graph_block.schemas.graph_state import GraphState
from src.graph_block.prompts.docs_toc_prompt import Docs_toc_SYSTEM_PROMPT
from src.Services.llm_services.llm_factory import LLMFactory
from src.graph_block.schemas.docs_toc_node_schema import DocsTocNodeSchema
from loguru import logger

docs_toc_node_llm = LLMFactory.create("gemini")
docs_toc_node_llm = docs_toc_node_llm.with_structured_output(DocsTocNodeSchema)


def create_docs_toc_node(tree_retrieval):
    def Docs_toc_node(state: GraphState):
        """
        Selects specific sections within the chosen documents.
        """
        try:
            logger.info("Starting Docs_toc_node")
            user_query = HumanMessage(content=state.user_query)

            docs_toc = tree_retrieval.get_toc(state.selected_docs_indexes)

            response = docs_toc_node_llm.invoke(
                [
                    SystemMessage(
                        content=Docs_toc_SYSTEM_PROMPT.format(docs_toc=docs_toc)
                    ),
                    user_query,
                ]
            )

            logger.info(f"Docs TOC Node Raw Response: {response}")
            json_res = response.model_dump()
            res_list = json_res["selected_docs"]

            return {"target_docs": res_list}
        except Exception as e:
            logger.error(f"Error in Docs_toc_node: {e}")
            return {"target_docs": []}

    return Docs_toc_node
