def main():
    print("Dictionaries in Python (aka maps).")

    # polls = {} # empty dictionary

    # polls is going to be a dictionary whose keys are states and whose values are a polling percentage for a candidate in that state 
    polls: dict[str, float] = {}

    # we can set the value associated with any key
    polls["Pennsylvania"] = 0.517 
    polls["Ohio"] = 0.488
    polls["Texas"] = 0.378
    polls["Florida"] = 0.5

    print("Number of states in dictionary:", len(polls))

    polls["Vermont"] = 0.69

    print("Vermont poll:", polls["Vermont"])

    print("Number of states in dictionary:", len(polls))

    # bye Florida forever

    # is Florida in our polling data?
    if "Florida" in polls: # this is useful for checking if a key is a key of a given dictionary
        del polls["Florida"]

    print("Number of states in dictionary after Florida deletion:", len(polls))

    # list and dictionary literals 
    symbols = ["A", "C", "G", "T"]

    electoral_votes: dict[str, int] = {
        "Pennsylvania": 20,
        "Ohio": 18,
        "Texas": 38
    }

    update_votes(electoral_votes)

    # are dictionaries pass by value or reference????

    print("After function call, printing electoral votes.")
    print(electoral_votes)

    # let's print things more nicely 
    # when ranging over a list, we get the values of the list 
    # with dictionaries, we get the KEYS of the list
    for state_name in electoral_votes:
        print("The number of electoral votes in", state_name, "is", electoral_votes[state_name])

    # we also have double ranging for dictionaries 
    for state_name, votes in electoral_votes.items():
        print("The number of electoral votes in", state_name, "is", votes)

    # let's instead get these in alphabetical order. but how?

    # for a dictionary dict, Python gives us an operator dict.keys() that produces the dictionary's keys, which we can convert to a list
    state_names = list(electoral_votes.keys())
    print(state_names)

    # Python gives us a built in sorting algorithm that sorts a list into alphabetical order :) 
    state_names.sort()

    print(state_names)

    # now we can print the dictionary by ranging over the sorted keys and printing the associated values 

    for state in state_names:
        print("The number of electoral votes in", state, "is", electoral_votes[state])





def update_votes(votes: dict[str, int]) -> None:
    """
    Update votes according to 2024 values.
    """
    votes["Pennsylvania"] = 19
    votes["Ohio"] = 17
    votes["Texas"] = 40

    




if __name__ == "__main__":
    main()