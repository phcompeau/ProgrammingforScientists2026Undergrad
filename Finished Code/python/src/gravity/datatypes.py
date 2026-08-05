class OrderedPair:
    """
    Represents a 2D vector or coordinate pair (x, y).

    Attributes:
        x: The x-coordinate or horizontal component (float).
        y: The y-coordinate or vertical component (float).
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x: float = x
        self.y: float = y


class Body:
    """
    Represents a celestial body within the simulation universe.

    Attributes:
        name: The name of the body (e.g., "Earth", "Sun").
        mass: Mass of the body.
        radius: Radius of the body (used for drawing and collision distance).
        position: Current position as an OrderedPair.
        velocity: Current velocity as an OrderedPair.
        acceleration: Current acceleration as an OrderedPair.
        red: Red component of the display color (0–255).
        green: Green component of the display color (0–255).
        blue: Blue component of the display color (0–255).
    """

    def __init__(
        self,
        name: str,
        mass: float,
        radius: float,
        position: OrderedPair,
        velocity: OrderedPair,
        acceleration: OrderedPair,
        red: int,
        green: int,
        blue: int
    ):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.red = red
        self.green = green
        self.blue = blue


class Universe:
    """
    Represents the entire simulation environment.

    Attributes:
        bodies: A list of Body objects in the universe.
        width: The width of the simulation space (assumed square).
        gravitational_constant (class attribute): The gravitational constant (G)
            shared by all Universe instances.

    Class Attributes:
        gravitational_constant: float — default value can be set globally.
    """

    gravitational_constant: float = 6.674e-11  # Default; can be overridden

    def __init__(self, bodies: list[Body], width: float):
        """
        Initialize a new Universe instance.

        Args:
            bodies: List of Body objects in the simulation.
            width: Width of the universe (used for scaling when drawing).
        """
        self.bodies = bodies
        self.width = width