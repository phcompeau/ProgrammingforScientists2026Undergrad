import sys
import pygame # for drawing to a virtual canvas
import numpy # for converting drawings to arrays that can be rendered as frames of videos
import imageio # for rendering videos

# specific functions that we will need from elsewhere in the folder
from custom_io import read_board_from_file, read_rules_from_file
from functions import play_automaton 
from drawing import draw_game_boards

def main():
    print("Cellular automata!")

    # first, parse command line arguments to take num generations, which game to play, initial board, where to draw it, etc.

    neighborhood_type = sys.argv[1]
    rule_file = sys.argv[2]

    initial_board_file = sys.argv[3]
    output_file = sys.argv[4]

    cell_width = int(sys.argv[5])
    num_gens = int(sys.argv[6])

    print("Parameters read! Reading in board and rule set.")

    # read in initial board and rule set

    initial_board = read_board_from_file(initial_board_file)
    rules = read_rules_from_file(rule_file)

    print("Board and rules read from file.")

    # then, we want to run the simulation

    print("Running simulation.")
    boards = play_automaton(initial_board, num_gens, neighborhood_type, rules)

    print("Simulation is complete!")

    print("Drawing to canvases.")

    surfaces = draw_game_boards(boards, cell_width)

    print("Drawing done! Now, animating.")

    # we need a little bit more code to visualize the canvases that we have as an animation

    video_path = output_file + ".mp4" # gives it the appropriate file extension 

    # create a writer object to write to file 
    writer = imageio.get_writer(video_path, fps=10, codec="libx264", quality = 8)

    # range over surface objects and draw each one 
    for surface in surfaces:
        # writer needs to convert the surface to a numpy array
        frame = pygame_surface_to_numpy(surface)
        writer.append_data(frame)

    writer.close()

    print("Success! MP4 video produced.")

    print("Animation finished! Exiting normally.")

def pygame_surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """
    Convert a Pygame Surface to a NumPy RGB image array.

    Returns:
        numpy.ndarray: The frame as (height, width, 3) uint8 RGB.
    """

    # get a numpy array associated with the surface and swap its axes
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)

if __name__ == "__main__":
    main()