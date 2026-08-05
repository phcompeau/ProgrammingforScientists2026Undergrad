"""
CLI entry point for the gravity simulation.

Usage:
    python main.py <scenario_name> <num_gens> <time_step> <canvas_width> <drawing_frequency>

Example:
    python main.py jupiter_4 2000 0.01 800 5

This will read:   data/jupiter_4.txt
and write video:  output/jupiter_4.mp4
"""

import sys
import os
import time
import imageio.v2 as imageio
from custom_io import read_universe
from gravity import simulate_gravity
from drawing import animate_system, pygame_surface_to_numpy


def main() -> None:
    """
    Run the full pipeline:
      1) read universe from file
      2) simulate gravity for N generations
      3) render selected frames to pygame surfaces
      4) encode frames to an MP4 video
    """
    print("Let's simulate gravity!")

    # Expect 5 user arguments (plus program name)
    if len(sys.argv) != 6:
        raise ValueError(
            "Error: incorrect number of command line arguments.\n\n"
            "Usage:\n"
            "  python main.py <scenario_name> <num_gens> <time_step> <canvas_width> <drawing_frequency>\n"
            "Example:\n"
            "  python main.py jupiter_4 2000 0.01 800 5"
        )

    scenario = sys.argv[1]
    input_file = f"data/{scenario}.txt"
    output_stub = f"output/{scenario}"

    # Parse CLI arguments
    num_gens = int(sys.argv[2])
    time_step = float(sys.argv[3])
    canvas_width = int(sys.argv[4])
    drawing_frequency = int(sys.argv[5])

    if num_gens < 0:
        raise ValueError("Error: num_gens must be >= 0.")
    if time_step <= 0.0:
        raise ValueError("Error: time_step must be > 0.")
    if canvas_width <= 0:
        raise ValueError("Error: canvas_width must be > 0.")
    if drawing_frequency <= 0:
        raise ValueError("Error: drawing_frequency must be > 0.")

    print("Command line arguments read!")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_stub), exist_ok=True)

    # Read initial universe (also sets Universe.gravitational_constant via file)
    initial_universe = read_universe(input_file)

    # --- Simulate ---
    print("Simulating gravity now.")
    sim_start = time.time()
    time_points = simulate_gravity(initial_universe, num_gens, time_step)
    sim_end = time.time()
    print(f"Simulation complete. Time taken: {sim_end - sim_start:.2f} seconds")

    # --- Draw frames ---
    print("Rendering frames.")
    draw_start = time.time()
    surfaces = animate_system(time_points, canvas_width, drawing_frequency)
    draw_end = time.time()
    print(f"Rendered {len(surfaces)} frames in {draw_end - draw_start:.2f} seconds.")

    # --- Encode video ---
    print("Encoding MP4 video.")
    video_path = output_stub + ".mp4"

    # Create a writer object to write to file.
    # Note: libx264 requires ffmpeg available in your environment.
    writer = imageio.get_writer(video_path, fps=10, codec="libx264", quality=8)

    try:
        for surface in surfaces:
            frame = pygame_surface_to_numpy(surface)  # (H, W, 3) uint8
            writer.append_data(frame)
    finally:
        writer.close()

    print(f"Success! MP4 video produced at: {video_path}")
    print("Animation finished! Exiting normally.")


if __name__ == "__main__":
    main()