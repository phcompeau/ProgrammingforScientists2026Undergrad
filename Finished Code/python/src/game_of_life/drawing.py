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
    
    # how wide and tall should the surface be?
    width = count_cols(board) * cell_width 
    height = count_rows(board) * cell_width

    # make the surface 
    surface = pygame.Surface((width, height))

    # draw on surface
    dark_gray = (60, 60, 60)
    white = (255, 255, 255)

    # set the background color to dark gray 
    surface.fill(dark_gray)

    # set the radius of the circles to draw 
    scaling_factor = 0.8
    radius = scaling_factor * (cell_width / 2)

    # fill in the colored squares 
    num_rows = count_rows(board)
    for row in range(num_rows): 
        num_cols = count_cols(board)
        for col in range(num_cols):
            # only draw cell if it's alive
            if board[row][col]:
                # draw cell as white. But where?
                # draw our rectangle 
                # x = col * cell_width
                # y = row * cell_width
                
                # pygame.draw.rect(surface, white, (int(x), int(y), cell_width, cell_width))

                # I will draw a circle instead
                # center should be in the center of the cell
                x = col * cell_width + cell_width/2
                y = row * cell_width + cell_width/2

                # radius will be a little less than cell_width/2 

                pygame.draw.circle(surface, white, (int(x), int(y)), int(radius))

    return surface


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
    
    if not isinstance(cell_width, int) or cell_width <= 0:
        raise ValueError("Issue with cell_width parameter.")

    surfaces = []

    for board in boards: 
        surfaces.append(draw_game_board(board, cell_width))

    return surfaces