"""
serial.py

Serial reaction-diffusion simulation loop.
"""

import copy

from datatypes import Particle, ReactionTable, SimulationParameters
from functions import apply_reactions, apply_unary_reactions, rand_step


def simulate_serial(particles: list[Particle],
                    table: ReactionTable,
                    params: SimulationParameters) -> list[list[Particle]]:
    """Run the simulation serially.

    Each batch:
      1. Move every particle proximity_interval times.
      2. Apply contact reactions once using the reaction table.
      3. Apply unary reactions (deaths, spontaneous conversions, births).
      4. Record a frame.

    Args:
        particles: Initial configuration (not mutated).
        table:     ReactionTable for conversion lookups.
        params:    Simulation parameters.

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

    # now, I just range over all the batches and apply reaction-diffusion to each one
    for _ in range(num_batches):
        # move all my points proximity_interval times
        for _ in range(params.proximity_interval):
            for p in current:
                rand_step(p, params.width, params.height)

        # now I want to apply the reactions
        # contact reactions first, then unary
        current = apply_reactions(current, table, params)
        current = apply_unary_reactions(current, table, params)

        # add the current snapshot to overall list
        frames.append(copy.deepcopy(current))

    # we may have a few steps left over of just random walking
    if remainder > 0:
        # move all my points remainder times
        for _ in range(remainder):
            for p in current:
                rand_step(p, params.width, params.height)

    return frames
