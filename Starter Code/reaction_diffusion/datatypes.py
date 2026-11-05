"""
datatypes.py

Core data types for the multi-species reaction-diffusion simulator.

Particles take fixed-length random-walk steps every tick. Any number of
species can be defined; conversion rules are loaded from a CSV reaction
table at runtime rather than being hardcoded.
"""

from dataclasses import dataclass, field


@dataclass
class OrderedPair:
    """A point or vector in two-dimensional space.

    Attributes:
        x: The x-coordinate.
        y: The y-coordinate.
    """
    x: float = 0.0
    y: float = 0.0


@dataclass
class Particle:
    """A single particle performing a 2D random walk.

    Attributes:
        position:       Current position as an OrderedPair.
        species:        Integer species ID (0-indexed, must be < num_species
                        in the reaction table).
        radius:         Visual radius (does not affect interactions).
        diffusion_rate: Length of each random-walk step.
    """
    position:       OrderedPair = field(default_factory=OrderedPair)
    species:        int         = 0
    radius:         float       = 5.0
    diffusion_rate: float       = 1.0


@dataclass
class Reaction:
    """Base type for any reaction. All reactions carry a per-event rate.

    Subclasses add the species ids that participate. Reaction objects are
    plain data; the simulation loop discriminates on subclass.
    """
    rate: float


@dataclass
class ContactReaction(Reaction):
    """A reaction that fires when two particles come into contact.

    When a particle of species `catalyst` meets a particle of species
    `substrate`, the substrate becomes species `product` with
    probability `rate` per contact. The catalyst is unchanged.
    """
    catalyst:  int
    substrate: int
    product:   int


@dataclass
class UnaryReaction(Reaction):
    """A spontaneous (contact-free) species conversion.

    Each particle of species `from_species` converts to `to_species`
    with probability `rate` per simulation batch.
    """
    from_species: int
    to_species:   int


@dataclass
class BirthReaction(Reaction):
    """A spontaneous spawn of a new particle of `species` per batch."""
    species: int


@dataclass
class DeathReaction(Reaction):
    """A spontaneous removal of a particle of `species` per batch."""
    species: int


@dataclass
class ReactionTable:
    """Defines what happens when two particles meet, plus all spontaneous events.

    The contact `table` is an N x N grid where table[i][j] is either a
    ContactReaction (i meeting j has an effect) or None (no reaction for
    that ordered pair). Self-meetings are permitted: table[i][i] may hold
    a ContactReaction.

    Attributes:
        table:            2D list -- table[catalyst][substrate] -> ContactReaction or None.
        num_species:      Number of distinct species (= len(table)).
        diffusion_rates:  Step length per species (length = num_species).
        names:            Display name per species (defaults to "Species N" if absent).
        colors:           RGB triple per species (each entry is (r, g, b) ints in 0-255).
        background_color: Canvas background as an (r, g, b) triple (defaults to white).
        unary_reactions:  Spontaneous species conversions.
        birth_reactions:  Spontaneous spawns.
        death_reactions:  Spontaneous removals.
    """
    table:            list[list[ContactReaction | None]] = field(default_factory=list)
    num_species:      int                                = 0
    diffusion_rates:  list[float]                        = field(default_factory=list)
    names:            list[str]                          = field(default_factory=list)
    colors:           list[tuple[int, int, int]]         = field(default_factory=list)
    background_color: tuple[int, int, int]               = (255, 255, 255)
    unary_reactions:  list[UnaryReaction]                = field(default_factory=list)
    birth_reactions:  list[BirthReaction]                = field(default_factory=list)
    death_reactions:  list[DeathReaction]                = field(default_factory=list)


@dataclass
class SimulationParameters:
    """All fixed parameters governing the simulation.

    Attributes:
        width, height:        Box dimensions.
        num_particles:        Total particle count across all species.
        activation_range:     Distance within which conversion can occur.
        proximity_interval:   Number of motion steps between reaction checks.
        num_steps:            Total number of motion steps to run.
    """
    width:              float = 0.0
    height:             float = 0.0
    num_particles:      int   = 0
    activation_range:   float = 0.0
    proximity_interval: int   = 1
    num_steps:          int   = 0
