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
    
    num_rows = count_rows(current_board)
    num_cols = count_columns(current_board)

    # declare surface 
    width = cell_width * num_cols
    height = cell_width * num_rows
    surface = pygame.Surface((width, height))

    # next, declare colors 
    dark_gray = (60, 60, 60)
    white = (255, 255, 255)  # 2^8 - 1
    red = (239, 71, 111)
    green = (6, 214, 160)
    yellow = (255, 255, 0)
    orange = (255, 165, 0)
    purple = (160, 32, 240)
    blue = (17, 138, 178)
    black = (0, 0, 0)

    # set fill color 
    surface.fill(dark_gray)

    # let's make a dictionary that maps ints (cell states) to colors
    color_map = {
        0: dark_gray,
        1: white, 
        2: red,
        3: green,
        4: yellow,
        5: orange,
        6: purple,
        7: blue,
        8: black,
    }

    scaling_factor = 0.8
    radius = scaling_factor * cell_width/2

    # range over the board and color in circles
    for i in range(num_rows):
        for j in range(num_cols):
            # what is the current cell's state?
            val = current_board[i][j]

            # what color should I color it? Only color it if it's not the background color
            if val != 0:
                # set the center 
                x = j * cell_width + cell_width // 2 
                y = i * cell_width + cell_width // 2

                # look up current color in the dictionary
                current_color = color_map[val]

                # draw the circle 
                pygame.draw.circle(surface, current_color, (x, y), int(radius))

    return surface

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