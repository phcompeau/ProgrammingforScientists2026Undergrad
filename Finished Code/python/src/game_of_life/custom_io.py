from datatypes import GameBoard

from functions import assert_rectangular


def read_board_from_file(filename: str) -> GameBoard:
    """
    Reads a CSV file representing a Game of Life board.
    "1" = alive (True), "0" = dead (False).
    Args:
        filename (str): The name of the CSV file.
    Returns:
        GameBoard: Parsed board.
    """
    if (not isinstance(filename, str)) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")
    
    # open(filename, 'r') as f: opens the file with name filename in read mode ('r') and returns a file object called f

    giant_string = "" #I'm comfortable with this because in many languages, giant_string would only exist in the block below

    with open(filename, 'r') as f:
        # adding with means that as soon as this block finishes, the file is closed 

        giant_string = f.read()  # read the file and return a giant string of file contents

        # f is done, so this is all we do

    # now I can work with the contents of f in giant_string

    # first, trim any whitespace at start or end of file
    trimmed_giant_string = giant_string.strip()

    # split the string into multiple strings, one for each line
    lines = trimmed_giant_string.splitlines()

    num_rows = len(lines) 

    # how do I make a GameBoard?
    board: GameBoard = []

    # now we read through the lines, and parse each line to add to our board 

    for current_line in lines:
        # split the current line every time we see a comma 
        line_elements = current_line.split(',')

        # line_elements is a list of strings, one string for each element in the current line (commas not included)

        # set the row values with a subroutine 
        new_row = set_row_values(line_elements)

        # new_row is a 1D list of booleans that we can append to board 
        board.append(new_row)

    assert_rectangular(board)

    return board


def set_row_values(line_elements: list[str]) -> list[bool]:
    """
    Convert a list of "0"/"1" strings into booleans.
    Args:
        line_elements (list[str]): Strings "0"/"1".
    Returns:
        list[bool]: Row with True/False.
    """
    if not isinstance(line_elements, list) or len(line_elements) == 0:
        raise ValueError("line_elements must be a non-empty list.")
    
    # make our row 
    current_row = [] # this will be a blank list of booleans
    
    for val in line_elements:
        if val == "0":  # dead
            current_row.append(False)
        elif val == "1":  # alive
            current_row.append(True)
        else:
            raise ValueError("Error: invalid entry in board file.")

    return current_row
