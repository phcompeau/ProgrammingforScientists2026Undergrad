import sys
import pygame
import imageio

from custom_io import read_board_from_file
from functions import evolve
from drawing import draw_game_boards, save_video_from_surfaces

USAGE = """Usage:
    python main.py <filename> <b> <steps> <cell_width>

Example:
    python main.py /mnt/data/f99.txt 1.9 60 6
"""

def parse_args(argv: list[str]) -> tuple[str, float, int, int]:
    """Parse and validate CLI arguments in the same order as the Go program.
    Returns (filename, b, steps, cell_width). Exits with code 1 on error.
    """
    if not isinstance(argv, list):
        print("Internal error: argv must be a list.")
        sys.exit(1)
    if len(argv) != 5:
        print(USAGE)
        sys.exit(1)

    # argv[0] is the script name
    filename = argv[1]

    # Parse b (float), steps (int), cell_width (int)
    try:
        b = float(argv[2])
    except Exception:
        print("Error: <b> must be a floating-point number.")
        print(USAGE)
        sys.exit(1)

    try:
        steps = int(argv[3])
        if steps < 0:
            raise ValueError
    except Exception:
        print("Error: <steps> must be a non-negative integer.")
        print(USAGE)
        sys.exit(1)

    try:
        cell_width = int(argv[4])
        if cell_width <= 0:
            raise ValueError
    except Exception:
        print("Error: <cell_width> must be a positive integer.")
        print(USAGE)
        sys.exit(1)

    return filename, b, steps, cell_width


def main():
    print("Parsing command line arguments...")
    filename, b, steps, cell_width = parse_args(sys.argv)

    print("Command line arguments read.")
    # Initialize pygame (no display window needed to render Surfaces)
    pygame.init()

    print("Reading board from file.")
    # Read initial board (C/D characters)
    board = read_board_from_file(filename)

    print("Evolving board.")
    # Evolve
    boards = evolve(board, steps, b)

    print("Rendering frames with pygame.")
    # Render frames with pygame as circles (radius = 0.8 * half cell width)
    surfaces = draw_game_boards(boards, cell_width)

    print("Saving video from frames.")
    # Save video (keeping close to Go's 'prisoners' name)
    out_path = "output/jeff_didn't_k_h.mp4"
    save_video_from_surfaces(surfaces, out_path, 8, "libx264", 8)

    # Cleanly shut down pygame
    pygame.quit()

    print(f"Done! Wrote video to {out_path}.")


if __name__ == "__main__":
    main()
