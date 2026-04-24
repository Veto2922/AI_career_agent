from loguru import logger

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
