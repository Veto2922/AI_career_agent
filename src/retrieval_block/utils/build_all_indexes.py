from pageindex import PageIndexClient
from .build_index import build_index

def build_all_indexes(pi_client: PageIndexClient, docs_list):
    all_indexes = {}

    for i, doc in enumerate(docs_list.get("documents", [])):
        doc_id = doc["id"]

        tree_result = pi_client.get_tree(doc_id, node_summary=True)
        nodes = tree_result.get("result", [])

        all_indexes[i] = build_index(nodes)  # store index per doc

    return all_indexes
