def main():
    print("Finding clumps.")

# Pseudocode from the learning objectives (for reference)

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

    Notes:
    - Follow the pseudocode in FIND_CLUMPS_PSEUDOCODE.
    - Build a frequency table for each window using `frequency_table`.
    - Use `contains` to avoid duplicates (or see the faster variant below).
    """
    # TODO: Implement this function
    pass


def frequency_table(text: str, k: int) -> dict[str, int]:
    """
    Builds a frequency table (dictionary) of all k-mers of length k in `text`,
    including overlaps.

    Parameters:
    - text (str): The input string.
    - k (int): The k-mer length.

    Returns:
    - dict[str, int]: Mapping from k-mer to frequency.

    Precondition checks to consider:
    - k must be positive.
    - If k > len(text), return an empty dict.
    """
    # TODO: Implement this function
    pass

if __name__ == "__main__":
    main()