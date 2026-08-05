import os
from multiprocessing import Process, Queue
import math
import numpy as np
import pygame
from datatypes import Board


def animate_boards(time_points: list[Board], cell_width: int) -> list[np.ndarray]:
    """Generates a list of images corresponding to drawing each Board on a pygame 
        surface with the given cell width.
    Args:
        time_points: Sequence of boards to render
        cell_width: The width/height in pixels of each cell.

    Returns:
        List of frames as uint8 numpy arrays of shape (H, W, 3).
        In this format so we can use it with imageio and make a mp4 video later.
    """
    if len(time_points) == 0:
        raise ValueError("Error: no Board objects present in input to animate_boards.")
    
    # note each image is a numpy array representation of the pygame surface
    # used for creating mp4 video later
    images: list[np.ndarray] = [None] * len(time_points) 
    
    # for every board, draw to pygame surface
    for i in range(len(time_points)):
        images[i] = draw_to_image(time_points[i], cell_width)
        
    return images


def process_images_section(timepoints: list[Board], cell_width: int, start_offset: int, out_q: Queue) -> None:
    """Process a contiguous slice of boards and emit frames into a multiprocessing Queue.

    Args:
        timepoints: The slice of boards to render in this worker.
        cell_width: The width/height in pixels of each cell.
        start_offset: Global index offset used to place frames back in order.
        out_q: Multiprocessing Queue to which (global_index, frame) tuples are sent.
    """
    for i, board in enumerate(timepoints):
        frame = draw_to_image(board, cell_width)  # np.ndarray (H, W, 3), uint8
        out_q.put((start_offset + i, frame))


def animate_boards_parallel(time_points: list[Board], cell_width: int) -> list[np.ndarray]:
    """Parallelize rendering of boards using multiprocessing and return frames in order.

    Args:
        time_points: Sequence of boards to render.
        cell_width: The width/height in pixels of each cell.

    Returns:
        List of frames as uint8 numpy arrays of shape (H, W, 3), ordered by original index.
    """
    if len(time_points) == 0:
        raise ValueError("Error: no Board objects present in input to animate_boards_parallel.")
    
    num_procs = os.cpu_count()
    n = len(time_points)

    images_per_proc = n // num_procs
    ranges = []
    start = 0
    
    for i in range(num_procs):
        start = i * images_per_proc
        end = start + images_per_proc
        if i == num_procs - 1:
            end = n  # last takes remaining images
        
        ranges.append((start, end))

    out_q = Queue()
    procs: list[Process] = []
    for start, end in ranges:
        board_slice = time_points[start:end]
        if not board_slice: # just in case
            continue
        p = Process(
            target=process_images_section,
            args=(board_slice, cell_width, start, out_q),
        )
        p.start()
        procs.append(p)       

    # Collect exactly n frames
    images_np: list[np.ndarray] = [None] * n
    for _ in range(n):
        idx, frame = out_q.get()     # frame is already a new array in the parent
        images_np[idx] = frame       # no .copy() needed unless you want to duplicate it

    # # Ensure all workers finished (technically don't need this because the loop above waits til n frames are collected, so all processes should be finished when we get here)
    for p in procs:
        p.join()

    return images_np


def draw_to_image(b: Board, cell_width: int) -> np.ndarray:
    """Draw a single board to a numpy RGB frame using pygame filled circles per cell.

    Args:
        b: Board to render.
        cell_width: Each square cell has width cell_width
        
    Returns:
        Convert a pygame surface into a uint8 numpy array (H, W, 3) 
        representation suitable for imageio.
    """
    if b is None:
        raise ValueError("Can't draw a nil board.")

    num_rows = len(b)
    canvas_width = num_rows * cell_width

    # create a new pygame surface
    surface = pygame.Surface((canvas_width, canvas_width))

    dark_gray = (30, 30, 30)
    gray = (95, 95, 95)
    light_gray = (190, 190, 190)
    white = (255, 255, 255)

    # create a black background
    surface.fill(dark_gray)

    # fixed circle radius factor
    scaling_factor = 0.8
    radius = int(scaling_factor * (cell_width / 2.0))

    # range over all the bodies and draw them
    for i in range(num_rows):
        for j in range(len(b[0])):
            val = b[i][j]

            if val == 0:
                # background already dark_gray; skip
                continue
            elif val == 1:
                color = gray
            elif val == 2:
                color = light_gray
            elif val == 3:
                color = white
            else:
                t = float(val - 3)
                color = (
                    255,
                    int(255 - min(255, 40 * math.log2(t))),
                    int(255 - min(255, 80 * math.log2(t))),
                )

            # set central coordinates (x,y) for this cell
            x = j * cell_width + cell_width // 2
            y = i * cell_width + cell_width // 2

            # draw filled circle
            if val > 0:
                pygame.draw.circle(surface, color, (x, y), radius)

    # convert the surface to a numpy array for imageio (pygame returns (W,H,3))
    frame = pygame.surfarray.array3d(surface)
    frame = np.transpose(frame, (1, 0, 2)).copy()  # to (H,W,3), ensure contiguous
    return frame
