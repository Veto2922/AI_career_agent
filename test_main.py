# from src.data_ingestion_block.data_ingestion import DataIngestion


# di = DataIngestion()

# di.upload_file("data/resume.pdf")


##########################################################


# from src.retrieval_block.tree_retrieval import TreeRetrieval

# import os
# from dotenv import load_dotenv
# from pageindex import PageIndexClient
# from loguru import logger

# load_dotenv()

# Page_index_api = os.getenv("Page_index_api")

# pi_client = PageIndexClient(api_key=Page_index_api)

# tr = TreeRetrieval(pi_client)

# target_docs = [{"doc_index": 0, "target_ids": ["0007"]}]

# print(tr.get_docs_titles())

# print(" * " * 50)

# print(tr.get_toc([0, 1]))

# print(" * " * 50)
# print(tr.retrieve(target_docs))


#####################################################################
from src.graph_block.graph import compile_graph
from src.retrieval_block.tree_retrieval import TreeRetrieval
from pageindex import PageIndexClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("Page_index_api")

if not api_key:
    raise ValueError("PageIndex API key is missing.")

pi_client = PageIndexClient(api_key=api_key)


tree_retrieval = TreeRetrieval(pi_client)

agent = compile_graph(tree_retrieval)

docs_titles = tree_retrieval.get_docs_titles()

config = {"configurable": {"thread_id": "1"}}

res = agent.invoke(
    {"user_query": "ايه هي المشاريع الي اشتغلت عليها؟", "docs_titles": docs_titles},
    config,
)

for m in res["messages"]:
    m.pretty_print()
