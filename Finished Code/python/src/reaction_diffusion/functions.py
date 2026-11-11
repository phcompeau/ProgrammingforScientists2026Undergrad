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
    angle = random.uniform(0.0, 2.0 * math.pi)
    particle.position.x = (particle.position.x + (particle.diffusion_rate * math.cos(angle))) % width
    particle.position.y = (particle.position.y + (particle.diffusion_rate * math.sin(angle))) % height


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
    dx = abs(p0.x-p1.x)
    dy = abs(p0.y-p1.y)

    # trick: we "wrap around" if when wrapping around, distance in the x direction is smaller than dx (or the same for dy)
    # width = 1000, p0.x = 1, p1.x = 999 -- dx = 998, but they're actually 2 away
    # idea: update dx, and dy to be min of their current values and width-dx or height-dy
    if width-dx < dx:
        dx=width-dx
    if height-dy < dy:
        dy=height-dy

    return math.sqrt(dx*dx + dy*dy)


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
    # find all pairs of particles that might interact
    # range over list twice
    for substrate in particles:
        for catalyst in particles:
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

    return particles


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
    # create two lists that will be useful: one for survivors, one for births
    survivors: list[Particle] = []
    births: list[Particle] = []

    # apply each of the three reaction types

    for particle in particles:
        # rule #1: does it die out?
        dead = False
        for d in table.death_reactions:
            if particle.species == d.species:
                # we find that this particle can die
                # does it?
                if random.random() < d.rate:
                    dead = True

        # now we'll move on to rule 2: does it change?
        # it can only change from one species to another if it's alive
        if not dead:
            for u in table.unary_reactions:
                if particle.species == u.from_species:
                    if random.random() < u.rate:
                        particle.species = u.to_species

        # rule 3: is there a new particle born?
        for b in table.birth_reactions:
            if particle.species == b.species:
                # roll the dice one more time,
                if random.random() < b.rate:
                    # if there's a win, place it randomly
                    births.append(Particle(position = OrderedPair(
                                           x = random.uniform(0.0, params.width),
                                           y = random.uniform(0.0, params.height)),
                                           species = particle.species,
                                           radius = particle.radius,
                                           diffusion_rate=particle.diffusion_rate))

        # at this point in time, if the particle has survived all this, then we want it to add it to the survivors
        if not dead:
            survivors.append(particle)

    return survivors + births
