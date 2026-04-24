from pageindex import PageIndexClient

def build_all_trees_index(pi_client: PageIndexClient, docs_list: dict) -> dict:
    """
    Build all trees once and store them in memory
    """
    all_trees = {}

    for i, doc in enumerate(docs_list.get("documents", [])):
        doc_id = doc["id"]

        tree_result = pi_client.get_tree(doc_id, node_summary=True)
        tree = tree_result.get("result", [])

        all_trees[i] = tree

    return all_trees
