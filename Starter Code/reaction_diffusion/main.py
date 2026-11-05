"""
main.py

Reaction-diffusion simulator entry point.

Usage:
    random or clustered init:
        python3 main.py {random|clustered} <reaction_csv> <n_per_species> <width> <height> <steps>

    csv-loaded particle init:
        python3 main.py csv <reaction_csv> <particle_csv> <steps>

n_per_species can be a single int (broadcast to every species) or a comma list
(one count per species, e.g. "700,50,0").

num_procs is inferred via multiprocessing.cpu_count().
"""

import multiprocessing
import os
import sys
import time

from custom_io import (
    load_reaction_table,
    load_particles,
    make_random_particles,
    make_clustered_particles,
)
from serial   import simulate_serial
from parallel import simulate_parallel
from datatypes import SimulationParameters


ACTIVATION_RANGE   = 28.0
PROXIMITY_INTERVAL = 5
RADIUS             = 6.0


def main() -> None:
    # Imports for rendering live inside main() so that multiprocessing
    # workers (which re-execute this module on spawn) don't pay the cost of
    # loading pygame and matplotlib.
    from drawing  import frames_to_surfaces
    from animate  import animate_surfaces
    from plotting import plot_species_counts

    print("Reaction-diffusion simulation!")

    if len(sys.argv) < 2:
        raise ValueError("Usage: python3 main.py {random|clustered|csv} ...")

    mode = sys.argv[1].lower()
    num_procs = multiprocessing.cpu_count()

    # Two flavors of particle init that take counts + box size off the
    # command line. `random` scatters everyone across the whole box;
    # `clustered` puts each species in its own vertical band.
    if mode == "random" or mode == "clustered":
        if len(sys.argv) != 7:
            raise ValueError(
                "Usage: python3 main.py {random|clustered} reaction_csv n_per_species width height steps"
            )
        reaction_csv = sys.argv[2]
        counts_arg   = sys.argv[3]
        width        = float(sys.argv[4])
        height       = float(sys.argv[5])
        n_steps      = int(sys.argv[6])

        table = load_reaction_table(reaction_csv)

        # The counts argument is either a single integer (broadcast to every
        # species) or a comma-separated list (one count per species).
        if "," in counts_arg:
            counts: list[int] = []
            for c in counts_arg.split(","):
                counts.append(int(c.strip()))
            if len(counts) != table.num_species:
                raise ValueError(
                    f"Expected {table.num_species} comma-separated counts, got {len(counts)}."
                )
        else:
            counts = [int(counts_arg)] * table.num_species

        if mode == "random":
            particles = make_random_particles(counts, table.num_species,
                                              width, height,
                                              table.diffusion_rates, RADIUS)
        else:
            particles = make_clustered_particles(counts, table.num_species,
                                                 width, height,
                                                 table.diffusion_rates, RADIUS)

    # Third flavor: read particles directly from a CSV file -- positions,
    # species, and per-particle diffusion rates are all baked in. Useful for
    # reproducing a specific scenario.
    elif mode == "csv":
        if len(sys.argv) != 5:
            raise ValueError(
                "Usage: python3 main.py csv reaction_csv particle_csv steps"
            )
        reaction_csv = sys.argv[2]
        particle_csv = sys.argv[3]
        n_steps      = int(sys.argv[4])

        table = load_reaction_table(reaction_csv)
        particles, width, height = load_particles(particle_csv)

    else:
        raise ValueError(f"Unknown mode '{mode}'. Use random, clustered, or csv.")

    print(f"Loaded {table.num_species} species and {len(particles)} particles.")

    params = SimulationParameters(
        width              = width,
        height             = height,
        num_particles      = len(particles),
        activation_range   = ACTIVATION_RANGE,
        proximity_interval = PROXIMITY_INTERVAL,
        num_steps          = n_steps,
    )

    # Output directory: output/<reaction_csv_stem>/, stripping any "reactions_" prefix.
    stem = os.path.splitext(os.path.basename(reaction_csv))[0]
    if stem.startswith("reactions_"):
        stem = stem[len("reactions_"):]
    elif stem.startswith("reaction_"):
        stem = stem[len("reaction_"):]
    out_dir = os.path.join("output", stem)
    os.makedirs(out_dir, exist_ok=True)
    print(f"Output: {out_dir}/")

    # Run the serial simulator first, render its animation and counts plot,
    # and time the simulation for comparison with the parallel version.
    print("Running serial simulation.")
    t0 = time.time()
    serial_frames = simulate_serial(particles, table, params)
    serial_time = time.time() - t0
    print(f"Serial simulation complete in {serial_time:.3f}s.")

    print("Rendering serial animation.")
    serial_surfaces = frames_to_surfaces(serial_frames, table, params)
    animate_surfaces(serial_surfaces, os.path.join(out_dir, "serial.mp4"))
    plot_species_counts(serial_frames, table, os.path.join(out_dir, "serial_counts.png"))

    # Now run the parallel simulator (same inputs) so we can compare both
    # the wall-clock and the resulting animations side by side.
    print(f"Running parallel simulation ({num_procs} processes).")
    t1 = time.time()
    parallel_frames = simulate_parallel(particles, table, params, num_procs)
    parallel_time = time.time() - t1
    print(f"Parallel simulation complete in {parallel_time:.3f}s.")

    print("Rendering parallel animation.")
    parallel_surfaces = frames_to_surfaces(parallel_frames, table, params)
    animate_surfaces(parallel_surfaces, os.path.join(out_dir, "parallel.mp4"))
    plot_species_counts(parallel_frames, table, os.path.join(out_dir, "parallel_counts.png"))

    print()
    print("--- Timing ---")
    print(f"Serial:   {serial_time:.3f}s")
    print(f"Parallel: {parallel_time:.3f}s ({num_procs} processes)")
    if parallel_time > 0:
        print(f"Speedup:  {serial_time / parallel_time:.2f}x")

    print("Animation finished! Exiting normally.")


if __name__ == "__main__":
    main()
