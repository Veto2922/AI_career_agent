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
