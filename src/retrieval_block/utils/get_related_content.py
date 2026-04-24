from loguru import logger
from .clean_child_nodes import clean_child_nodes

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
