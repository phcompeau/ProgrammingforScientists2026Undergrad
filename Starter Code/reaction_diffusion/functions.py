"""
functions.py

Physics and reaction dynamics shared by the serial and parallel simulators.

Motion model
------------
Every particle takes a fixed-length step in a uniformly-random direction each
tick. The simulation lives on a periodic torus: a particle leaving one edge
re-enters from the opposite edge.

Reaction dynamics
-----------------
When two particles come within activation_range of each other, the reaction
table is consulted: table[catalyst][substrate] gives a ContactReaction or
None. If a ContactReaction is present, the substrate is converted to its
`product` species with the per-contact probability `rate`. The catalyst is
unchanged.

Because the table is fully general, any number of species and any interaction
pattern can be expressed.
"""

import math
import random

from datatypes import OrderedPair, Particle, ReactionTable, SimulationParameters


def rand_step(particle: Particle,
              width: float, height: float) -> None:
    """Take one random-walk step, wrapping around box edges.

    Args:
        particle: Particle to update (in-place).
        width:    Box width for wrapping.
        height:   Box height for wrapping.
    """
    pass


def toroidal_distance(p0: OrderedPair, p1: OrderedPair,
                      width: float, height: float) -> float:
    """Shortest distance between two points on a periodic (torus) box.

    A particle at x=0 and a particle at x=width-1 are 1.0 apart on the torus,
    not width-1 apart. This matches the wrap-around motion done by
    rand_step.

    Args:
        p0:     First point.
        p1:     Second point.
        width:  Box width (the periodic length along x).
        height: Box height (the periodic length along y).

    Returns:
        Shortest periodic distance as a float.
    """
    pass


def apply_reactions(particles: list[Particle],
                    table: ReactionTable,
                    params: SimulationParameters) -> list[Particle]:
    """Apply contact reactions: pair every particle with every other particle.

    For each ordered pair of distinct particles (A, B), we ask the reaction
    table what happens if A meets B. If table.table[A.species][B.species] is
    a ContactReaction and the pair is within activation_range (toroidally),
    B's species is changed to the reaction's product with probability
    reaction.rate. A is the "catalyst" (unchanged); B is the "substrate"
    (the one that may change).

    In each iteration of the outer loop, the same particle plays the
    substrate role; in the inner loop it plays the catalyst role for every
    other particle. So every particle is potentially both -- this is what
    "ordered pairs" means here.

    The list is mutated in place (only the species attribute changes; no
    particles are added or removed). We also return the list so the caller
    can use the same `current = apply_reactions(...)` pattern as
    apply_unary_reactions.

    Args:
        particles: Every particle in the simulation. Modified in place.
        table:     ReactionTable for conversion lookups.
        params:    Simulation parameters.

    Returns:
        The particles list (the same object as the input).
    """
    pass


def apply_unary_reactions(particles: list[Particle],
                          table: ReactionTable,
                          params: SimulationParameters) -> list[Particle]:
    """Apply spontaneous (contact-free) reactions: deaths, conversions, births.

    For each particle:
      1. Roll the death rule for its species (if any). A dead particle
         won't make it into the survivor list.
      2. If still alive, roll the spontaneous-conversion rule for its
         species (if any). The species attribute may be overwritten.
      3. Roll the birth rule for its species (if any). Birth is independent
         of death -- a particle dying this batch can still leave behind one
         offspring before being removed.

    Args:
        particles: Particle list (read-only here; we return a fresh list).
        table:     ReactionTable defining unary, birth, and death rules.
        params:    Simulation parameters (provides box size).

    Returns:
        A new particle list containing the survivors plus any newly born
        particles. The caller should reassign their reference.
    """
    pass
