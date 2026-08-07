import requests
import time

def main():
    print("Finding clumps.")

    text = "AAAACGTCGAAAA"
    k = 3
    window_length = 4
    t = 2

    # should print "AAA"
    print(find_clumps(text, k, window_length, t))

    url = "https://bioinformaticsalgorithms.com/data/realdatasets/Replication/E_coli.txt"

    response = requests.get(url)

    response.raise_for_status() # give us an error if there was a problem

    genome = response.text

    print("Genome has length", len(genome), "nucleotides.")

    # call the clump finding algorithm!
    k = 9
    window_length = 500
    t = 3

    # code for timing the two approaches on a small piece of the genome
    start = time.time()
    find_clumps(genome[:10000], k, window_length, t)
    elapsed1 = time.time() - start
    print(f"find_clumps {elapsed1:.6f} seconds")

    start = time.time()
    find_clumps_faster(genome[:10000], k, window_length, t)
    elapsed2 = time.time() - start
    print(f"find_clumps_faster {elapsed2:.6f} seconds")

    print(f"Speedup: {elapsed1/elapsed2:.2f}x faster")

    # the faster version is quick enough to run on the full genome
    patterns = find_clumps_faster(genome, k, window_length, t)

    print("Success!")

    print("We found", len(patterns), "total patterns that form clumps.")


"""
FindClumps(text, k, L, t)
    patterns ← an array of strings of length 0
    n ← length(text)
    for every integer i between 0 and n − L
        window ← text[i, i + L]
        freqMap ← FrequencyTable(window, k)
        for every key s in freqMap
            if freqMap[s] ≥ t and Contains(patterns, s) = false
                patterns ← append(patterns, s)
    return patterns
"""

def find_clumps(text: str, k: int, window_length: int, t: int) -> list[str]:
    """
    Finds a list of strings representing all k-mers that appear at least t times
    in a window of given length in the string.

    Parameters:
    - text (str): The input string.
    - k (int): The k-mer length.
    - window_length (int): Length L of the sliding window.
    - t (int): Frequency threshold within a window.

    Returns:
    - list[str]: All distinct k-mers forming (L, t)-clumps in text.
    """
    # what do we need to check in terms of errors?
    if k <= 0 or window_length <= 0 or t <= 0:
        raise ValueError("Error: non-positive parameter given.")

    if len(text) == 0:
        raise ValueError("Error: empty string given.")

    if k > window_length:
        raise ValueError("Error: k bigger than window length.")

    if k > len(text):
        return []

    patterns = []
    n = len(text)

    # range over all windows (i.e., all substrings having length window_length in text)
    for i in range(n-window_length+1):
        current_window = text[i:i+window_length]
        freq_map = frequency_table(current_window, k)

        # find any k-mers in table that occur at least t times 
        for s, occurrences in freq_map.items():
            # does it occur at least t times? AND have we not seen it before
            if occurrences >= t and (s not in patterns):
                # append pattern to list
                patterns.append(s)

    return patterns


def find_clumps_faster(text: str, k: int, window_length: int, t: int) -> list[str]:
    """
    Finds all substrings of a given length in a longer string that occur more than some threshold number of times within a short region.

    Instead of rebuilding the frequency table for every window, this version
    updates the previous window's table: one k-mer "falls off" the front and
    one new k-mer enters at the back.

    Parameters:
    - text (str): The input string.
    - k (int): The k-mer length.
    - window_length (int): Length L of the sliding window.
    - t (int): Frequency threshold within a window.

    Returns:
    - list[str]: All distinct k-mers forming (L, t)-clumps in text.
    """
    # what do we need to check in terms of errors?
    if k <= 0 or window_length <= 0 or t <= 0:
        raise ValueError("Error: non-positive parameter given.")

    if len(text) == 0:
        raise ValueError("Error: empty string given.")

    if k > window_length:
        raise ValueError("Error: k bigger than window length.")

    if k > len(text):
        return []

    # sets in Python are unordered and don't allow duplicates
    patterns: set[str] = set()   # empty set
    n = len(text)

    # compute the frequency table for the first window
    first_window = text[:window_length]
    freq_map = frequency_table(first_window, k)

    # anything frequent?
    for s, val in freq_map.items():
        if val >= t:
            patterns.add(s)

    # we need to range over all remaining windows (having window_length) of text.
    for i in range(1, n-window_length+1):
        # what is the k-mer that "fell off"?
        old_pattern = text[i-1:i-1+k]

        # what is the new pattern?
        new_pattern = text[i+window_length-k:i+window_length]

        # let's update the frequency map
        # subtract 1 from the value of old_pattern
        freq_map[old_pattern] -= 1

        if freq_map[old_pattern] == 0:
            del freq_map[old_pattern]

        # add 1 to the value of new_pattern (or create its value equal to 1)
        freq_map[new_pattern] = freq_map.get(new_pattern, 0) + 1

        # now the frequency map is updated, great!

        # what is frequent that we haven't seen?

        # two possibilities:
        # (1) it was already frequent in previous map
        # (2) new_pattern all of a sudden is frequent

        # we don't need to check 1, but we do need to check 2
        if freq_map[new_pattern] >= t:
            patterns.add(new_pattern)

    return sorted(patterns)

# Example of the sliding window update
# text = "BANANASPLIT"
# window length = 6
# k = 3

# first frequency table
# BAN   1
# ANA   2
# NAN   1

# second frequency table
# ANA   2
# NAN   1
# NAS   1

def frequency_table(text: str, k: int) -> dict[str, int]:
    """
    Builds a frequency table of all k-mers of length k in the given text, 
    including overlaps.
    
    Parameters:
    - text (str): The input string.
    - k (int): The size of the k-mers.
    
    Returns:
    - dict[str, int]: A dictionary mapping each k-mer to its frequency.
    """
    if k <= 0:
        raise ValueError("k is not positive.")
    if k > len(text):
        return {}

    # declare a blank map
    freq_map: dict[str, int] = {}

    n = len(text)

    # range over all k-mer substrings of text
    for i in range(n-k+1):
        # grab current pattern of length k
        pattern = text[i:i+k]

        # does pattern exist in freq_map??
        # if not, then we create it as an entry 

        """
        CLASSIC WAY
        if pattern not in freq_map:
            freq_map[pattern] = 1
        else:
            # we have seen it!
            freq_map[pattern] += 1
        """

        # shortcut approach using get() 
        # get() takes two parameters: the key to retrieve, and a default value to assign it if it doesn't exist as a key
        freq_map[pattern] = freq_map.get(pattern, 0) + 1


    return freq_map

if __name__ == "__main__":
    main()