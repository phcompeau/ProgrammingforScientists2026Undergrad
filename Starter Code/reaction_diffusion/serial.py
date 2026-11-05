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
    pass
