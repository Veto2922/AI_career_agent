from loguru import logger

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
