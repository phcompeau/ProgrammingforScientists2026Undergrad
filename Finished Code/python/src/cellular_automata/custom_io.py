from datatypes import GameBoard

def read_board_from_file(filename: str) -> GameBoard:
    """
    Read a CSV of integers into a GameBoard (2D list[int]).
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")
    board: GameBoard = []
    with open(filename, "r", encoding="utf-8") as f:
        # strip trailing/leading whitespace, split into lines
        lines = f.read().strip().splitlines()
    for line in lines:
        elements = line.split(",")
        board.append(set_row_values(elements))
    return board

def set_row_values(line_elements: list[str]) -> list[int]:
    """
    Convert a list of numeric strings into a row of ints.
    """
    if not isinstance(line_elements, list) or len(line_elements) == 0:
        raise ValueError("line_elements must be a non-empty list of strings.")
    
    current_row = []

    # range over line elements and parse each one
    for element in line_elements:
        # we have a string, we need an integer 
        current_row.append(int(element))

    return current_row

def read_rules_from_file(filename: str) -> dict[str, int]:
    """
    Read rules from a text file where each line looks like: <neighborhood>:<next_state>

    Returns:
        dict[str, int]: mapping neighborhood-string -> next-state int
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")
    
    rules: dict[str, int] = dict()  # or {}

    # read in file and set the elements of the dictionary 
    with open(filename, "r") as file:
        giant_string = file.read()

    # parse giant_string one line at a time 
    trimmed_giant_string = giant_string.strip()

    lines = trimmed_giant_string.splitlines()
    # lines is a list of strings, one corresponding to each line of the file 

    # range over lines and parse each rule 
    for current_line in lines:
        # split line at the colon 
        parts = current_line.split(":")

        # how many parts are there? 2!
        if len(parts) != 2:
            raise ValueError("Someone added too many colons or not enough into our rule set.")
        
        # key is first element in parts 
        neighborhood_string = parts[0]

        # value is second element; need to convert to int
        new_state = int(parts[1])

        # add current rule to dictionary 
        rules[neighborhood_string] = new_state

    return rules