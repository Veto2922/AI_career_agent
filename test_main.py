# from src.data_ingestion_block.data_ingestion import DataIngestion


# di = DataIngestion()

# di.upload_file("data/resume.pdf")


##########################################################


from src.retrieval_block.tree_retrieval import TreeRetrieval

import os
from dotenv import load_dotenv
from pageindex import PageIndexClient
from loguru import logger

load_dotenv()

Page_index_api = os.getenv("Page_index_api")

pi_client = PageIndexClient(api_key=Page_index_api)

tr = TreeRetrieval(pi_client)

target_docs = [{"doc_index": 0, "target_ids": ["0007"]}]

print(tr.get_docs_titles())

print(" * " * 50)

print(tr.get_toc([0, 1]))

print(" * " * 50)
print(tr.retrieve(target_docs))
