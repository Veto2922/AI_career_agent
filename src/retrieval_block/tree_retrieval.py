from pageindex import PageIndexClient
from .utils.get_trees_titles import get_trees_titles
from .utils.get_docs_toc import get_docs_toc
from .utils.get_related_content import get_related_content
from .utils.build_all_indexes import build_all_indexes
from .utils.build_all_trees_index import build_all_trees_index


class TreeRetrieval:
    def __init__(self, pi_client: PageIndexClient):
        self.pi_client = pi_client
        self.docs_list = pi_client.list_documents()
        self.indexes = build_all_indexes(self.pi_client, self.docs_list)
        self.all_tree_index = build_all_trees_index(self.pi_client, self.docs_list)

    def get_docs_titles(self):
        return get_trees_titles(self.docs_list)

    def get_toc(self, doc_indices: list):  # doc_indices = [0 , 1 , 2 ...]
        return get_docs_toc(
            self.pi_client, self.docs_list, doc_indices, self.all_tree_index
        )

    def retrieve(
        self, target_docs: list[dict]
    ):  # target_docs = [{"doc_index": 0, "target_ids": [ "0007"]}]
        return get_related_content(self.indexes, self.docs_list, target_docs)
