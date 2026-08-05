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