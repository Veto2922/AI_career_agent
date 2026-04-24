from loguru import logger
from pageindex import PageIndexClient
from .get_tree_toc import get_tree_toc

def get_docs_toc(
    pi_client: PageIndexClient,
    docs_list,
    docs_index: list,
    all_trees_index: dict = None   
):
    try:
        docs_tocs = []

        for i in docs_index:
            if i >= len(docs_list["documents"]):
                logger.warning(f"Document index {i} is out of range. Skipping.")
                continue

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
        return []
