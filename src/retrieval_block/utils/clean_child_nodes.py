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
