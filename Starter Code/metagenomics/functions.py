def richness_map(all_maps: dict[str, dict[str, int]]) -> dict[str, int]:
    """
    Takes a dict of frequency maps and returns a dict mapping each sample
    name to its richness.
    """
    # TODO: Implement this function.
    pass    

def simpsons_map(all_maps: dict[str, dict[str, int]]) -> dict[str, float]:
    """
    Takes a dict of frequency maps and returns a dict mapping
    each sample name to its Simpson's index.
    """
    # TODO: Implement this function.
    pass    

def beta_diversity_matrix (
    all_maps: dict[str, dict[str, int]],
    dist_metric: str
) -> tuple[list[str], list[list[float]]]:
    """
    Compute a beta-diversity distance matrix between multiple samples.

    Parameters
    ----------
    all_maps : dict[str, dict[str, int]]
        A dictionary mapping sample names to frequency maps, where each
        frequency map records counts for species/patterns.
    dist_metric : str
        The distance metric to use. Must be either "Bray-Curtis" or "Jaccard".

    Returns
    -------
    tuple[list[str], list[list[float]]]
        - A list of sample names, sorted alphabetically.
        - A square matrix of distances (size = number of samples),
          where entry (i, j) is the distance between the i-th and j-th samples
          under the given metric.

    Notes
    -----
    - The returned matrix is symmetric with zeros on the diagonal.
    - Raises ValueError if an unsupported distance metric is provided.
    """
    # TODO: Implement this function.
    pass    

# HELPER FUNCTIONS BELOW

def richness(sample: dict) -> int:
    """
    richness finds the total number of values in the table that are positive.

    Parameters:
    - sample (dict): A dictionary that contains integer values.

    Returns:
    - int: The total number of values that are greater than zero.
    """
    
    # Defines the count for the number of keys with positive values.
    count = 0

    # Range through the values in the sample map.
    for _, val in sample.items():
        # If the value is >0, we add one to the count.
        if val > 0:
            count += 1

        # If the value is negative, we raise an error.
        if val < 0:
            raise ValueError

    # Return the count of the positive values.
    return count

def simpsons_index(sample: dict) -> float:
    """
    simpsons_index returns a the Simpson's index of a given sample. 
    This is the sum of the squared ratio of number of individual for
    a given key or species to the total number of individuals across
    alll keys.

    Parameters:
    - sample (dict): A given sample or frequency table.

    Returns:
    - float: The Simpson's index of the particular sample.
    """
    
    # Find the sum of values of the sample.
    total = sum_of_values(sample)

    # Create an empty float value to add to.
    simpson = 0.0

    # If the total value is 0, we throw a value error.
    if total == 0:
        raise ValueError("Error: Empty frequency map given to simpsons_index()!")

    # Range through the dictionary sample (the frequency map.)
    for _, val in sample.items():
        # Square the ratio of the value to the sum of all values.
        x = float(val) / float(total)

        # Add the square ratio to the simpson variable.
        simpson += x * x

    # Return the sum of all the squares of the ratios.
    return simpson

def jaccard_distance(sample1: dict, sample2: dict) -> float:
    """
    jaccard_distance computes the Jaccard distance between two samples or
    two frequency tables.

    Parameters:
    - sample1 (dict): A given frequency table or sample.
    - sample2 (dict): A second frequency table or sample.

    Returns:
    - float: The Jaccard distance between these two individual samples.
    """

    # Finds the sum of minima between two samples.
    sum_min = sum_of_minima(sample1, sample2)

    # Finds the sum of maxima between the two samples.
    sum_max = sum_of_maxima(sample1, sample2)

    # Returns 1 - the ratio of the sum of minima to the sum of maxima.
    return 1.0 - float(sum_min) / float(sum_max)



def sum_of_maxima(sample1: dict, sample2: dict) -> int:
    """
    sum_of_maxima returns the sum of the maxima of the values for shared keys
    across two samples. If a key is not shared it is still added to the sum.

    Parameters:
    - sample1 (dict): A given input sample.
    - sample2 (dict): Another given input sample.

    Returns:
    - int: The sum of the minima of all values for shared keys.  
    If a key is not shared it is still added to the sum.
    """

    # Define an empty sum variable.
    sum_result = 0
    # Range through the keys of one of the maps.
    for key, _ in sample1.items():
        # Is this key present in the other map?
        if key in sample2:  # yes
            # Add the maximum to the current sum
            sum_result += max_2(sample1[key], sample2[key])
        # If not present in the other map, add to the sum.
        else:
            sum_result += sample1[key]

    # If the key is not in sample 1, we add to the sum.
    for key, _ in sample2.items():
        if key not in sample1:
            sum_result += sample2[key]
    return sum_result

def bray_curtis_distance(sample1: dict, sample2: dict) -> float:
    """
    bray_curtis_distance computes the Bray-Curtis distance between two samples 
    (frequency maps).

    Parameters:
    - sample1 (dict): Sample or frequency map 1.
    - sample2 (dict): Sample or frequency map 2.

    Returns:
    - float: The Bray-Curtis distance betweeen these two smaples.
    """

    # Finds the sum of all values of the two frequency maps.
    total1 = sum_of_values(sample1)
    total2 = sum_of_values(sample2)

    # Finds the average between the two.
    av = average(float(total1), float(total2))

    # Calculates the sum of minima for these two frequency maps.
    sum_minima = sum_of_minima(sample1, sample2)

    # The BrayCurtis score is 1 - the ratio of the sum of minima to the average of the two
    # sum of values.
    return 1.0 - float(sum_minima) / av


def average(x: float, y: float) -> float:
    """
    Finds the average.

    Parameters:
    - x (float): One float variable.
    - y (float): A second float variable.

    Returns:
    - float: The average of x and y.
    """

    return (x + y) / 2.0

def sum_of_values(sample: dict) -> int:
    """
    sum_of_values finds the sum of all the integer values in the 
    key of the dictionary.

    Parameters:
    - sample1 (dict): The sample or frequency table.

    Returns:
    - int: The sum of the keys in the given sample1.
    """

    total = 0

    for _, val in sample.items():
        total += val

    return total

def sum_of_minima(sample1: dict, sample2: dict) -> int:
    """
    sum_of_minima returns the sum of the minima of the values for shared keys
    across two samples.

    Parameters:
    - sample1 (dict): A given input sample.
    - sample2 (dict): Another given input sample.

    Returns:
    - int: The sum of the minima of all values for shared keys. 
    """

    # Define an empty sum variable.
    sum_minima = 0
    # Range through the keys of one of the maps.
    for key, _ in sample1.items():
        # Is this key present in the other map?
        if key in sample2:  # yes
            # Add the minimum to the current sum
            sum_minima += min(sample1[key], sample2[key])

        # if no, take no action (or add zero)
    return sum_minima

def initialize_square_matrix(n: int) -> list[list[float]]:
    """Allocate an n x n matrix of floats initialized to 0.0."""
    mtx = []

    for i in range(n):
        new_row = [0.0] * n
        mtx.append(new_row)

    return mtx

def frequency_map(patterns: list[str]) -> dict[str, int]:
    """Construct a frequency map from a list of strings."""
    freq: dict[str, int] = {}

    for p in patterns:
        # if pattern already in map, increment count
        # else add pattern with count 1
        freq[p] = freq.get(p, 0) + 1

    return freq

def average(x: float, y: float) -> float:
    return (x + y) / 2.0

def sample_total(freq_map: dict[str, int]) -> int:
    """Sum of counts across all keys."""
    return sum(freq_map.values())

def sum_of_minima(map1: dict[str, int], map2: dict[str, int]) -> int:
    """Sum over keys of min(count1, count2)."""
    s = 0

    for key in map1.keys():
        if key in map2:
            s += min(map1[key], map2[key])

    return s

def min2(n1: int, n2: int) -> int:
    if n1 < n2:
        return n1
    return n2

def max2(n1: int, n2: int) -> int:
    if n1 > n2:
        return n1
    return n2
