from dataclasses import dataclass

@dataclass
class Node:
    """
    Represents a node in a directed graph.

    Attributes:
        id (int): Unique identifier for the node.
        neighbors (list[Node] | None): Outgoing edges from this node.
    """
    id: int
    neighbors: list | None = None

    def DFS(self) -> list:
        """
        Perform a depth-first search starting from this node to detect a cycle.

        This DFS is implemented iteratively using an explicit Stack object.
        The stack stores *paths* (lists of Node objects). A cycle is detected
        when we see a child that already appears in the current path.

        Returns:
            list[Node]: A list of nodes representing a directed cycle
                        (in order) if one is found. If no cycle exists,
                        returns an empty list [].
        """
        # TODO: implement
        pass


class Stack:
    """
    Simple stack data structure for DFS.
    """

    def __init__(self):
        self.data: list = []

    def push(self, item) -> None:
        """Push an item onto the top of the stack."""
        self.data.append(item)

    def pop(self):
        """
        Pop and return the top item from the stack.
        Returns None if the stack is empty.
        """
        if len(self.data) == 0:
            return None
        # Manual pop to emphasize what's happening (no built-in pop used)
        item = self.data[len(self.data) - 1]
        self.data = self.data[0 : len(self.data) - 1]
        return item

    def is_empty(self) -> bool:
        """Return True if the stack has no items, False otherwise."""
        return len(self.data) == 0