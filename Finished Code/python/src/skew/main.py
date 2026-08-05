from matplotlib import pyplot

import requests

def main():
    print("Building a skew array.")

    # --- Tiny local demo (uncomment after implementing functions) ---
    demo_genome = "CATGGGCATCGGCCATACGCC"
    arr = skew_array(demo_genome)
    print("Demo skew array length:", len(arr))
    print("First few values:", arr[:10])
    print("Minimum skew indices (demo):", minimum_skew(demo_genome))

    # --- E. coli genome experiment & plotting (uncomment to run) ---
    url = "https://bioinformaticsalgorithms.com/data/realdatasets/Replication/E_coli.txt"

    response = requests.get(url)
    response.raise_for_status()

    genome = response.text

    print("The number of nucleotides in E. coli genome is " + str(len(genome)))

    ecoli_skew_array = skew_array(genome)
    min_skew_positions = minimum_skew(genome)
    if len(min_skew_positions) == 0:
        raise RuntimeError("No minimum positions found (unexpected).")

    first_pos = min_skew_positions[0]
    print(
        "The minimum skew value of "
        + str(ecoli_skew_array[first_pos])
        + " occurs at positions "
        + str(min_skew_positions)
    )

    # Plot (requires matplotlib)
    
    draw_skew(ecoli_skew_array)
    print("Skew diagram drawn! Exiting normally.")



"""
Skew(symbol)
    if symbol = 'G'
        return 1
    else if symbol = 'C'
        return -1
    return 0
"""

"""
SkewArray(genome)
    n ← length(genome)
    array ← array of length n + 1
    array[0] ← 0
    for every integer i between 1 and n
        array[i] = array[i-1] + Skew(genome[i-1])
    return array
"""

def skew_array(genome: str) -> list[int]:
    """
    Returns the skew array for `genome`, where skew[i] is the difference
    (# of 'G') - (# of 'C') in genome[0:i].

    Parameters:
    - genome (str): DNA string.

    Returns:
    - list[int]: Skew array of length len(genome) + 1.

    Raises:
    - ValueError: If genome is empty.
    """

    if len(genome) == 0:
        raise ValueError("Zero length genome given.")
    
    n = len(genome)

    # define a skew array 
    skew_array = [0] * (n+1)

    # range over genome, and set skew_array[i-1] using previous value 
    for i in range(1, n+1):
        skew_array[i] = skew_array[i-1] + skew(genome[i-1])

    return skew_array


def skew(symbol: str) -> int:
    """
    Returns 1 if symbol is 'G'/'g', -1 if 'C'/'c', else 0.

    Parameters:
    - symbol (str): Single-character string.

    Returns:
    - int: Skew contribution for this symbol.

    Raises:
    - ValueError: If `symbol` is not length 1.
    """

    if len(symbol) != 1:
        raise ValueError("String given must be single character.")
    
    # return 1 if G or g 
    if symbol == "G" or symbol == "g":
        return 1
    elif symbol == "C" or symbol == "c":
        return -1
    else:
        return 0 # we could do better

"""
MinimumSkew(genome)
    indices ← array of integers of length 0
    n ← length(genome)
    array ← SkewArray(genome)
    m ← MinIntegerArray(array)
    for every integer i between 0 and n
        if array[i] = m
            indices = append(indices, i)
    return indices
"""

def minimum_skew(genome: str) -> list[int]:
    """
    Returns all indices i (0..len(genome)) where the skew array achieves
    its minimum value.

    Parameters:
    - genome (str): DNA string.

    Returns:
    - list[int]: Indices where skew is minimal.

    Raises:
    - ValueError: If genome is empty.
    """
    
    if len(genome) == 0:
        raise ValueError("Empty genome given.")
    
    # create list of indices 
    indices = []

    skew_arr = skew_array(genome)

    # find minimum value 
    min_val = min_integer_array(skew_arr)

    # range over the skew array, and find all indices where val = m
    n = len(skew_arr)
    for i in range(n):
        if skew_arr[i] == min_val:
            indices.append(i)

    return indices


def min_integer_array(a:list[int]) -> int:
    """"
    Returning the minimum value in a list of integers.
    """

    if len(a) == 0:
        raise ValueError("Error: empty list given.") 

    m = 0

    # iterate over list, updating m if we find a smaller value

    for i, val in enumerate(a):
        # ranges over the values in a list
        # if we find a smaller value than the current min 
        # OR we are at the first element, update m
        if val < m or i == 0:
            m = val

    return m


def draw_skew(skew_list: list[int]) -> None:
    """
    draw_skew draws a skew diagram using a skew_array output.
    
    """
    if len(skew_list) == 0:
        raise ValueError("skew_list is empty")
    pyplot.plot(skew_list)
    pyplot.title("Skew Diagram")
    pyplot.xlabel("Genome Position")
    pyplot.ylabel("Skew Value")
    pyplot.savefig("skewDiagram.png")

if __name__ == "__main__":
    main()