import pygame 
from datatypes import Board

# draw_boards takes a slice of Board objects as input along with a cell_width and n parameter.
# It returns a slice of images corresponding to drawing every nth board to a file,
# where each cell is cell_width x cell_width pixels.
def draw_boards(boards: list[Board], cell_width: int, n: int) -> list[pygame.Surface]:
    image_list = []

    # range over boards and if divisible by n, draw board and add to our list
    for i, board in enumerate(boards):
        if i % n == 0:
            image_list.append(draw_board(board, cell_width))

    return image_list


# draw_board takes a Board objects as input along with a cell_width parameter.
# It returns an image corresponding to drawing every nth board to a file,
# where each cell is cell_width x cell_width pixels.
def draw_board(b: Board, cell_width: int) -> pygame.Surface:
    # need to know how many pixels wide and tall to make our image
    height = len(b) * cell_width
    width = len(b[0]) * cell_width

    # think of a canvas as a PowerPoint slide that we draw on
    c = pygame.Surface((width, height))

    # canvas will start as black, so we should fill in colored squares
    c.fill((0, 0, 0))

    for i in range(len(b)):
        for j in range(len(b[i])):
            prey = b[i][j][0]
            predator = b[i][j][1]

            # we will color each cell according to a color map.

            if predator + prey > 0:
                val = predator / (predator + prey)
            else:
                val = 0.0

            # we create a red-blue color gradient 
            r = int(val * 255)
            g = 0
            b_col = int((1 - val) * 255)
            color = (r, g, b_col)

            # draw a rectangle in right place with this color
            x = i * cell_width
            y = j * cell_width
            rect = pygame.Rect(x, y, cell_width, cell_width)
            pygame.draw.rect(c, color, rect)

    # canvas has an image field that we should return
    return c
