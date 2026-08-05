from dataclasses import dataclass

@dataclass
class Node:
    """
    Represents a node in a general (binary) tree.

    Attributes:
        age (float): Optional stored numeric value (unused in depth computation).
        label (str): Optional descriptive label.
        child1 (Node | None): First child.
        child2 (Node | None): Second child.
    """

    age: float = 0.0
    label: str = ""
    child1: "Node | None" = None
    child2: "Node | None" = None

    def depth(self) -> int:
        """
        Compute the depth of the subtree rooted at this node.

        Depth is defined as:
        - A leaf has depth 1.
        - Otherwise: depth = 1 + max(depth(child1), depth(child2)).

        Returns:
            int: The depth of this node.
        """
        # TODO: implement
        pass