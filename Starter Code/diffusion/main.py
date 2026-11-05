"""
main.py

Random-walk diffusion simulator entry point.

Usage:
    python3 main.py <num_particles> <num_steps> <width> <scatter|center> <drawing_frequency>

Example:
    python3 main.py 100 1000 500 center 10

Every particle takes a random step of fixed length each tick.
With "center", all particles start at the center of the box
(a "drop of dye") and spread out over time. With "scatter",
particles start uniformly at random across the box.
"""

import multiprocessing
import os
import random
import sys
import time

from datatypes import OrderedPair, Particle
from drawing  import frames_to_surfaces
from animate  import animate_surfaces
from serial   import simulate_serial
from parallel import simulate_parallel


# Physics/visual tuning (not scenario parameters).
PARTICLE_RADIUS = 5.0
DIFFUSION_RATE  = 1.0

# Rendering colors (RGB).
BACKGROUND_COLOR = (18, 18, 31)
PARTICLE_COLOR   = (255, 255, 255)


def main() -> None:
    print("Random-walk diffusion simulation!")

    if len(sys.argv) != 6:
        raise ValueError(
            "Usage: python3 main.py <num_particles> <num_steps> <width> <scatter|center> <drawing_frequency>"
        )

    num_particles     = int(sys.argv[1])
    num_steps         = int(sys.argv[2])
    width             = float(sys.argv[3])
    mode              = sys.argv[4].lower()
    drawing_frequency = int(sys.argv[5])

    if num_particles <= 0:
        raise ValueError("num_particles must be > 0.")
    if num_steps < 0:
        raise ValueError("num_steps must be >= 0.")
    if width <= 0.0:
        raise ValueError("width must be > 0.")
    if drawing_frequency <= 0:
        raise ValueError("drawing_frequency must be > 0.")
    if mode != "scatter" and mode != "center":
        raise ValueError("mode must be 'scatter' or 'center'.")

    height = width  # square box
    scatter = (mode == "scatter")
    num_procs = multiprocessing.cpu_count()

    particles = initialize_particles(
        num_particles  = num_particles,
        width          = width,
        height         = height,
        radius         = PARTICLE_RADIUS,
        diffusion_rate = DIFFUSION_RATE,
        scatter        = scatter,
    )
    print(f"Initialized {len(particles)} particles "
          f"({'scattered' if scatter else 'centered'}).")

    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    print(f"Output: {out_dir}/")

    # serial simulation (timed)
    print("Running serial simulation.")
    start_serial = time.time()
    serial_frames = simulate_serial(particles, num_steps, width, height)
    serial_time = time.time() - start_serial
    print(f"Serial simulation complete in {serial_time:.3f}s.")

    print("Rendering serial animation.")
    serial_surfaces = frames_to_surfaces(serial_frames, width, height, BACKGROUND_COLOR, PARTICLE_COLOR, drawing_frequency)
    animate_surfaces(serial_surfaces, os.path.join(out_dir, "serial.mp4"))

    # parallel simulation (timed)
    print(f"Running parallel simulation ({num_procs} processes).")
    start_parallel = time.time()
    parallel_frames = simulate_parallel(particles, num_steps, num_procs, width, height)
    parallel_time = time.time() - start_parallel
    print(f"Parallel simulation complete in {parallel_time:.3f}s.")

    print("Rendering parallel animation.")
    parallel_surfaces = frames_to_surfaces(parallel_frames, width, height, BACKGROUND_COLOR, PARTICLE_COLOR, drawing_frequency)
    animate_surfaces(parallel_surfaces, os.path.join(out_dir, "parallel.mp4"))

    # timing summary
    print()
    print("--- Timing ---")
    print(f"Serial:   {serial_time:.3f}s")
    print(f"Parallel: {parallel_time:.3f}s ({num_procs} processes)")
    if parallel_time > 0:
        print(f"Speedup:  {serial_time / parallel_time:.2f}x")

    print("Animation finished! Exiting normally.")


def initialize_particles(num_particles: int,
                         width: float,
                         height: float,
                         radius: float,
                         diffusion_rate: float,
                         scatter: bool) -> list[Particle]:
    """Create a list of particles for the simulation.

    Args:
        num_particles:  Number of particles to create.
        width:          Box width.
        height:         Box height.
        radius:         Particle radius (visual only).
        diffusion_rate: Length of each random-walk step.
        scatter:        If True, place particles uniformly at random across
                        the box. If False, place every particle at the center
                        (a "drop of dye").

    Returns:
        Flat list of all particles.
    """
    particles: list[Particle] = []
    for _ in range(num_particles):
        if scatter:
            position = OrderedPair(
                x = random.uniform(0.0, width),
                y = random.uniform(0.0, height),
            )
        else:
            position = OrderedPair(x = width / 2.0, y = height / 2.0)
        particles.append(Particle(
            position       = position,
            radius         = radius,
            diffusion_rate = diffusion_rate,
        ))
    return particles


if __name__ == "__main__":
    main()
