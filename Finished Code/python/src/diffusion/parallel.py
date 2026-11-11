"""
parallel.py

Parallel random-walk diffusion simulation loop using spatial decomposition.

Particles are assigned to vertical stripes by x-coordinate each step,
and each worker advances its own stripe. Re-striping every step
naturally handles particles that crossed stripe boundaries.

This shape positions the simulator for chemical reactions: with stripes,
reaction pair checks stay local to a worker (plus a thin halo of nearby
particles from adjacent stripes). The current implementation does no
halo exchange yet because diffusion has no inter-particle interactions.

Implementation note: per-step parallelism requires workers that persist
across many small jobs. multiprocessing.Pool spawns its workers once
at construction and reuses them; the Process + Queue pattern from
parallel_craps would re-spawn every step, which is prohibitively slow
on macOS (where each spawn boots a fresh interpreter).
"""

import copy
import multiprocessing

from datatypes import Particle
from functions import update_particles


def simulate_parallel(particles: list[Particle],
                      num_steps: int,
                      num_procs: int,
                      width: float,
                      height: float) -> list[list[Particle]]:
    """Run the simulation by splitting particles into spatial stripes.

    Each step:
      1. Assign current particles to num_procs vertical stripes by x.
      2. pool.starmap advances every stripe by one random-walk step.
      3. Reassemble into a global frame.

    Args:
        particles: Initial configuration (not mutated).
        num_steps: Total number of random-walk steps to run.
        num_procs: Number of worker processes (= number of stripes).
        width:     Box width (for striping and periodic wrapping).
        height:    Box height (for periodic wrapping).

    Returns:
        List of snapshots of length num_steps + 1 (including step 0).
    """
    # current will store my current generation of particles
    current = copy.deepcopy(particles)
    frames: list[list[Particle]] = [copy.deepcopy(current)]

    # it would be a bad idea to create workers every time through a new generation

    # each worker is going to be responsible for a vertical "stripe" of our space of equal size
    # the workers are only going to get initialized once (create a pool)
    pool = multiprocessing.Pool(num_procs)

    # range over all the steps
    for _ in range(1, num_steps+1):
        # divide the space
        stripes = assign_stripes(current, num_procs, width)
        # stripes[0] holds the particles associated with worker 0, stripes[1] holds particles for worker 1, etc.

        # next, assign each worker precisely one stripe

        worker_args: list[tuple[list[Particle], float, float]] = []

        # let's assign the i-th worker the three parameters that update_particles needs
        for stripe in stripes:
            worker_args.append((stripe, width, height))

        # this starts the process of each worker calling update_particles() on its stripe (subset of particles that it was assigned)
        moved_stripes = pool.starmap(update_particles, worker_args)

        # the starmap call blocks until they are all finished

        # in other words, we wait on them to all finish

        # let's combine their work
        current = []

        # at this point in time, moved_stripes is a list[list[Particle]] where moved_stripes[i] has the particles that were moved by worker i

        for stripe in moved_stripes:
            # stripe is a list[Particle]
            current.extend(stripe)

        # we now have updated positions of all particles and I will add the current snapshot into frames

        frames.append(copy.deepcopy(current))

    # at this point, we are going to indicate that work is done and the workers can be "retired"
    pool.close()  # no more work coming
    pool.join()   # you're all fired

    return frames


def assign_stripes(particles: list[Particle],
                   num_stripes: int,
                   width: float) -> list[list[Particle]]:
    """Partition particles into vertical stripes by x-coordinate.

    Args:
        particles:   All particles.
        num_stripes: Number of stripes (= number of processes).
        width:       Total box width.

    Returns:
        List of num_stripes particle lists. Positions are guaranteed to
        be in [0, width) by torus wrapping in update_particles, so no
        out-of-range clamping is needed.
    """
    # how wide is the current stripe?
    stripe_width = width/num_stripes

    # stripes[i] holds the list of particles associated with worker i
    stripes: list[list[Particle]] = []

    # every worker starts off receiving an empty list of particles
    for _ in range(num_stripes):
        stripes.append([])

    # range over every particle in the universe, assigning current particle to the worker that it should be assigned to
    for p in particles:
        # e.g., 10 processes and width = 200 -> stripe_width = 200/10 = 20
        # if x coordinate of particle's position is 47, then int(47/20) = int(2.something) = 2
        i = int(p.position.x/stripe_width)

        # i is the index of the worker that this particle should be assigned to
        stripes[i].append(p)

    return stripes
