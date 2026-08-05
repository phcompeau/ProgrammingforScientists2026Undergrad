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

    # TODO: Implement function
    pass


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

    # TODO: Implement function
    pass

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

    # TODO: Implement function
    pass

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

    # TODO: implement neighborhood string construction
    pass

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
