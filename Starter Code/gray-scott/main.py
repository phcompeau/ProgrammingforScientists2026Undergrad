import os
import sys
import pygame
import numpy as np
import imageio.v2 as imageio  # imageio handles MP4 export

from datatypes import Board
from functions import simulate_gray_scott, initialize_board
from drawing import draw_boards


def pygame_surface_to_numpy(surface: pygame.Surface) -> np.ndarray:
    """
    Convert a Pygame Surface to a NumPy RGB image array.

    Returns:
        np.ndarray: The frame as (height, width, 3) uint8 RGB.
    """
    return pygame.surfarray.array3d(surface).transpose(1, 0, 2)


def main():
    print("Gray–Scott reaction–diffusion model")

    num_rows = 100
    num_cols = 100

    print("Parameters read in successfully!")

    pygame.init()

    # initialize empty board
    initial_board: Board = initialize_board(num_rows, num_cols)

    # how many predator rows and columns are there?
    frac = 0.05
    pred_rows = int(frac * num_rows)
    pred_cols = int(frac * num_cols)
    mid_row, mid_col = num_rows // 2, num_cols // 2

    # a little for loop to fill predators
    for r in range(mid_row - pred_rows // 2, mid_row + pred_rows // 2):
        for c in range(mid_col - pred_cols // 2, mid_col + pred_cols // 2):
            initial_board[r][c] = (initial_board[r][c][0], 1) # predators

    # make prey = 1 everywhere
    for r in range(len(initial_board)):
        for c in range(len(initial_board[r])):
            initial_board[r][c] = (1, initial_board[r][c][1])

    # parameters
    num_gens = 8000
    feed_rate = 0.034
    kill_rate = 0.095

    # kernel for diffusion
    kernel = np.array([
        [0.05, 0.2, 0.05],
        [0.2, -1.0, 0.2],
        [0.05, 0.2, 0.05],
    ])

    print("Starting simulation...")
    boards = simulate_gray_scott(
        initial_board,
        num_gens,
        feed_rate,
        kill_rate,
        prey_diffusion_rate=0.2,
        predator_diffusion_rate=0.1,
        kernel=kernel,
    )
    print("Simulation complete!")

    print("Drawing boards to file")

    # for visualization
    n = 100
    cell_width = 1

    surfaces = draw_boards(boards, cell_width, n)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "Gray-Scott")
    print("Encoding video with imageio...")
    video_path = f"{output_file}.mp4"
    writer = imageio.get_writer(video_path, fps=10, codec="libx264", quality=8)

    for surf in surfaces:
        frame = pygame_surface_to_numpy(surf)
        writer.append_data(frame)

    writer.close()

    print(f"Video saved as {video_path}")

    pygame.quit()


if __name__ == "__main__":
    main()
