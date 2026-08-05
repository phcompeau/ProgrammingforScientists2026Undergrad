from datatypes import GameBoard

# blank functions to fill in:

def play_automaton(initial_board: GameBoard, num_gens: int,
                   neighborhood_type: str,
                   rules: dict[str, int]) -> list[GameBoard]:
    """
    Simulate an arbitrary cellular automaton for a given number of generations.

    Args:
        initial_board: Starting GameBoard (2D list of ints).
        num_gens: Number of generations to simulate (>= 0).
        neighborhood_type: "Moore" or "vonNeumann".
        rules: Mapping from neighborhood-string -> next-state integer.

    Returns:
        A list of GameBoards of length num_gens + 1.
    """
    if not isinstance(initial_board, list) or len(initial_board) == 0:
        raise ValueError("initial_board must be a non-empty GameBoard.")
    assert_rectangular(initial_board)
    if not isinstance(num_gens, int) or num_gens < 0:
        raise ValueError("num_gens must be a non-negative integer.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dict[str, int].")

    boards = []
    boards.append(initial_board)

    for i in range(num_gens):
        current_board = update_board(boards[i], neighborhood_type, rules)
        boards.append(current_board)

    return boards


def update_board(current_board: GameBoard,
                 neighborhood_type: str,
                 rules: dict[str, int]) -> GameBoard:
    """
    Update a GameBoard for one generation according to the given rules and neighborhood type.

    Args:
        current_board (GameBoard): The current state of the automaton.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, int]): A mapping from neighborhood strings to next-state integers.

    Returns:
        GameBoard: The new board after applying the automaton rules for one generation.
    """

    # parameter checks
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    if neighborhood_type not in ["Moore", "vonNeumann"]:
        raise ValueError("neighborhood_type must be 'Moore' or 'vonNeumann'.")
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dictionary.")

    # first, create a new board corresponding to the next generation 
    num_rows = count_rows(current_board)
    num_cols = count_columns(current_board)

    new_board = initialize_board(num_rows, num_cols)

    # iterate over all the cells and set their current values 
    for r in range(num_rows):
        for c in range(num_cols):
            new_board[r][c] = update_cell(current_board, r, c, neighborhood_type, rules)

    return new_board

def update_cell(board: GameBoard, r: int, c: int,
                neighborhood_type: str,
                rules: dict[str, int]) -> int:
    """
    Determine next-state integer for cell (r, c) using rules and neighborhood type.

    Args:
        board (GameBoard): Current state of the automaton.
        r (int): Row index of the cell to update.
        c (int): Column index of the cell to update.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, int]): A mapping from neighborhood strings to next-state integers.

    Returns:
        int: next state for the cell.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    assert_rectangular(board)
    if not isinstance(r, int) or not isinstance(c, int):
        raise ValueError("r and c must be integers.")
    if not in_field(board, r, c):
        raise ValueError("(r, c) must be inside the board.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dict[str, int].")

    # first thing that we want to do is convert the current cell's neighborhood to a string

    neighborhood = neighborhood_to_string(board, r, c, neighborhood_type)

    # does this neighborhood exist as a key within the rule set?
    if neighborhood in rules:
        # I found a rule! Find cell state 
        return rules[neighborhood]

    # if not, there's an issue 
    # one possibility: error!
    # another: keep it same 
    # third: kill it! Will be helpful on the boundary
    return 0 
    # fourth: return -1


def neighborhood_to_string(current_board: GameBoard, r: int, c: int,
                           neighborhood_type: str) -> str:
    """
    Construct the neighborhood string for a given cell in a GameBoard.

    Args:
        current_board (GameBoard): The current game board.
        r (int): The row index of the cell.
        c (int): The column index of the cell.
        neighborhood_type (str): The type of neighborhood ("Moore" or "vonNeumann").

    Returns:
        str: A string formed of the central square followed by its neighbors
        according to the neighborhood type indicated.
    """
    # parameter checks
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    assert_rectangular(current_board)
    if not isinstance(r, int) or not isinstance(c, int):
        raise ValueError("r and c must be integers.")
    if not in_field(current_board, r, c):
        raise ValueError("(r, c) must be inside the board.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')
    
    # we can go ahead and add the current cell as the starting point of our string 
    neighborhood = str(current_board[r][c])

    # we'll make a little list to store the cell values we are going to look at 
    offsets = [] # represents what we change (r,c) by to get an element we care about

    if neighborhood_type == "Moore":
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    elif neighborhood_type == "vonNeumann":
        offsets =  [(-1, 0), (0, 1), (1, 0), (0, -1)]
    else:
        raise ValueError("Invalid neighborhood type given.")
    
    # range over offsets, identify cells we need, and add them to the neighborhood if they're on the board 
    for x,y in offsets:
        # x is first thing, y is second thing in my current tuple
        # what is current cell I'm looking at? (r+x, c+y)
        # is it in the board?
        if in_field(current_board, r+x, c+y):
            neighborhood += str(current_board[r+x][c+y])
        else:
            #give it our default 0 state
            neighborhood += "0"
    
    return neighborhood

# Helper functions are below

def initialize_board(num_rows: int, num_cols: int) -> GameBoard:
    """
    Initialize a GameBoard with the given number of rows and columns.

    Args:
        num_rows (int): Number of rows.
        num_cols (int): Number of columns.

    Returns:
        GameBoard: A num_rows x num_cols board filled with False values.
    """

    if not isinstance(num_rows, int) or num_rows <= 0:
        raise ValueError("num_rows must be a positive integer.")

    if not isinstance(num_cols, int) or num_cols <= 0:
        raise ValueError("num_cols must be a positive integer.")

    board: GameBoard = [] # declaring board

    for _ in range(num_rows):
        row = [0] * num_cols
        board.append(row)

    return board

def count_rows(board: GameBoard) -> int:
    """
    Count the number of rows in a GameBoard.
    Args:
        board (GameBoard): A 2D list of ints representing the game state.
    Returns:
        int: Number of rows in the board.
    """

    if not isinstance(board, list):
        raise ValueError("board must be a list.")

    return len(board)


def count_columns(board: GameBoard) -> int:
    """
    Count the number of columns in a GameBoard.
    Args:
        board (GameBoard): A 2D list of ints representing the game state.
    Returns:
        int: Number of columns in the board.
    Raises:
        ValueError: If the board is not rectangular.
    """

    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")

    if len(board) == 0:
        raise ValueError("Error: no rows in GameBoard.")

    return len(board[0])

def assert_rectangular(board: GameBoard) -> None:
    """
    Check whether a GameBoard is rectangular.

    Args:
        board (GameBoard): The game board.

    Raises:
        ValueError: If the board has no rows or if its rows are not the same length.
    """
    if len(board) == 0:
        raise ValueError("Error: no rows in GameBoard.")

    first_row_length = len(board[0])
    
    # range over rows and make sure that they have the same length as first row
    for row in board:
        if len(row) != first_row_length:
            raise ValueError("Error: GameBoard is not rectangular.")

def in_field(board: GameBoard, i: int, j: int) -> bool:
    """
    Check if the indices (i, j) are within the bounds of the board.

    Args:
        board (GameBoard): The game board (2D list of ints).
        i (int): Row index.
        j (int): Column index.

    Returns:
        bool: True if (i, j) is inside the board, False otherwise.
    """

    # parameter checks
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if not isinstance(i, int) or not isinstance(j, int):
        raise ValueError("i and j must be integers.")

    if i < 0 or j < 0:
        return False

    if i >= count_rows(board) or j >= count_columns(board):
        return False

    # if we survive to here, then we are on the board
    return True
