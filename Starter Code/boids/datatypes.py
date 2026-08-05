class OrderedPair:
    """
    Represents a point or vector in two-dimensional space.

    Attributes:
        x (float): The x-coordinate of the point or vector.
        y (float): The y-coordinate of the point or vector.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y


class Boid:
    """
    Represents our "bird" object.

    Each Boid has position, velocity, and acceleration, each represented by
    an OrderedPair instance.

    Attributes:
        position (OrderedPair): The current position of the boid.
        velocity (OrderedPair): The current velocity of the boid.
        acceleration (OrderedPair): The current acceleration of the boid.
    """

    def __init__(self, position: OrderedPair, velocity: OrderedPair, acceleration: OrderedPair):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration


class Sky:
    """
    Represents a single time point of the simulation.

    The Sky defines the simulation parameters such as spatial boundaries, speed limits,
    and behavioral factors influencing boid interactions (separation, alignment, cohesion).

    Attributes:
        width (float): The boundary width of the simulation space.
        boids (list[Boid]): A list of Boid objects within the sky.
        max_boid_speed (float): The maximum allowed speed for any boid.
        proximity (float): The distance threshold within which boids influence each other.
        separation_factor (float): The weighting factor for the separation behavior.
        alignment_factor (float): The weighting factor for the alignment behavior.
        cohesion_factor (float): The weighting factor for the cohesion behavior.
    """
    def __init__(
        self,
        width: float = 0.0,
        boids: list[Boid] = None,
        max_boid_speed: float = 0.0,
        proximity: float = 0.0,
        separation_factor: float = 0.0,
        alignment_factor: float = 0.0,
        cohesion_factor: float = 0.0,
    ):
        self.width = width
        self.boids = boids if boids is not None else []
        self.max_boid_speed = max_boid_speed
        self.proximity = proximity
        self.separation_factor = separation_factor
        self.alignment_factor = alignment_factor
        self.cohesion_factor = cohesion_factor

