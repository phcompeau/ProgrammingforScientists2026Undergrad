import csv
from datatypes import Tree, Node, DistanceMatrix


def write_newick_to_file(t: Tree, file_dest: str, file_name: str) -> None:
    """
    Write a phylogenetic tree to a file in Newick format.

    Args:
        t: The tree to serialize.
        file_dest: Destination directory (no trailing slash required).
        file_name: Output filename (e.g., "tree.nwk").
    """
    newick_string = to_newick(t)
    with open(f"{file_dest}/{file_name}", "w", newline="") as f:
        f.write(newick_string)


def to_newick(tree: Tree) -> str:
    """
    Convert an entire tree to a Newick-formatted string.

    Args:
        tree: The phylogenetic tree (root is at tree[-1]).

    Returns:
        The Newick representation of the tree, terminated with a semicolon.
    """
    return f"({tree[-1].to_newick_ages()});"


def read_matrix_from_file(filename: str) -> tuple[list[str], DistanceMatrix]:
    """
    Read a distance matrix and corresponding species names from a CSV file.

    Expected CSV layout (no header):
      - Column 0: species name (string)
      - Columns 1..N: numeric distances to other species (floats)

    Args:
        filename: Path to the CSV file.

    Returns:
        (species_names, distance_matrix):
            species_names: list[str]
            distance_matrix: 2D list of floats (DistanceMatrix)
    """
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        records = [row for row in reader if row]

    species: list[str] = []
    distance_matrix: DistanceMatrix = []

    for record in records:
        species.append(record[0])
        row = [float(x) for x in record[1:]]
        distance_matrix.append(row)

    return species, distance_matrix