def main():
    print("Dictionaries in Python.")

    # polls = {}   # standard dictionary declaration

    # polls is going to be a dictionary whose keys are states and whose values are a polling percentage for a candidate in that state
    polls: dict[str, float] = {}

    # let's add some elements
    polls["Pennsylvania"] = 0.517
    polls["Ohio"] = 0.488
    polls["Texas"] = 0.378
    polls["Florida"] = 0.5

    print("Number of elements in my dictionary is", len(polls))

    # primes = {}
    # primes[0] = 2
    # primes[1] = 3
    # primes[2] = 5
    # etc.
    # This is really bad.

    polls["Vermont"] = 0.69

    print(polls["Vermont"])

    print("Number of elements in my dictionary is", len(polls))

    # let's get rid of Florida, if it's in the dictionary
    if "Florida" in polls:  # this is useful for checking if a key is a key of a given dictionary
        del polls["Florida"]

    print(polls)

    # we can create a small list with a list literal
    # primes = [2, 3, 5, 7, 11]

    # dictionaries have literals too
    electoral_votes: dict[str, int] = {
        "Pennsylvania": 20,
        "Ohio": 18,
        "Texas": 38
    }

    update_votes_2024(electoral_votes)

    print("As of 2024, the number of votes in Pennsylvania is", electoral_votes["Pennsylvania"])

    # Dictionaries are pass by reference

    # ranging over dictionaries
    # when we range, the order is based on the order in which elements were added to the dictionary

    # when ranging over a list, we get the values of the list
    # with dictionaries, we get the KEYS
    for state_name in electoral_votes:
        print("Number of votes in", state_name, "is", electoral_votes[state_name])

    # we also have double ranging for dictionaries
    for key, num_votes in electoral_votes.items():
        print("Number of votes in", key, "is", num_votes)

    # let's instead get these in alphabetical order. but how?

    # for a dictionary, Python gives us dict.keys(), which produces the dictionary's keys; we can convert this to a list
    keys = list(electoral_votes.keys())
    print(keys)

    # sort the keys (Python gives us a built in sorting algorithm)
    keys.sort()
    print(keys)

    # range over the states
    for state_name in keys:
        # I'm ranging over a list, but that list is the collection of state names
        print("Num of electoral votes in", state_name, "is", electoral_votes[state_name])

    # there's a faster approach
    # for state_name in sorted(electoral_votes):
        # print("Num of electoral votes in", state_name, "is", electoral_votes[state_name])

    # we also can get just the values of a dictionary with dict.values()

    total_votes = 0

    for num_votes in list(electoral_votes.values()):
        total_votes += num_votes

    print("Total votes:", total_votes)

def update_votes_2024(votes: dict[str, int]) -> None:
    """
    Updates electoral college votes from 2020 to 2024.

    Parameters:
    - votes: dict[str, int] representing a map of states to votes

    Returns:
    (None): updates the dictionary "in place"
    """
    votes["Pennsylvania"] = 19
    votes["Ohio"] = 17
    votes["Texas"] = 40



def complement(dna:str) -> str:
    """
    Finds the complementary strand of a given DNA string, this time using a dictionary.
    """
    dna2 = ""

    # before, we could use if/elif statements, or a match statement (switch)
    comp_dict: dict[str, str] = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    # now, range over the string, and set the appropriate value of dna2
    for symbol in dna:
        dna2 += comp_dict[symbol]

    return dna2

if __name__ == "__main__":
    main()
