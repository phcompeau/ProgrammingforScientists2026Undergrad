import csv

def read_electoral_votes(filename: str) -> dict[str, int]:
    """
    Processes the number of electoral votes for each state.
    Parameters:
    - filename (str): A filename string.
    Returns:
    - dict[str, int]: A dictionary that associates each state name (string)
      to an integer corresponding to its number of Electoral College votes.
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("filename must be a non-empty string.")
    
    electoral_votes: dict[str, int] = {}

    # read in the file contents
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        lines = csv.reader(file)
        # range over lines, parse each line, and add values to our dictionary
        for line in lines:
            if not line:
                continue  # skip empty lines
            # line has two items: the state name and the number of electoral votes (as a string)
            state_name = line[0]
            # parse the number of electoral votes
            num_votes = int(line[1])
            # add to dictionary
            electoral_votes[state_name] = num_votes

    return electoral_votes


def read_polling_data(filename: str) -> dict[str, float]:
    """
    Parses polling percentages from a file.
    Parameters:
    - filename (str): A filename string.
    Returns:
    - dict[str, float]: A dictionary of state names (strings) to floats
      corresponding to the percentages for candidate 1.
    """

    if not filename or not isinstance(filename, str):
        raise ValueError("filename must be a non-empty string.")
    
    candidate_1_percentages: dict[str, float] = {}

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # range over each line of the file and parse in the data
        for line in reader:
            if not line:
                continue  # skip empty lines
            # line has three items (state name and two percentages)
            state_name = line[0]
            percentage_1 = float(line[1])
            # normalize percentage (divide by 100) and set the appropriate dictionary value
            candidate_1_percentages[state_name] = percentage_1 / 100.0
            
    return candidate_1_percentages
