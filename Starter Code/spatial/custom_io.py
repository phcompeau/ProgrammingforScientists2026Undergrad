import os
from typing import List
from datatypes import Cell
from functions import assert_rectangular, count_rows, count_cols


def parse_header(first_line: str) -> tuple[int, int]:
    """
    Parse a header line of the form "<rows> <cols>" into two positive ints.

    Raises
    ------
    ValueError
        If the header is missing, not two tokens, or not positive integers.
    """
    if not isinstance(first_line, str):
        raise ValueError("header line must be a string")
    parts = first_line.strip().split()
    if len(parts) != 2:
        raise ValueError("header must contain exactly two integers: '<rows> <cols>'")
    try:
        rows = int(parts[0])
        cols = int(parts[1])
    except Exception:
        raise ValueError("header must contain integers: '<rows> <cols>'")
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive in header")
    return rows, cols


def read_board_from_file(filename: str) -> List[List[Cell]]:
    """
    Read a spatial-game board from a text file with header and C/D grid.

    Format
    ------
    First line:
        <rows> <cols>
    Then exactly <rows> lines each of length <cols>, consisting only of 'C' or 'D'.

    Parameters
    ----------
    filename : str
        Path to the file (e.g., f99.txt, f100.txt, rand200-*.txt, smallfield.txt).

    Returns
    -------
    List[List[Cell]]
        A rectangular 2D list of Cells with strategies 'C' or 'D'.

    Raises
    ------
    ValueError
        On invalid filename, malformed header, wrong number of data rows,
        wrong line lengths, or invalid characters.
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")
    if not os.path.isfile(filename):
        raise ValueError(f"file not found: {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        header_line = f.readline()
        if header_line is None or len(header_line) == 0:
            raise ValueError("missing header line ('<rows> <cols>')")
        rows, cols = parse_header(header_line)

        board: List[List[Cell]] = []
        i = 0
        while i < rows:
            line = f.readline()
            if line is None or len(line) == 0:
                raise ValueError(f"unexpected end of file: expected {rows} rows, got {i}")
            line = line.strip()
            if len(line) != cols:
                raise ValueError(f"row {i} has length {len(line)} but expected {cols}.")

            row: List[Cell] = []
            j = 0
            while j < cols:
                ch = line[j]
                if ch != "C" and ch != "D":
                    raise ValueError(
                        f"invalid character '{ch}' at row {i}, col {j}; expected 'C' or 'D'."
                    )
                row.append(Cell(ch, 0.0))
                j += 1

            board.append(row)
            i += 1

    assert_rectangular(board)
    return board


def write_board_to_file(board: List[List[Cell]], filename: str) -> None:
    """
    Write a board back to a text file in the same C/D format.

    Each row becomes a line; each Cell's .strategy ('C' or 'D') is written directly.

    Parameters
    ----------
    board : List[List[Cell]]
        2D list of Cells to write. Must be rectangular.
    filename : str
        Output file path. Parent directory must exist.

    Raises
    ------
    ValueError
        If inputs are invalid or board is not rectangular.
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")
    if not isinstance(board, list) or len(board) == 0 or not isinstance(board[0], list):
        raise ValueError("board must be a non-empty 2D list.")
    assert_rectangular(board)

    # Write rows (no list comprehensions)
    with open(filename, "w", encoding="utf-8") as f:
        i = 0
        rows = count_rows(board)
        while i < rows:
            j = 0
            cols = count_cols(board)
            line_chars: List[str] = []
            while j < cols:
                strat = board[i][j].strategy
                if strat != "C" and strat != "D":
                    raise ValueError(
                        f"invalid strategy '{strat}' at row {i}, col {j}; expected 'C' or 'D'."
                    )
                line_chars.append(strat)
                j += 1
            # Join manually without list comp:
            line = ""
            k = 0
            while k < len(line_chars):
                line += line_chars[k]
                k += 1
            f.write(line + "\n")
            i += 1