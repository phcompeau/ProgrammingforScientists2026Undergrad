import pygame
from datatypes import GameBoard
from functions import count_rows, count_cols


def draw_game_board(board: GameBoard, cell_width: int) -> pygame.Surface:
    """
    Draw a single GameBoard as a pygame.Surface.
    Args:
        board (GameBoard): A 2D list of booleans.
        cell_width (int): Pixel width of each cell.
    Returns:
        pygame.Surface: Surface with the board drawn.
    """
    if not isinstance(cell_width, int) or cell_width <= 0:
        raise ValueError("cell_width must be a positive integer.")
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    return pygame.Surface((1, 1))  # TODO: implement


def draw_game_boards(boards: list[GameBoard], cell_width: int) -> list[pygame.Surface]:
    """
    Draw multiple GameBoards.
    Args:
        boards (list[GameBoard]): List of GameBoard objects.
        cell_width (int): Pixel width of each cell.
    Returns:
        list[pygame.Surface]: Surfaces drawn for each board.
    """
    if not isinstance(boards, list) or len(boards) == 0:
        raise ValueError("boards must be a non-empty list.")
    return []  # TODO: implement
