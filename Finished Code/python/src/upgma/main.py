from functions import upgma
from io_util import read_matrix_from_file, write_newick_to_file
from datatypes import Node


def main() -> None:
    print("Happy trees.")

    filename = "Data/HBA1/hemoglobin.mtx"

    # read in data from file
    species_names, mtx = read_matrix_from_file(filename)

    # generate our tree 

    t = upgma(mtx, species_names)

    print("Tree made.")

    # write our tree to file in order to visualize

    write_newick_to_file(t, "Output/HBA1", "hba1.tre")

    print("Tree written to file.")

if __name__ == "__main__":
    main()