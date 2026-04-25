from langchain.messages import AIMessage, HumanMessage, SystemMessage
from src.graph_block.schemas.graph_state import GraphState
from src.graph_block.prompts.generator_prompt import Generator_SYSTEM_PROMPT
from src.Services.llm_services.llm_factory import LLMFactory
from src.graph_block.tools.career_tools import tools
from loguru import logger

generator_node_llm = LLMFactory.create("gemini").bind_tools(tools)


def create_generator_node(tree_retrieval):
    def generator_node(state: GraphState):
        """
        Generates the final response based on retrieved context and user query.
        """
        try:
            logger.info("Starting generator_node")
            retrieved_content = tree_retrieval.retrieve(state.target_docs)
            user_query = HumanMessage(content=state.user_query)

            response = generator_node_llm.invoke(
                [
                    SystemMessage(
                        content=Generator_SYSTEM_PROMPT.format(
                            retrieved_docs=retrieved_content
                        )
                    ),
                    user_query,
                ]
                + state.messages
            )

            logger.info(f"Generator Response: {response}")
            res = response.content

            # If the LLM didn't return content but made a tool call, the content might be empty
            # We must return the response message to allow tool calls to be processed
            return {"messages": [user_query, response]}
        except Exception as e:
            logger.error(f"Error in generator_node: {e}")
            return {"messages": [AIMessage(content="عذراً، حدث خطأ أثناء معالجة طلبك.")]}

    return generator_node
