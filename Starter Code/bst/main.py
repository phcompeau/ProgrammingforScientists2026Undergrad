import bisect
import os
import sys
import time
from dataclasses import dataclass
from typing import Self

# These six populations evolved much higher mutation rates.
MUTATORS: list[str] = ["Ara+3", "Ara+6", "Ara-1", "Ara-2", "Ara-3", "Ara-4"]

FOLDER: str = os.path.dirname(os.path.abspath(__file__))

# False: run only the search, insert, and in-order demos (instant).
# True: also race a sorted list against a BST on the real LTEE catalog (a few seconds).
RUN_FULL_DEMO: bool = False


@dataclass
class Node:
    """
    A node in a binary search tree of mutation positions.

    Attributes:
        label (int): A position in the genome where we found a mutation.
        left_child (Node | None): The left child, or None.
        right_child (Node | None): The right child, or None.
    """

    label: int = 0
    left_child: Self | None = None
    right_child: Self | None = None

    def search_recursive(self, key: int) -> Self | None:
        """
        MUST COVER IN RECITATION.

        Find the node of this BST whose label equals key.

        Parameters:
        - key (int): The position to look for.

        Returns:
        - Node | None: The node whose label is key, or None if no node has
          that label.
        """
        return None

    def insert_recursive(self, key: int) -> Self:
        """
        MUST COVER IN RECITATION.

        Insert key into the BST rooted at this node, keeping it a BST.

        Parameters:
        - key (int): The position to insert.

        Returns:
        - Node: The node whose label is key. If key is already in the tree,
          nothing changes.
        """
        return self

    def inorder_traversal(self) -> list[int]:
        """
        Cover next, if there is time after search and insert.

        List the labels of this BST in in-order: left subtree, node, right
        subtree.

        Returns:
        - list[int]: The labels in increasing order.
        """
        return []

    def range_count(self, low: int, high: int) -> int:
        """
        Already written for you.

        Count the labels of this BST with low <= label <= high, skipping any
        subtree that cannot hold a label in range.

        Parameters:
        - low (int): The start of the range (for us, the start of a gene).
        - high (int): The end of the range (the end of the gene).

        Returns:
        - int: How many labels lie in the range.
        """
        count: int = 0
        if low <= self.label and self.label <= high:
            count = 1
        if self.left_child is not None and low < self.label:
            count += self.left_child.range_count(low, high)
        if self.right_child is not None and self.label < high:
            count += self.right_child.range_count(low, high)
        return count


def print_tree(node: Node | None, depth: int) -> None:
    """
    Print a tree on its side: the root at the left edge, the right subtree
    above it, and the left subtree below it. Already written for you.

    Parameters:
    - node (Node | None): The root of the (sub)tree to print.
    - depth (int): How far to indent this node (0 for the root).
    """
    if node is None:
        return
    print_tree(node.right_child, depth + 1)
    print("    " * depth + str(node.label))
    print_tree(node.left_child, depth + 1)


def slide_tree() -> Node:
    """
    Build the running tree from the slides by hand, so we can search it
    before insert is written. Already written for you.

    Returns:
    - Node: The root (7) of the tree with labels 7, 3, 8, 1, 6, 15.
    """
    return Node(7, Node(3, Node(1), Node(6)), Node(8, None, Node(15)))


def build_bst(positions: list[int]) -> Node:
    """
    Insert positions one at a time, in the order given, into a new BST.

    Parameters:
    - positions (list[int]): Mutation positions; the first becomes the root.

    Returns:
    - Node: The root of the tree.
    """
    root: Node = Node(positions[0])
    for position in positions[1:]:
        root.insert_recursive(position)
    return root


def build_sorted_list(positions: list[int]) -> list[int]:
    """
    Insert positions one at a time into a sorted list, the way we would
    keep a sorted array up to date.

    Parameters:
    - positions (list[int]): Mutation positions.

    Returns:
    - list[int]: The positions in increasing order (repeats skipped).
    """
    catalog: list[int] = []
    for position in positions:
        index: int = bisect.bisect_left(catalog, position)
        if index == len(catalog) or catalog[index] != position:
            catalog.insert(index, position)
    return catalog


def read_catalog(filename: str) -> dict[str, list[int]]:
    """
    Read the LTEE mutation catalog (one mutation per line, from sequenced
    clones) and group the positions by population.

    Parameters:
    - filename (str): Tab-separated file with columns population,
      generation, clone, type, position.

    Returns:
    - dict[str, list[int]]: Each population's mutation positions, in file
      order.
    """
    catalog: dict[str, list[int]] = {}
    handle = open(filename)
    handle.readline()
    for line in handle:
        fields: list[str] = line.rstrip("\n").split("\t")
        population: str = fields[0]
        if population not in catalog:
            catalog[population] = []
        catalog[population].append(int(fields[4]))
    handle.close()
    return catalog


def read_observations(filename: str) -> list[int]:
    """
    Read every mutation observation in the LTEE catalog, in the order the
    clones were sampled (generation 500 first). Two clones carrying the same
    mutation are two observations, so each gets its own key: its position
    times 1,000, plus a number for its clone (there are 303 clones).

    Parameters:
    - filename (str): Tab-separated file with columns population,
      generation, clone, type, position.

    Returns:
    - list[int]: One distinct key per observation, in generation order.
    """
    clone_numbers: dict[str, int] = {}
    by_generation: dict[int, list[int]] = {}
    handle = open(filename)
    handle.readline()
    for line in handle:
        fields: list[str] = line.rstrip("\n").split("\t")
        clone: str = fields[0] + " " + fields[2]
        if clone not in clone_numbers:
            clone_numbers[clone] = len(clone_numbers)
        generation: int = int(fields[1])
        if generation not in by_generation:
            by_generation[generation] = []
        by_generation[generation].append(int(fields[4]) * 1000 + clone_numbers[clone])
    handle.close()
    observations: list[int] = []
    for generation in sorted(by_generation):
        observations = observations + by_generation[generation]
    return observations


def read_genes(filename: str) -> list[tuple[str, int, int]]:
    """
    Read the REL606 gene table.

    Parameters:
    - filename (str): Tab-separated file with columns gene, start, end.

    Returns:
    - list[tuple[str, int, int]]: (name, start, end) for every gene.
    """
    genes: list[tuple[str, int, int]] = []
    handle = open(filename)
    handle.readline()
    for line in handle:
        fields: list[str] = line.rstrip("\n").split("\t")
        genes.append((fields[0], int(fields[1]), int(fields[2])))
    handle.close()
    return genes


def populations_hit(trees: dict[str, Node], start: int, end: int) -> int:
    """
    Count the populations whose tree has at least one mutation in a gene.

    Parameters:
    - trees (dict[str, Node]): One BST of mutation positions per population.
    - start (int): The start of the gene.
    - end (int): The end of the gene.

    Returns:
    - int: The number of populations with a mutation in [start, end].
    """
    hits: int = 0
    for population in trees:
        if trees[population].range_count(start, end) > 0:
            hits += 1
    return hits


def main() -> None:
    print("Binary search trees!")

    print()
    print("Search (the tree from the slides):")
    root: Node = slide_tree()
    print_tree(root, 0)
    found: Node | None = root.search_recursive(6)
    if found is None:
        print("search_recursive(6) returned None")
    else:
        print("search_recursive(6) returned the node labeled", found.label)
    found = root.search_recursive(4)
    if found is None:
        print("search_recursive(4) returned None: no mutation at position 4")
    else:
        print("search_recursive(4) returned the node labeled", found.label)

    print()
    print("Insert (a new clone has a mutation at position 5):")
    root.insert_recursive(5)
    print_tree(root, 0)

    print()
    print("In-order traversal (the mutations along the genome):")
    print(root.inorder_traversal())

    print()
    print("Range count (already written for you):")
    print("Mutations in 'pykF' (positions 5 to 7):", root.range_count(5, 7))
    print("Mutations in 'gene B' (positions 9 to 14):", root.range_count(9, 14))

    if not RUN_FULL_DEMO:
        print()
        print("Set RUN_FULL_DEMO = True at the top of this file to run the rest.")
        return

    print()
    print("Part 2: racing a sorted list against a BST on the real LTEE catalog.")
    observations: list[int] = read_observations(os.path.join(FOLDER, "ltee_mutations.tsv"))
    print("Inserting all", len(observations), "observations, generation by generation:")
    start: float = time.time()
    build_sorted_list(observations)
    list_seconds: float = time.time() - start
    start = time.time()
    race_tree: Node = build_bst(observations)
    bst_seconds: float = time.time() - start
    if race_tree.left_child is None and race_tree.right_child is None:
        print("The BST has only one node: implement insert_recursive first.")
        return
    print("sorted list:", round(list_seconds, 2), "s   BST:", round(bst_seconds, 2), "s   speedup:",
          round(list_seconds / bst_seconds, 1), "times")

    print()
    print("Part 3: which genes were hit in every population?")
    catalog: dict[str, list[int]] = read_catalog(os.path.join(FOLDER, "ltee_mutations.tsv"))
    genes: list[tuple[str, int, int]] = read_genes(os.path.join(FOLDER, "genes.tsv"))
    records: int = 0
    trees: dict[str, Node] = {}
    start = time.time()
    for population in sorted(catalog):
        records += len(catalog[population])
        trees[population] = build_bst(catalog[population])
    print("Built", len(trees), "trees, one per population, from", records, "records in",
          round(time.time() - start, 2), "seconds.")
    print("Ara-1's first five mutations along the genome:", trees["Ara-1"].inorder_traversal()[:5])

    print("Genes with a mutation in all 12 populations:")
    for name, gene_start, gene_end in genes:
        if populations_hit(trees, gene_start, gene_end) == 12:
            print("   ", name, "(positions " + str(gene_start) + " to " + str(gene_end) + ")")

    steady: dict[str, Node] = {}
    for population in trees:
        if population not in MUTATORS:
            steady[population] = trees[population]
    print("The same genes in the", len(steady), "populations without high mutation rates:")
    for name, gene_start, gene_end in genes:
        if populations_hit(trees, gene_start, gene_end) == 12:
            print("   ", name, "hit in", populations_hit(steady, gene_start, gene_end), "of", len(steady))

    print()
    print("Part 4: what if the catalog arrives already sorted?")
    every_position: list[int] = []
    for population in catalog:
        every_position = every_position + catalog[population]
    in_order: list[int] = sorted(set(every_position))
    try:
        build_bst(in_order)
        print("Built the tree.")
    except RecursionError:
        print("RecursionError: inserting", len(in_order),
              "sorted positions builds one long chain, deeper than Python allows.")
    print("The recursion limit is", sys.getrecursionlimit())


if __name__ == "__main__":
    main()
