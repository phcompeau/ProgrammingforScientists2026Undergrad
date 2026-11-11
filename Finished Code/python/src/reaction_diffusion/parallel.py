"""
parallel.py

Parallel reaction-diffusion simulation loop using spatial decomposition + halo exchange.

Particles are assigned to vertical strips by x-coordinate at the start of every
batch. Each worker advances its own strip by proximity_interval motion steps
and then applies contact + unary reactions within the strip. To make
cross-strip reactions work, each worker also receives a 'halo' of particles
from adjacent strips that are within activation_range of the boundary; those
halo particles act as read-only catalysts (a strip particle can be converted
by a halo particle, but halo particles are not modified or returned). Halos
wrap across the box edges to match the toroidal distance metric used in
apply_reactions.

Implementation notes
--------------------
* multiprocessing.Pool is created once at the start and reused across all
  batches -- spawning a fresh pool every batch is prohibitively slow on
  macOS (each process boots a fresh interpreter).
* Pool.starmap copies the strip + halo to each worker. The worker mutates
  its local strip particles and returns them; the parent assembles fresh
  particle objects with each batch. Frames can therefore be stored by
  reference -- no per-frame deepcopy is needed.
"""

import copy
import multiprocessing
import random

from datatypes import Particle, ReactionTable, SimulationParameters
from functions import apply_unary_reactions, rand_step, toroidal_distance


def simulate_parallel(particles: list[Particle],
                      table: ReactionTable,
                      params: SimulationParameters,
                      num_procs: int) -> list[list[Particle]]:
    """Run the simulation using spatial decomposition.

    Each batch:
      1. Assign current particles to num_procs vertical strips by x.
      2. Compute each strip's halo (particles from adjacent strips, with wrap,
         within activation_range of the boundary).
      3. starmap process_strip across all strips.
      4. Reassemble strips into a global frame.

    Args:
        particles: Initial configuration (not mutated).
        table:     ReactionTable for conversion lookups.
        params:    Simulation parameters.
        num_procs: Number of worker processes (= number of strips).

    Returns:
        List of snapshots, one per batch (including the initial step).
    """
    # first, let's make the current list of particles and the list of "snapshots" that we eventually want to return
    current: list[Particle] = copy.deepcopy(particles)
    frames: list[list[Particle]] = [copy.deepcopy(current)]

    # question: how many snapshots will I eventually take?
    # remember: proximity_interval = number of steps between snapshots
    num_batches = params.num_steps // params.proximity_interval
    remainder = params.num_steps % params.proximity_interval

    # let's make our worker pool
    pool = multiprocessing.Pool(num_procs)

    # again, we divide into batches
    for _ in range(num_batches):
        # divide the space into vertical strips
        # key tricky point: each worker needs to know the collection of points that fall in its strip + the collection of particles that are close enough to its strip to maybe be involved in a reaction
        strips, halos = assign_strips_with_halos(current, num_procs, params.width, params.activation_range)

        # next, create list of all the arguments that are passed as inputs to each worker
        worker_args: list[tuple] = []
        for i in range(num_procs):
            worker_args.append((strips[i], halos[i], table, params, params.proximity_interval, True))

        # now we call the critical pool method (starmap)
        # this is where the parallelization happens
        results = pool.starmap(process_strip, worker_args)

        # now we compile the results, list[list[Particle]]
        current = []
        for strip in results:  # strip is list[Particle]
            current.extend(strip)

        # now, current is set: all particles in our snapshot
        frames.append(current)

    # run any leftover steps that are remaining that don't involve reactions
    if remainder > 0:
        strips, halos = assign_strips_with_halos(current, num_procs, params.width, params.activation_range)

        worker_args = []
        # range over all workers and give each one what it needs
        for i in range(num_procs):
            worker_args.append((strips[i], halos[i], table, params, remainder, False))

        results = pool.starmap(process_strip, worker_args)

        # now we compile the results, list[list[Particle]]
        current = []
        for strip in results:  # strip is list[Particle]
            current.extend(strip)

        # now, current is set: all particles in our snapshot
        frames.append(current)

    # at the end of the process, fire all the workers
    pool.close()
    pool.join()

    return frames


def assign_strips_with_halos(particles: list[Particle],
                             num_strips: int,
                             width: float,
                             halo_width: float) -> tuple[list[list[Particle]],
                                                         list[list[Particle]]]:
    """Partition particles into strips and compute each strip's halo.

    Strip i covers x in [i * W/N, (i+1) * W/N). Strip i's halo consists of
    particles in strips i-1 and i+1 that lie within halo_width of strip i's
    boundary, with toroidal wrap: strip 0's left neighbor is the rightmost
    strip, and the rightmost strip's right neighbor is strip 0. This matches
    the toroidal distance metric used by apply_reactions.

    Args:
        particles:  All particles.
        num_strips: Number of strips (= number of processes).
        width:      Total box width.
        halo_width: Halo radius (typically params.activation_range).

    Returns:
        (strips, halos), each a list of length num_strips.
    """
    # first, set strip width and declare them
    strip_width = width/num_strips
    strips: list[list[Particle]] = []

    # every strip starts as empty
    for _ in range(num_strips):
        strips.append([])

    # we range over particles and assign each one to the strip it belongs to
    for p in particles:
        idx = int(p.position.x / strip_width)

        # it could be that the point has walked off the board but has not been wrapped
        if idx >= num_strips:
            idx = num_strips-1
        if idx < 0:
            idx = 0

        # now, assign the current particle to its appropriate strip
        strips[idx].append(p)

    # we now need to build each strip's halo (the particles that could possibly be used in a reaction in a neighboring strip)
    halos: list[list[Particle]] = []

    # every halo starts as empty
    for _ in range(num_strips):
        halos.append([])

    # let's range over all the strips and determine the particles belonging to its halo
    for i in range(num_strips):
        # what range of x values are possible in this strip
        x_lo = i*strip_width
        x_hi = (i+1)*strip_width

        # pull in the particles from the left strip (if not in first strip)
        if i > 0:
            for p in strips[i-1]:
                if p.position.x >= x_lo - halo_width:
                    halos[i].append(p)

        # pull in the particles from the right strip (if not in last strip)
        if i < num_strips-1:
            for p in strips[i+1]:
                if p.position.x <= x_hi + halo_width:
                    halos[i].append(p)

        # finally, apply "toroidal wrap" to the first and last strip
        if num_strips >= 2:
            if i == 0:
                for p in strips[num_strips-1]:
                    if p.position.x >= width-halo_width:
                        halos[i].append(p)
            elif i == num_strips - 1:
                # look in the first strip for anything close to left edge
                for p in strips[0]:
                    if p.position.x <= halo_width:
                        halos[i].append(p)

    return strips, halos


def process_strip(strip_particles: list[Particle],
                  halo_particles:  list[Particle],
                  table:           ReactionTable,
                  params:          SimulationParameters,
                  steps_to_run:    int,
                  do_reactions:    bool) -> list[Particle]:
    """Worker: advance a strip and apply reactions.

    Both strip and halo particles are advanced by steps_to_run motion steps so
    that proximity checks use post-move positions on both sides. Halo particles
    are not returned -- their canonical copies live in the strip-worker that
    owns them. After motion, contact reactions may convert any strip particle
    using catalysts drawn from strip + halo. Unary reactions (deaths,
    spontaneous conversions, births) act only on strip particles.

    Args:
        strip_particles: This worker's own particles (will be returned).
        halo_particles:  Adjacent-strip particles within activation_range
                         (read-only catalysts; discarded after this call).
        table:           ReactionTable for conversion lookups.
        params:          Simulation parameters.
        steps_to_run:    Number of motion steps before reactions are applied.
        do_reactions:    Whether to apply reactions this batch.

    Returns:
        The (mutated) strip particle list.
    """
    # first, move all the particles in the strip and the halo the appropriate number of steps
    for _ in range(steps_to_run):
        for p in strip_particles:
            rand_step(p, params.width, params.height)
        for p in halo_particles:
            rand_step(p, params.width, params.height)

    # second part is to apply the reactions
    if do_reactions:
        strip_particles = apply_reactions_with_halo(strip_particles, halo_particles, table, params)
        # fortunately, unary reactions don't involve a halo
        strip_particles = apply_unary_reactions(strip_particles, table, params)

    return strip_particles


def apply_reactions_with_halo(strip: list[Particle],
                              halo:  list[Particle],
                              table: ReactionTable,
                              params: SimulationParameters) -> list[Particle]:
    """Apply contact reactions inside a parallel worker, using strip + halo.

    This is the parallel cousin of apply_reactions in functions.py. The key
    difference is that ownership now matters: only strip particles can have
    their species changed (this worker owns them), but halo particles -- read-
    only borrows from neighboring strips -- can still trigger reactions in
    the strip. Without that, a strip particle right at the boundary couldn't
    react with a particle just on the other side of the strip line.

    The reaction-firing logic is the same as apply_reactions: pair check,
    table lookup, distance check, dice roll. The only difference is which
    particles each loop iterates over.

    Args:
        strip:  Particles owned by this worker (substrates: their species
                may change in place).
        halo:   Particles from adjacent strips that act as read-only
                catalysts (never modified).
        table:  ReactionTable for conversion lookups.
        params: Simulation parameters.

    Returns:
        The strip list (mutated in place; returned for caller convenience).
    """
    # possible catalysts are both the strip itself and the halo
    catalysts = strip + halo

    # range over all the possible pairs and see if there's a reaction
    for substrate in strip:
        for catalyst in catalysts:
            if catalyst is not substrate:  # don't have reaction with yourself
                # two things: is there a reaction involving these two?
                # are they close enough (within threshold distance) to actually react?
                # first test is faster, so we want to do it first
                reaction = table.table[catalyst.species][substrate.species]
                if reaction is not None:
                    # now we know that there is a reaction involving them
                    # now we check to see if they're close
                    d = toroidal_distance(catalyst.position, substrate.position, params.width, params.height)
                    if d <= params.activation_range:
                        # both are true, then we roll some dice to see if we apply the reaction to these particles
                        if random.random() < reaction.rate:
                            # update substrate to whatever the reaction gives
                            substrate.species = reaction.product

    return strip
