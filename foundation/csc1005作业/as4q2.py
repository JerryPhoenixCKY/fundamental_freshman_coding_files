class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree_from_list(tree_list: list) -> TreeNode:
    """
    根据列表构建二叉树。
    列表表示方式：根节点在索引0，左子节点在2*i+1，右子节点在2*i+2。
    空节点用None表示。
    """
    if not tree_list:
        return None

    nodes = [None] * len(tree_list)
    for i, val in enumerate(tree_list):
        if val is not None:
            nodes[i] = TreeNode(val)

    for i, node in enumerate(nodes):
        if node is not None:
            left_child_index = 2 * i + 1
            right_child_index = 2 * i + 2

            if left_child_index < len(tree_list):
                node.left = nodes[left_child_index]
            if right_child_index < len(tree_list):
                node.right = nodes[right_child_index]
    return nodes[0] # 返回根节点

def dfs_traversal(tree: list, order: str) -> list:
    """
    对二叉树进行深度优先遍历（DFS）。

    Args:
        tree: 二叉树的列表表示。
        order: 遍历顺序，可选值为 "preorder", "inorder", "postorder"。

    Returns:
        包含遍历结果的列表。
    """
    root = build_tree_from_list(tree) # 首先将列表转换为树结构

    result = []

    def _preorder(node):
        if not node:
            return
        result.append(node.val)
        _preorder(node.left)
        _preorder(node.right)

    def _inorder(node):
        if not node:
            return
        _inorder(node.left)
        result.append(node.val)
        _inorder(node.right)

    def _postorder(node):
        if not node:
            return
        _postorder(node.left)
        _postorder(node.right)
        result.append(node.val)

    if order == "preorder":
        _preorder(root)
    elif order == "inorder":
        _inorder(root)
    elif order == "postorder":
        _postorder(root)
    else:
        raise ValueError("无效的遍历顺序，请选择 'preorder', 'inorder' 或 'postorder'.")

    return result
