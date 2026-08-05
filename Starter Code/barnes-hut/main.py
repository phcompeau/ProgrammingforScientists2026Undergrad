import sys
import numpy as np
import imageio
import time
import pygame.surfarray

from initialization import initialize_galaxy, initialize_universe, push
from engine import barnes_hut
from drawing import animate_system
from datatypes import OrderedPair


def surface_to_array(surface: pygame.Surface) -> np.ndarray:
    """Convert a Pygame Surface to a NumPy array suitable for imageio."""
    return np.transpose(pygame.surfarray.array3d(surface), (1, 0, 2))


def main():
    # Expect: python main.py num_stars num_gens time_interval theta canvas_width frequency
    if len(sys.argv) != 7:
        raise ValueError(
            "Usage: python main.py <num_stars> <num_gens> <time_interval> <theta> <canvas_width> <frequency>\n"
            "Example: python main.py 100 10000 4e16 1.0 1000 100"
        )

    num_stars = int(sys.argv[1])
    num_gens = int(sys.argv[2])
    time_interval = float(sys.argv[3])
    theta = float(sys.argv[4])
    canvas_width = int(sys.argv[5])
    frequency = int(sys.argv[6])

    # Basic type sanity check (optional clarity for beginners)
    if not all(isinstance(v, int) for v in [num_stars, num_gens, canvas_width, frequency]):
        raise ValueError("num_stars, num_gens, canvas_width, and frequency must be integers.")
    if not all(isinstance(v, float) for v in [time_interval, theta]):
        raise ValueError("time_interval and theta must be floating-point numbers.")

    # --- initialize galaxies ---
    g0 = initialize_galaxy(num_stars, 4e21, 5.0e22 - 4.0e21, 5.0e22+4.0e21)
    push(g0, OrderedPair(1.5e2, 0))
    g1 = initialize_galaxy(num_stars, 4e21, 5.0e22 + 4.0e21, 5.0e22-4.0e21)
    push(g1, OrderedPair(-1.5e2, 0))

    width = 1.0e23
    galaxies = [g0, g1]
    initial_universe = initialize_universe(galaxies, width)

    # --- run simulation ---
    start = time.time()
    time_points = barnes_hut(initial_universe, num_gens, time_interval, theta)
    print(f"Simulation complete in {time.time() - start:.2f}s")

    # --- draw and render ---
    scaling_factor = 1e11  # could later also be a CLI argument if desired
    image_list = animate_system(time_points, canvas_width, frequency, scaling_factor)

    output_filename = "galaxy.mp4"
    fps = 30
    with imageio.get_writer(output_filename, fps=fps, codec="libx264") as writer:
        for surface in image_list:
            writer.append_data(surface_to_array(surface))
    print("Saved video as galaxy.mp4")


if __name__ == "__main__":
    main()