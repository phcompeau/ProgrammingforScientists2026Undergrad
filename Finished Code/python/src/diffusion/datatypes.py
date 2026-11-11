"""
datatypes.py

Core data types for the random-walk diffusion simulation.

Every particle takes a random step of fixed length each tick.
No velocity, no species.
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
        radius:         Visual radius (does not affect dynamics).
        diffusion_rate: Length of each random step.
    """
    position:       OrderedPair = field(default_factory=OrderedPair)
    radius:         float       = 5.0
    diffusion_rate: float       = 1.0
