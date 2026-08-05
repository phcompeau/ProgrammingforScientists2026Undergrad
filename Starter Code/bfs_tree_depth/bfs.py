from dataclasses import dataclass, field

# Node represents a node in the tree.
@dataclass
class Node:
    id: int
    neighbors: list["Node"] | None = None

    # Insert your BFS() function here, along with any subroutines that you need.
    def BFS(self, target: int):
        """
        Perform a breadth-first search starting from this node,
        returning the shortest path (as a list of Node objects)
        to the node whose id == target.

        If no such node exists, return an empty list.
        """
        # TODO: implement
        pass

# BFS encapsulates the state and behavior needed for breadth-first search.
@dataclass
class BFS:
    queue: list | None = None  # The queue of paths to explore.
    visited: list | None = None # Map to track visited nodes.
        
    def __init__(self):
        self.queue = []
        self.visited = []

    # Enqueue adds a new path to the BFS queue.
    def Enqueue(self, path):
        self.queue.append(path)

    # Dequeue removes and returns the first path from the BFS queue.
    def Dequeue(self):
        if len(self.queue) == 0:
            return None
        path = self.queue[0]
        self.queue = self.queue[1:]
        return path