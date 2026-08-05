def main():
    print("Substrings in Python.")

    s = "Hi Lovers"
    print(s[1:5])
    print(s[:7]) # if first index is omitted, it's zero
    print(s[4:]) # if final index is omitted, it's len(s)

    # the exact same notation applies to sublists (See online)

    pattern = "ATA"
    text = "ATATA"

    print("Our function:", pattern_count(pattern, text))

    print("Built in function:", text.count(pattern)) # built in function

    print("Starting positions:", starting_indices(pattern, text))

    print("Counting patterns again:", pattern_count_2(pattern, text))


# finding starting indices is a more general problem than counting # of occurrences of the pattern!

def starting_indices(pattern: str, text:str) -> list[int]:
    """
    Returns the list of all the starting positions of pattern in text.
    """
    n = len(text)
    k = len(pattern)

    if k == 0:
        raise ValueError("empty pattern not allowed.")
    
    if k > n:
        return []
    
    positions = [] 

    # range over all substrings, incrementing count every time we find a match 
    for i in range(n-k+1):
        # print("Current substring:", text[i:i+k])
        if pattern == text[i:i+k]:
            #match!
            positions.append(i)

    return positions

def pattern_count_2(pattern: str, text: str) -> int:
    """
    Finds the number of times the substring occurs in the larger text, including overlaps (e.g., AA occurs twice in AAA).

    Uses the fact that finding starting indices is a more general problem.
    """

    positions = starting_indices(pattern, text)
    return len(positions)


def pattern_count(pattern: str, text: str) -> int:
    """
    Finds the number of times the substring occurs in the larger text, including overlaps (e.g., AA occurs twice in AAA).
    """

    n = len(text)
    k = len(pattern)

    if k == 0:
        raise ValueError("empty pattern not allowed.")
    
    if k > n:
        return 0
    
    count = 0 

    # range over all substrings, incrementing count every time we find a match 
    for i in range(n-k+1):
        # print("Current substring:", text[i:i+k])
        if pattern == text[i:i+k]:
            #match!
            count += 1

    return count

"""
StartingIndices(pattern, text)
    positions ← array of integers of length 0
    n ← length(text)
    k ← length(pattern)
    for every integer i between 0 and n − k
        if text[i, i + k] = pattern
            positions ← append(positions, i)
    return positions
"""

"""
PatternCount(pattern, text)
    count ← 0
    n ← length(text)
    k ← length(pattern)
    for every integer i between 0 and n − k
        if text[i, i + k] = pattern
            count ← count + 1
    return count
"""

if __name__ == "__main__":
    main()




