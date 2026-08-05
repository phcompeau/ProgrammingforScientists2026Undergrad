from datatypes import Node, Tree, DistanceMatrix

def upgma(mtx: DistanceMatrix, species_names: list[str]) -> Tree:
    """
    Build a phylogenetic tree using the UPGMA algorithm.

    Given a distance matrix and species names, iteratively merges the closest
    clusters and updates the matrix using cluster-size-weighted averages.
    The resulting tree has `n` leaves (the species) and `n-1` internal nodes.

    Args:
        mtx (DistanceMatrix): Square symmetric matrix of pairwise distances.
        species_names (list[str]): Names of the species, in the same order as `mtx`.

    Returns:
        Tree: A list of `Node` objects representing the full UPGMA tree.
              Conventionally, the last node (index -1) is the root.
    """
    #TODO: Implement
    pass


def assert_square_matrix(mtx: DistanceMatrix) -> None:
    """
    Validate that a distance matrix is square.

    Args:
        mtx (DistanceMatrix): The matrix to validate.

    Raises:
        ValueError: If the matrix is empty or not square.
    """
    #TODO: Implement
    pass


def assert_same_number_species(mtx: DistanceMatrix, species_names: list[str]) -> None:
    """
    Validate that the number of species matches the matrix dimension.

    Args:
        mtx (DistanceMatrix): Square distance matrix.
        species_names (list[str]): Species labels.

    Raises:
        ValueError: If their sizes do not match.
    """
    #TODO: Implement
    pass


def add_row_col(row: int, col: int, cluster_size1: int, cluster_size2: int, mtx: DistanceMatrix) -> DistanceMatrix:
    """
    Append a new row and column for the merged cluster.

    Args:
        row (int): Index of the first cluster to merge (row < col).
        col (int): Index of the second cluster to merge.
        cluster_size1 (int): Leaf count of the first cluster.
        cluster_size2 (int): Leaf count of the second cluster.
        mtx (DistanceMatrix): The current distance matrix.

    Returns:
        DistanceMatrix: The matrix with one new row and column added.
    """
    #TODO: Implement
    pass


def delete_clusters(clusters: list[Node], row: int, col: int) -> list[Node]:
    """
    Remove two merged clusters from the cluster list.

    Args:
        clusters (list[Node]): The active cluster list.
        row (int): Index of the first cluster to remove (row < col).
        col (int): Index of the second cluster to remove.

    Returns:
        list[Node]: The updated cluster list.
    """
    #TODO: Implement
    pass


def delete_row_col(mtx: DistanceMatrix, row: int, col: int) -> DistanceMatrix:
    """
    Remove two rows and columns from the distance matrix.

    Args:
        mtx (DistanceMatrix): The current distance matrix.
        row (int): Row/column index of the first cluster (row < col).
        col (int): Row/column index of the second cluster.

    Returns:
        DistanceMatrix: The matrix with two rows and columns removed.
    """
    #TODO: Implement
    pass


def find_min_element(mtx: DistanceMatrix) -> tuple[int, int, float]:
    """
    Scan the upper triangle of mtx for the minimum value.

    Args:
        mtx (DistanceMatrix): A square distance matrix (at least 2x2).

    Returns:
        tuple[int, int, float]: (row, col, min_val) where row < col.

    Raises:
        ValueError: If the matrix has only one row or column.
    """
    #TODO: Implement
    pass


def initialize_tree(species_names: list[str]) -> Tree:
    """
    Allocate all 2n - 1 nodes for a tree with n leaves.

    Args:
        species_names (list[str]): Names for the n leaf nodes.

    Returns:
        Tree: A Tree of labeled leaves followed by unlabeled internal nodes.
    """
    #TODO: Implement
    pass
