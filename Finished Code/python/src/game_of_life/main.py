import sys
import pygame
import numpy
import imageio
from custom_io import read_board_from_file
from functions import play_game_of_life
from drawing import draw_game_board, draw_game_boards


def pygame_surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """
    Convert a Pygame Surface to a NumPy RGB image array.
    Returns:
        numpy.ndarray: Frame as (height, width, 3) array.
    """
    return None  # TODO: implement


def main():
    print("Coding the Game of Life!")

    # initialize pygame 
    pygame.init()

    # read the board from file 
    r_pentomino = read_board_from_file("boards/rPentomino.csv")

    cell_width = 20

    surface = draw_game_board(r_pentomino, cell_width)

    print("We made the surface?")

    filename = "output/rPentomino.png"

    pygame.image.save(surface, filename)

    print("Image created.")

    # when we type command line arguments, a tuple of strings is created called sys.argv
    # length of tuple is 1 more than # of arguments because the first one is always the name of the program, e.g., "main.py"

    pygame.quit()

    if len(sys.argv) != 5:
        raise ValueError("Usage: python main.py initial_board.csv output_prefix cell_width num_gens")
    
    # sys.argv[0] is "main.py"

    input_csv = sys.argv[1] # file name of initial board
    output_prefix = sys.argv[2] # where do I draw my animation?
    cell_width = int(sys.argv[3]) # what is cell width in pixels?
    num_gens = int(sys.argv[4]) # how many generations to run?

    print("Parameters read in successfully!")
    
    print("Reading in the initial Game of Life board.")

    initial_board = read_board_from_file(input_csv)

    print("Board read successfully.")

    print("Playing Game of Life.")

    boards = play_game_of_life(initial_board, num_gens)

    print("Game of Life simulation is finished!")

    print("Drawing the Game boards to surfaces.")

    surfaces = draw_game_boards(boards, cell_width)

    print("Boards drawn to canvases.")

    # we need a little bit more code to visualize the canvases that we have as an animation

    video_path = output_prefix + ".mp4" # gives it the appropriate file extension 

    # create a writer object to write to file 
    writer = imageio.get_writer(video_path, fps=10, codec="libx264", quality = 8)

    # range over surface objects and draw each one 
    for surface in surfaces:
        # writer needs to convert the surface to a numpy array
        frame = pygame_surface_to_numpy(surface)
        writer.append_data(frame)

    writer.close()

    print("Success! MP4 video produced.")

    pygame.image.save(surfaces[len(surfaces)-1], "output/test.png")


def pygame_surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """
    Convert a Pygame surface to a NumPy RGB image array.
    """
    return pygame.surfarray.array3d(surface).swapaxes(0,1) 

if __name__ == "__main__":
    main()
