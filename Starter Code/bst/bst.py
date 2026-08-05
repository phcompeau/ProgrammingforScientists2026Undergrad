from dataclasses import dataclass
from typing import Self

@dataclass
class Node:
    """
    Represents a node in a binary search tree (BST).

    Attributes:
        label (int): The value stored in the node.
        left_child (Node | None): The left child of this node.
        right_child (Node | None): The right child of this node.
    """

    label: int = 0
    left_child: Self | None = None   # left child
    right_child: Self | None = None   # right child

    def is_leaf(self) -> bool:
        """
        Return whether this node is a leaf (i.e., has no children).

        Returns:
            bool: True if both left_child and right_child are None, False otherwise.
        """
        if self.left_child is None and self.right_child is None:
            return True
        return False

    def count_leaves(self) -> int:
        """
        Recursively count the number of leaf nodes in the subtree rooted at this node.

        Returns:
            int: The number of leaves under this node.
        """
        if self.is_leaf():  # base case: we are at a leaf
            return 1

        leaves = 0
        if self.left_child is not None:
            leaves += self.left_child.count_leaves()
        if self.right_child is not None:
            leaves += self.right_child.count_leaves()
        return leaves

    def search_recursive(self, key: int) -> Node | None:
        """
        Recursively search for a key in a binary search tree (BST).

        Args:
            key (int): The value to search for.
            node (Node | None): The current node to start searching from.

        Returns:
            Node | None: The node containing the key if found; otherwise, None.
        """
        # TODO: implement
        pass    

    def insert_recursive(self, key: int, prev_node: Node) -> Node | None:
        """
        Recursively insert a key into a binary search tree (BST).

        Starting from this node, this method descends through the tree
        until it finds an empty position where the new key should be placed. A new
        Node is created and linked to its parent. If the key already exists in the
        tree, no new node is created.

        Args:
            key (int): The value to insert into the BST.
            prev_node (Node): The parent of the current node (used for linking).

        Returns:
            Node: The newly created node, or the existing node if the key is already present.
        """
        # TODO: implement
        pass    

        def inorder_traversal(self) -> list[Self]:
        """
        Perform an inorder traversal and return a list of nodes.

        Returns:
            list[Node]: List of nodes visited in inorder.
        """
        # TODO: implement
        pass    


def main():
    print("Binary search trees!")

    root = Node(3)
    insert_recursive(1, root, root)
    insert_recursive(5, root, root)

    print("In-order traversal:")
    print(root.inorder_traversal())

if __name__ == "__main__":
    main()