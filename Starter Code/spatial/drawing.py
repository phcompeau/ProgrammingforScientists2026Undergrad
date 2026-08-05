# drawing.py
# Pygame drawing utilities for boards, without list comprehensions.
# - draw_game_board(board, cell_width) -> pygame.Surface
# - draw_game_boards(boards, cell_width) -> list[pygame.Surface]
# - save_video_from_surfaces(surfaces, filename, fps=12) -> str
# Circles have radius = 0.8 * (cell_width / 2) = 0.4 * cell_width.

import pygame
import numpy as np
import imageio

from functions import count_rows, count_cols, assert_rectangular
from datatypes import GameBoard  # noqa: F401 (kept for parity with your structure)

def save_video_from_surfaces(
    surfaces: list[pygame.Surface],
    video_path: str,
    fps: int,
    codec: str,
    quality: int,
) -> None:
    """
    Save a list of pygame.Surface frames to a video file.

    Args:
        surfaces: List of pygame.Surface objects representing frames.
        video_path: Path where the video will be written.
        fps: Frames per second for the output video.
        codec: Video codec (default "libx264", requires ffmpeg).
        quality: Quality level for encoding (higher = better quality, larger file).

    Returns:
        None
    """
    writer = imageio.get_writer(video_path, fps=fps, codec=codec, quality=quality)

    for surface in surfaces:
        frame = pygame.surfarray.array3d(surface).swapaxes(0, 1)  # (H, W, 3)
        writer.append_data(frame)

    writer.close()

def pygame_surface_to_numpy(surface):
    """
    Convert a pygame Surface to a NumPy RGB array of shape (H, W, 3).
    """
    if not isinstance(surface, pygame.Surface):
        raise TypeError("surface must be a pygame.Surface")
    # surfarray.array3d returns (W, H, 3); swap to (H, W, 3)
    arr = pygame.surfarray.array3d(surface)
    arr = arr.swapaxes(0, 1)
    return arr.copy()


def draw_game_board(board, cell_width):
    """
    Draw a single board as a pygame.Surface.

    Supports:
      - Game of Life: board[i][j] is bool (True -> white circle).
      - Spatial games: board[i][j].strategy in {"C","D"} (C -> blue, D -> red).

    Each cell is drawn as a circle centered in its cell box with:
        radius = 0.8 * (cell_width / 2) = 0.4 * cell_width
    """
    if not isinstance(cell_width, int) or cell_width <= 0:
        raise ValueError("cell_width must be a positive integer.")
    if not isinstance(board, list) or len(board) == 0 or not isinstance(board[0], list):
        raise ValueError("board must be a non-empty 2D list.")

    assert_rectangular(board)

    width = count_cols(board) * cell_width
    height = count_rows(board) * cell_width

    surface = pygame.Surface((width, height))

    # colors
    dark_gray = (60, 60, 60)
    white = (255, 255, 255)
    blue_c = (40, 170, 255)   # for "C"
    red_d = (240, 60, 80)     # for "D"

    surface.fill(dark_gray)

    scaling_factor = 0.8
    radius = int(scaling_factor * cell_width / 2)

    rows = len(board)
    cols = len(board[0])

    i = 0
    while i < rows:
        j = 0
        while j < cols:
            cell = board[i][j]
            cx = int(j * cell_width + cell_width / 2)
            cy = int(i * cell_width + cell_width / 2)

            if isinstance(cell, bool):
                if cell:
                    pygame.draw.circle(surface, white, (cx, cy), radius)
            else:
                strat = getattr(cell, "strategy", None)
                if strat == "C":
                    pygame.draw.circle(surface, blue_c, (cx, cy), radius)
                elif strat == "D":
                    pygame.draw.circle(surface, red_d, (cx, cy), radius)
            j += 1
        i += 1

    return surface


def draw_game_boards(boards, cell_width):
    """
    Draw multiple boards; returns a list of pygame.Surface objects.
    """
    if not isinstance(boards, list) or len(boards) == 0:
        raise ValueError("boards must be a non-empty list of boards.")
    if not isinstance(cell_width, int) or cell_width <= 0:
        raise ValueError("cell_width must be a positive integer.")

    if not pygame.get_init():
        pygame.init()

    result = []
    idx = 0
    while idx < len(boards):
        result.append(draw_game_board(boards[idx], cell_width))
        idx += 1
    return result
