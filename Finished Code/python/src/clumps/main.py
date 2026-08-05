import requests

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

    patterns = find_clumps(genome, k, window_length, t)

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
    patterns = []
    n = len(text)

    # range over all windows (i.e., all substrings having length window_length in text)
    for i in range(n-window_length+1):
        if i % 10000 == 0:
            print(i)
        current_window = text[i:i+window_length]
        freq_map = frequency_table(current_window, k)

        # find any k-mers in table that occur at least t times 
        for s, occurrences in freq_map.items():
            # does it occur at least t times? AND have we not seen it before
            if occurrences >= t and (s not in patterns):
                # append pattern to list
                patterns.append(s)

    return patterns

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
        return []
    
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