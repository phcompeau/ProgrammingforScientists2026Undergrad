"""
functions.py

Physics shared by the serial and parallel diffusion simulators.
"""

import copy
import math
import random

from datatypes import Particle


def update_particles(current: list[Particle],
                     width: float,
                     height: float) -> list[Particle]:
    """Advance every particle by one random-walk step on a torus.

    After each random-walk step, particle positions are wrapped modulo
    the box dimensions, so the simulation lives on a periodic domain
    (a torus): a particle leaving the right edge re-enters from the left.

    Args:
        current: Particle list at the current step (not mutated).
        width:   Box width (used for periodic wrapping in x).
        height:  Box height (used for periodic wrapping in y).

    Returns:
        A fresh particle list with each particle moved one step,
        with positions wrapped into [0, width) x [0, height).
    """
    pass


def rand_step(particle: Particle) -> None:
    """Move a particle by its diffusion rate in a uniformly random direction.

    Args:
        particle: Particle to update (in-place).

    Returns:
        None
    """
    pass
