def find_frequent_words(text: str, k: int) -> list[str]:
    """
    Returns a list containing the most frequent k-mers occurring in text, 
    including overlaps.
    
    Parameters:
    - text (str): The input string.
    - k (int): The size of the k-mers.
    
    Returns:
    - list[str]: The most frequent k-mers in text.
    """
    # TODO: Implement this function
    pass


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
    # TODO: Implement this function
    pass


def max_map_value(dictionary: dict[str, int]) -> int:
    """
    Finds the maximum value in a dictionary with string keys and integer values.
    
    Parameters:
    - dictionary (dict[str, int]): The dictionary to evaluate.
    
    Returns:
    - int: The maximum value in the dictionary.
    
    Raises:
    - ValueError: If the dictionary is empty.
    """
    # TODO: Implement this function
    pass


def main():
    """
    Main entry point for testing frequent words finder.
    """
    print("Finding frequent words in Python!")
    
    # Small example test case
    text = "ACGTTTTGAGACGTTTACGC"
    k = 3
    print(find_frequent_words(text, k))
    
    # Uncomment this block to experiment with the Vibrio cholerae ori region
    """
    text = ("ATCAATGATCAACGTAAGCTTCTAAGCATGATCAAGGTGCTCACACAGTTTATCCACAACCTGAGTGG"
            "ATGACATCAAGATAGGTCGTTGTATCTCCTTCCTCTCGTACTCTCATGACCACGGAAAGATGATCAA"
            "GAGAGGATGATTTCTTGGCCATATCGCAATGAATACTTGTGACTTGTGCTTCCAATTGACATCTTCA"
            "GCGCCATATTGCGCTGGCCAAGGTGACGGAGCGGGATTACGAAAGCATGATCATGGCTGTTGTTCTG"
            "TTTATCTTGTTTTGACTGAGACTTGTTAGGATAGACGGTTTTTCATCACTGACTAGCCAAAGCCTTA"
            "CTCTGCCTGACATCGACCGTAAATTGATAATGAATTTACATGCTTCCGCGACGATTTACCTCTTGAT"
            "CATCGATCCGATTGAAGATCTTCAATTGTTAATTCTCTTGCCTCGACTCATAGCCATGATGAGCTCT"
            "TGATCATGTTTCCTTAACCCTCTATTTTTTACGGAAGAATGATCAAGCTGCTGCTCTTGATCATCGT"
            "TTC")
    for k in range(3, 10):
        print(k, find_frequent_words(text, k))
    """


if __name__ == "__main__":
    main()


"""
Pseudocode
"""

"""
FrequencyTable(text, k)
    freqMap ← empty map
    n ← length(text)
    for every integer i between 0 and n − k
        pattern ← text[i, i + k]
        if freqMap[pattern] doesn't exist
            freqMap[pattern] = 1
        else
            freqMap[pattern]++
    return freqMap
"""

"""
BetterFrequentWords(text, k)
    frequentPatterns ← an array of strings of length 0
    freqMap ← FrequencyTable(text, k)
    max ← MaxMapValue(freqMap)
    for all strings pattern in freqMap
        if freqMap[pattern] = max
            frequentPatterns ← append(frequentPatterns, pattern)
    return frequentPatterns
"""

"""
MaxMapValue(dict)
    m ← 0
    firstTime = true
    for every key pattern in dict
        if firstTime = true or dict[pattern] > m
            firstTime= false
            m ← dict[pattern]
    return m
"""