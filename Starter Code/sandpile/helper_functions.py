"""Helper functions for sandpile module."""

from datatypes import Board

def contains(b: Board, r: int, c: int) -> bool:
    """Return True if (r, c) lies within the board bounds.

    Args:
        b: Board to check.
        r: Row index.
        c: Column index.

    Returns:
        True if indices are in range; otherwise False.
    """
    if r < 0 or c < 0 or r >= num_rows(b) or c >= num_cols(b):
        return False
    else:
        return True

def deep_copy_board(b: Board) -> Board:
    """Return a deep copy of the board.

    Args:
        b: Board to copy.

    Returns:
        Deep-copied board.
    """
    new_board: Board = []
    for row in b:
        new_row = []
        for value in row:
            new_row.append(value)
        new_board.append(new_row)
    return new_board

def assert_rectangular(b: Board) -> None:
    """Raise an error if the board is not rectangular.

    Args:
        b: Board to check.

    Raises:
        ValueError: If any row has a different length from the first row.
    """
    if not b:   # empty board is rectangular by definition
        return

    first_len = len(b[0])
    for row in b:
        if len(row) != first_len:
            raise ValueError("Error: board is not rectangular.")


def num_rows(b: Board) -> int:
    """Return the number of rows in the board.

    Args:
        b: Board to query.

    Returns:
        Row count.
    """
    assert_rectangular(b)
    return len(b)


def num_cols(b: Board) -> int:
    """Return the number of columns in the board.

    Args:
        b: Board to query.

    Returns:
        Column count.
    """
    assert_rectangular(b)
    if not b:
        return 0
    return len(b[0])

def make_empty_board(r: int, c: int) -> Board:
    """Return an r x c board full of zeros (no comprehensions)."""
    b: Board = []
    for _ in range(r):
        row = []
        for _ in range(c):
            row.append(0)
        b.append(row)
    return b