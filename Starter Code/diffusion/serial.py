"""
serial.py

Serial random-walk diffusion simulation loop.
"""

import copy

from datatypes import Particle
from functions import update_particles


def simulate_serial(particles: list[Particle],
                    num_steps: int,
                    width: float,
                    height: float) -> list[list[Particle]]:
    """Run the simulation serially, recording every step.

    Args:
        particles: Initial configuration (not mutated).
        num_steps: Total number of random-walk steps to run.
        width:     Box width (used for periodic wrapping).
        height:    Box height (used for periodic wrapping).

    Returns:
        List of snapshots of length num_steps + 1 (including step 0).
    """
    pass
