from dataclasses import dataclass

# three things: distance matrix alias,
# node declaration,
# tree declaration


@dataclass
class Node:
    """
    Represents a node in a phylogenetic tree.

    Attributes:
        label (str): species name for leaves, ancestor name for internal nodes
        age (float): represents its "age" from the leaves
        child1: the first child node, or None if it doesn't exist
        child2: the second child node, or None if it doesn't exist
    """

    label: str = "Unlabeled"
    age: float = 0.0
    child1: 'Node | None' = None
    child2: 'Node | None' = None

    def is_leaf(self) -> bool:
        """
        Method that returns true if given node is a leaf and false otherwise.
        """
        if self.child1 is None and self.child2 is None:
            return True
        return False

    def count_leaves(self) -> int:
        """
        Count the number of leaf nodes in the subtree rooted at this node.
        """
        #TODO: Implement
        pass

    def to_newick_ages(self) -> str:
        """
        Recursively serialize this subtree to Newick with branch lengths,
        where each branch length = parent.age - child.age.

        Returns:
            Newick string for this subtree (no trailing semicolon).
        """
        #TODO: Implement
        pass


# alias declarations

DistanceMatrix = list[list[float]]

Tree = list[Node]
