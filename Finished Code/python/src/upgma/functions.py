from datatypes import Node, Tree, DistanceMatrix

def upgma(mtx: DistanceMatrix, species_names: list[str]) -> Tree:
    """
    Build a phylogenetic tree using the UPGMA algorithm.

    Given a distance matrix and species names, iteratively merges the closest
    clusters and updates the matrix using cluster-size–weighted averages.
    The resulting tree has `n` leaves (the species) and `n-1` internal nodes.

    Args:
        mtx (DistanceMatrix): Square symmetric matrix of pairwise distances.
        species_names (list[str]): Names of the species, in the same order as `mtx`.

    Returns:
        Tree: A list of `Node` objects representing the full UPGMA tree.
              Conventionally, the last node (index -1) is the root.
    """
    # let's call our assertions
    assert_square_matrix(mtx)
    assert_same_number_species(mtx, species_names)

    num_leaves = len(mtx)

    # initialize the tree by creating nodes and assigning species names to the leaves
    t = initialize_tree(species_names)

    clusters = t[:num_leaves]

    # range over all the internal nodes, and iterate one step of UPGMA algorithm 
    for p in range(num_leaves, 2*num_leaves-1):
        # working with t[p]

        # find min element
        row, col, min_val = find_min_element(mtx)

        # set the age of t[p]
        t[p].age = min_val/2.0

        # set its children 
        t[p].child1 = clusters[row]
        t[p].child2 = clusters[col]

        cluster_size_1 = t[p].child1.count_leaves()  # or clusters[row]
        cluster_size_2 = t[p].child2.count_leaves()  # or clusters[col]

        # update the distance matrix 
        mtx = add_row_col(row, col, cluster_size_1, cluster_size_2, mtx)

        mtx = delete_row_col(mtx, row, col)

        # update the clusters
        clusters.append(t[p])
        clusters = delete_clusters(clusters, row, col)


    return t

def assert_square_matrix(mtx: DistanceMatrix) -> None:
    """
    Validate that a distance matrix is square.

    Args:
        mtx (DistanceMatrix): The matrix to validate.

    Raises:
        ValueError: If the matrix is not square.
    """
    num_rows = len(mtx)

    if num_rows == 0:
        raise ValueError("Error: empty matrix.")

    for r in range(num_rows):
        if len(mtx[r]) != num_rows:
            raise ValueError("Error: matrix not square.")

    # there are lots of other things we could check about the matrix: all values non-negative, main diagonal zero, matrix symmetric, etc.


def assert_same_number_species(mtx: DistanceMatrix, species_names: list[str]) -> None:
    """
    Validate that the number of species matches the matrix dimension.

    Args:
        mtx (DistanceMatrix): Square distance matrix.
        species_names (list[str]): Species labels.

    Raises:
        ValueError: If their sizes do not match.
    """
    if len(species_names) != len(mtx):
        raise ValueError("Error: mismatched number of species and matrix rows.")


def add_row_col(row: int, col: int, cluster_size1: int, cluster_size2: int, mtx: DistanceMatrix) -> DistanceMatrix:
    """
    Add a new cluster (row/column) to the matrix via size-weighted averaging.

    Computes distances from the new merged cluster to each existing cluster
    using a weighted average by cluster sizes, then appends this as a new
    row/column at the end of the matrix.

    Args:
        row (int): Index of the first merged cluster (row < col).
        col (int): Index of the second merged cluster.
        cluster_size1 (int): Number of leaves in the first cluster.
        cluster_size2 (int): Number of leaves in the second cluster.
        mtx (DistanceMatrix): The current distance matrix.

    Returns:
        DistanceMatrix: The matrix with the new cluster appended as the last row/column.
    """
    # create my new row that we will eventually add to the matrix 
    num_rows = len(mtx)
    new_row = [0.0] * (num_rows + 1)

    # set values of the new row 
    for r in range(len(new_row)-1):  # this is num_rows also 
        # set values that are not indices row and col
        if r != row and r != col:
            # this is WPGMA (w = weighted)
            new_row[r] = (cluster_size1 * mtx[r][row] + cluster_size2 * mtx[r][col])/(cluster_size1 + cluster_size2)

    # append new row we created to mtx 
    mtx.append(new_row)

    # range over rows, and append new_row[r] to row r 
    for r in range(len(new_row)-1):
        mtx[r].append(new_row[r])

    return mtx

def delete_clusters(clusters: list[Node], row: int, col: int) -> list[Node]:
    """
    Remove two cluster representatives at indices `row` and `col`.

    This is used after we merge those two clusters into a new one.

    Args:
        clusters (list[Node]): Active cluster representatives.
        row (int): Index of the first cluster (row < col).
        col (int): Index of the second cluster.

    Returns:
        list[Node]: Updated list of cluster representatives with the two removed.
    """
    # thank you python for having a built-in delete function 

    # no
    # del clusters[row]
    # del clusters[col]

    # when deleting multiple elements of a list, start with the one that occurs last and move back to front 
    del clusters[col]
    del clusters[row]

    return clusters


def delete_row_col(mtx: DistanceMatrix, row: int, col: int) -> DistanceMatrix:
    """
    Delete two rows and two columns (row/col) from the matrix.

    This is used after appending the new merged cluster at the end.

    Args:
        mtx (DistanceMatrix): The distance matrix.
        row (int): The first row/column index to delete (row < col).
        col (int): The second row/column index to delete.

    Returns:
        DistanceMatrix: The matrix with the specified rows/columns removed.
    """
    # first, delete rows
    # we also want to delete later rows first
    del mtx[col]
    del mtx[row]

    num_rows = len(mtx) 
    # next, delete columns
    for r in range(num_rows):
        del mtx[r][col]
        del mtx[r][row]

    return mtx



def find_min_element(mtx: DistanceMatrix) -> tuple[int, int, float]:
    """
    Find the indices (i, j) of the smallest strictly upper-triangular entry.

    Args:
        mtx (DistanceMatrix): A square matrix with size >= 2.

    Returns:
        tuple[int, int, float]: (row_index, col_index, min_value) with col_index > row_index.

    Raises:
        ValueError: If the matrix is smaller than 2x2.
    """
    # range over values of the matrix and find the minimum 
    # let's start at (0, 1)
    if len(mtx) <= 1 or len(mtx[0]) <= 1:
        raise ValueError("Matrix has only one row or column.")
    row = 0 
    col = 1 
    min_val = mtx[row][col]

    # range over matrix values, finding the minimum 
    for i in range(len(mtx)-1):
        for j in range(i+1, len(mtx[i])):
                if mtx[i][j] < min_val:
                    row, col, min_val = i, j, mtx[i][j]

    return row, col, min_val



def initialize_tree(species_names: list[str]) -> Tree:
    """
    Initialize a tree container for UPGMA with labeled leaves and internal nodes.

    Creates a list of 2n - 1 nodes:
      - The first n nodes (0..n-1) are leaves labeled by species_names.
      - The remaining n - 1 nodes (n..2n-2) are internal nodes labeled as ancestors.

    Args:
        species_names (list[str]): Species labels.

    Returns:
        Tree: The preallocated list of `Node` objects used by UPGMA.
    """
    num_leaves = len(species_names)

    t: Tree = []

    for i in range(2 * num_leaves - 1):
        if i < num_leaves:
            t.append(Node(label=species_names[i]))
        else:
            t.append(Node(label=f"Ancestor Species: {i}"))

    return t

