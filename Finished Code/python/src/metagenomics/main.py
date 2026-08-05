from functions import (
    simpsons_index,
    simpsons_map,
    beta_diversity_matrix,
)

from custom_io import (
    read_frequency_map_from_file,
    read_samples_from_directory,
    write_simpsons_map_to_file,
    write_beta_diversity_matrix_to_file,
)

def main():
    print("Metagenomics!")

    # Step 1: reading input from a single file.

    file_name = "Data/Fall_Allegheny_1.txt"
    freq_map = read_frequency_map_from_file(file_name)

    print("File read successfully.")

    print("We have", len(freq_map), "unique sequences.")

    # we may as well do something with our file. For example, let's print its Simpson's Index.
    print("Simpson's Index:", simpsons_index(freq_map))

    # step 2: reading input from a directory
    path = "Data/"
    all_maps = read_samples_from_directory(path)

    print("Read", len(all_maps), "files from directory.")

    simpson = simpsons_map(all_maps)

    dist_metric = "Bray-Curtis"
    sample_names, mtx = beta_diversity_matrix(all_maps, dist_metric)

    # We cannot really analyze anything from this printing.

	# It would be better to print to a file.  Hence, we will need to learn writing to a file.

    simpson_file = "Matrices/SimpsonMatrix.csv"
    write_simpsons_map_to_file(simpson, simpson_file)

    matrix_file = "Matrices/BetaDiversityMatrix.csv"
    write_beta_diversity_matrix_to_file(mtx, sample_names, matrix_file)

    print("Matrices written to file.")

if __name__ == "__main__":
    main()