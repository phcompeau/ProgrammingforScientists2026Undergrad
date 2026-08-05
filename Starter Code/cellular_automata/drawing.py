from datatypes import GameBoard
from functions import assert_rectangular, count_rows, count_columns
import pygame


def draw_game_board(current_board: GameBoard, cell_width: int) -> pygame.Surface:
    """
    Draw a single GameBoard to an image/surface (implementation up to you).
    
    Returns a pygame.Surface object representing the visualization of the board).
    """
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    assert_rectangular(current_board)
    if not isinstance(cell_width, int) or cell_width <= 0:
        raise ValueError("cell_width must be a positive integer.")

    # TODO: implement drawing logic
    return None

def draw_game_boards(boards: list[GameBoard], cell_width: int) -> list[pygame.Surface]:
    """
    Draw multiple GameBoards and return a list of images/surfaces.
    """
    if not isinstance(boards, list) or len(boards) == 0:
        raise ValueError("boards must be a non-empty list of GameBoard objects.")
    if not isinstance(cell_width, int) or cell_width <= 0:
        raise ValueError("cell_width must be a positive integer.")

    surfaces = []

    for board in boards: 
        surfaces.append(draw_game_board(board, cell_width))

    return surfaces