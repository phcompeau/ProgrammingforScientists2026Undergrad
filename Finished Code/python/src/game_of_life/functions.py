"""
Pseudocode

PlayGameOfLife(initialBoard, numGens)
    boards ← array of numGens + 1 game boards
    boards[0] ← initialBoard
    for every integer i from 1 to numGens
        boards[i] ← UpdateBoard(boards[i–1])
    return boards

UpdateBoard(currentBoard)
    numRows ← CountRows(currentBoard)
    numCols ← CountCols(currentBoard)
    newBoard ← InitializeBoard(numRows, numCols)
    for every integer r between 0 and numRows – 1
        for every integer c between 0 and numCols – 1
            newBoard[r][c] ← UpdateCell(currentBoard, r, c)
    return newBoard

UpdateCell(currentBoard, r, c)
    numNeighbors ← CountLiveNeighbors(currentBoard, r, c)
    if currentBoard[r][c] = true (current cell is alive)
        if numNeighbors = 2 or numNeighbors = 3 (propagation)
            return true
        else (no mates/overpopulation)
            return false
    else (current cell is dead)
        if numNeighbors = 3 (zombie!)
            return true
        else (rest in peace)
            return false

CountLiveNeighbors(currentBoard, r, c)
    count ← 0
    for every integer i between r – 1 and r + 1
        for every integer j between c – 1 and c + 1
            if (i≠r or j≠c) and InField(currentBoard, i, j) = true
                if currentBoard[i][j] = true
                    count ← count + 1
    return count

    
"""

from datatypes import GameBoard


def count_rows(board: GameBoard) -> int:
    """
    Count the number of rows in a GameBoard.
    Args:
        board (GameBoard): A 2D list of booleans representing the game state.
    Returns:
        int: Number of rows in the board.
    """
    if not isinstance(board, list):
        raise ValueError("board must be a list.")
    
    return len(board)


def count_cols(board: GameBoard) -> int:
    """
    Count the number of columns in a GameBoard.
    Args:
        board (GameBoard): A 2D list of booleans representing the game state.
    Returns:
        int: Number of columns in the board.
    Raises:
        ValueError: If the board is not rectangular.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    
    assert_rectangular(board)
    
    return len(board[0])  # only works if board is rectangular


def assert_rectangular(board: GameBoard) -> None:
    """
    Ensure that a GameBoard is rectangular.
    Args:
        board (GameBoard): A 2D list of booleans representing the game state.
    Raises:
        ValueError: If the board has no rows or if its rows are not of equal length.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    
    # how can I check if the board is not rectangular?
    # if I find that it's non rectangular, I want to raise a value error. Otherwise I take no action.

    first_row_length = len(board[0])

    # range over remaining rows, and flip out if any has length not equal to first_row_length 
    for row in range(1, count_rows(board)):
        if len(board[row]) != first_row_length:
            raise ValueError("Board is not rectangular at row index " + row)


def play_game_of_life(initial_board: GameBoard, num_gens: int) -> list[GameBoard]:
    """
    Simulate Game of Life for a given number of generations.
    Args:
        initial_board (GameBoard): The starting game board.
        num_gens (int): The number of generations to simulate.
    Returns:
        list[GameBoard]: Boards from initial through num_gens generations.
    """
    if not isinstance(initial_board, list) or len(initial_board) == 0:
        raise ValueError("initial_board must be a non-empty GameBoard.")
    if not isinstance(num_gens, int) or num_gens < 0:
        raise ValueError("num_gens must be a non-negative integer.")
    
    boards = []
    boards.append(initial_board)
    # one-liner: boards = [initial_board]

    # range over number of generations and call update_board 
    for i in range(num_gens): 
        prev_board = boards[i]
        next_board = update_board(prev_board)
        boards.append(next_board)

    return boards

def update_board(current_board: GameBoard) -> GameBoard:
    """
    Apply Game of Life rules for one generation.
    Args:
        current_board (GameBoard): The current game board.
    Returns:
        GameBoard: A new board representing the next generation.
    """
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    
    assert_rectangular(current_board)

    num_rows = count_rows(current_board)
    num_cols = count_cols(current_board)

    if num_cols == 0:
        raise ValueError("Error: board should have at least one column.")
    
    # no funny business if we make it here 

    new_board = initialize_board(num_rows, num_cols) 

    # all cells are dead at this point 

    # range over all cells of old board and update the cell of the new board
    for r in range(num_rows):
        for c in range(num_cols):
            new_board[r][c] = update_cell(current_board, r, c)

    return new_board


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
    
    # let's declare a blank GameBoard 
    board: GameBoard = []

    # range over the rows and make the rows 
    for _ in range(num_rows):
        row = [False] * num_cols
        board.append(row)

    return board


def update_cell(board: GameBoard, r: int, c: int) -> bool:
    """
    Determine the next state of the cell at (r, c).
    Args:
        board (GameBoard): The current game board.
        r (int): Row index.
        c (int): Column index.
    Returns:
        bool: True if alive next generation, False otherwise.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if not isinstance(r, int) or not isinstance(c, int):
        raise ValueError("r and c must be integers.")
    
    num_live_neighbors = count_live_neighbors(board, r, c)

    # apply the Game of Life rules 
    # is current cell alive or dead?
    if board[r][c]: # alive
        if num_live_neighbors == 2 or num_live_neighbors == 3:
            #stayin alive 
            return True
        else: #die
            return False
    else: # dead
        if num_live_neighbors == 3:
            #zombie
            return True
        else:
            #RIP
            return False


def count_live_neighbors(board: GameBoard, r: int, c: int) -> int:
    """
    Count live neighbors of board[r][c].
    Args:
        board (GameBoard): The current game board.
        r (int): Row index.
        c (int): Column index.
    Returns:
        int: Number of live neighbors.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    
    assert_rectangular(board)

    if count_cols(board) == 0:
        raise ValueError("Board must have at least one column.")
    
    count = 0

    # range over just the Moore neighborhood 
    # easiest way: range over 9 cells
    # row ranges from r-1 to r+1, col ranges from c-1 to c+1
    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            # 3 things should be true
            # 1. board[i][j] is in nbd and isn't (r,c)
            # 2. (i, j) is in the boundaries of board 
            # 3. board[i][j] is True
            # the order of these checks is critical due to "short circuiting": break an and as soon as we hit a false statement
            if ((i != r) or (j != c)) and in_field(board, i, j) and board[i][j]:
                count += 1

    return count


def in_field(board: GameBoard, i: int, j: int) -> bool:
    """
    Check if the given (i, j) indices are within the board.
    Args:
        board (GameBoard): The current game board.
        i (int): Row index.
        j (int): Column index.
    Returns:
        bool: True if inside the board, False otherwise.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if not isinstance(i, int) or not isinstance(j, int):
        raise ValueError("i and j must be integers.")
    
    num_rows = count_rows(board)
    num_cols = count_cols(board)
    
    if i >= 0 and j >= 0 and i < num_rows and j < num_cols:
        return True 
    
    # if we make it here, we are off the board 
    return False

    """
    # alternatively check if something is off the board and return True if not
    if i < 0 or j < 0 or i >= num_rows or j >= num_cols:
        return False
    
    return True
    """
