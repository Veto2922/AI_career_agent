from loguru import logger
from pageindex import PageIndexClient

def get_trees_titles(docs_list: list) -> list[dict]:
    try:
        docs_titles = [
            {
                "doc_index": i,
                "name": doc.get("name"),
                "description": doc.get("description")
            }
            for i, doc in enumerate(docs_list.get("documents", []))
        ]

        return docs_titles

    except Exception as e:
        logger.exception("Error while trying to get the tree titles")


def get_tree_toc(tree: list) -> list:
    try:
        toc_structure = []

        for node in tree:
            new_node = {
                "node_id": node.get("node_id"),
                "title": node.get("title"),
                "node_summary": node.get("node_summary") 
                                or node.get("summary") 
                                or node.get("prefix_summary", ""),
                "child_nodes": []
            }

            children = node.get("nodes", [])
            if children:
                new_node["child_nodes"] = get_tree_toc(children)

            toc_structure.append(new_node)

        return toc_structure

    except Exception:
        logger.exception("Error while trying to get_tree_toc")
        return []


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


def get_docs_toc(
    pi_client: PageIndexClient,
    docs_list,
    docs_index: list,
    all_trees_index: dict = None   
):
    try:
        docs_tocs = []

        for i in docs_index:

            if all_trees_index and i in all_trees_index:
                tree = all_trees_index[i]
            else:
                # fallback (old behavior)
                doc_id = docs_list["documents"][i]['id']
                tree_result = pi_client.get_tree(doc_id, node_summary=True)
                tree = tree_result.get("result", [])

            docs_toc = {
                "doc_index": i,
                "doc_title": docs_list["documents"][i]["name"],
                "doc_toc": get_tree_toc(tree)
            }

            docs_tocs.append(docs_toc)

        return docs_tocs

    except Exception:
        logger.exception('Error while trying to get_docs_toc')


def build_index(nodes: list) -> dict:
    index = {}

    def dfs(node_list):
        for node in node_list:
            node_id = node.get("node_id")
            if node_id:
                index[node_id] = node

            children = node.get("nodes", [])
            if children:
                dfs(children)

    dfs(nodes)
    return index


def build_all_indexes(pi_client, docs_list):
    all_indexes = {}

    for i, doc in enumerate(docs_list.get("documents", [])):
        doc_id = doc["id"]

        tree_result = pi_client.get_tree(doc_id, node_summary=True)
        nodes = tree_result.get("result", [])

        all_indexes[i] = build_index(nodes)  # store index per doc

    return all_indexes


def clean_child_nodes(nodes: list) -> list:
    cleaned = []

    for node in nodes:
        cleaned.append({
            "node_id": node.get("node_id"),
            "title": node.get("title"),
            "page_num": node.get("page_index"),
            "node_text": node.get("text"),
            "child_nodes": clean_child_nodes(node.get("nodes", []))
        })

    return cleaned


def get_related_content(all_indexes: dict, docs_list: list, target_docs: list):
    try:
        pdfs_content = []

        for item in target_docs:
            doc_index = item["doc_index"]
            target_ids = item["target_ids"]

            index = all_indexes.get(doc_index, {})

            pdf_content = {
                "pdf_title": docs_list["documents"][doc_index]["name"]
            }

            results = [
                        {
                            "node_id": nid,
                            "title": index[nid].get("title"),
                            "page_num": index[nid].get("page_index"),
                            "node_text": index[nid].get("text"),
                            "child_nodes": clean_child_nodes(index[nid].get("nodes", []))
                        }
                        for nid in target_ids
                        if nid in index
                    ]

            pdf_content["pdf_related_content"] = results
            pdfs_content.append(pdf_content)

        return pdfs_content

    except Exception as e:
        logger.exception('Error while trying to get_related_content')
