class OrderedPair:
    """
    Represents a 2D vector or coordinate pair (x, y).

    Attributes:
        x: The x-coordinate or horizontal component (float).
        y: The y-coordinate or vertical component (float).
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        if not isinstance(x, (int, float)):
            raise TypeError(f"x must be a number (int or float), got {type(x).__name__}")
        if not isinstance(y, (int, float)):
            raise TypeError(f"y must be a number (int or float), got {type(y).__name__}")
        self.x: float = float(x)
        self.y: float = float(y)

    def __repr__(self):
        return f"OrderedPair({self.x}, {self.y})"

class Body:
    """
    Represents a celestial body within the simulation universe.
    """

    def __init__(
        self,
        name: str = "Unnamed",
        mass: float = 1.0,
        radius: float = 1.0,
        position: OrderedPair = None,
        velocity: OrderedPair = None,
        acceleration: OrderedPair = None,
        red: int = 255,
        green: int = 255,
        blue: int = 255,
    ):
        # Name
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Body name must be a non-empty string.")

        # Physical properties
        if not isinstance(mass, (int, float)) or mass <= 0:
            raise ValueError(f"Mass must be a positive number, got {mass}")
        if not isinstance(radius, (int, float)) or radius < 0:
            raise ValueError(f"Radius must be a non-negative number, got {radius}")

        # Vectors
        for arg, label in ((position, "position"), (velocity, "velocity"), (acceleration, "acceleration")):
            if not isinstance(arg, OrderedPair):
                raise TypeError(f"{label} must be an OrderedPair, got {type(arg).__name__}")

        # Color
        for c, channel in ((red, "red"), (green, "green"), (blue, "blue")):
            if not isinstance(c, int):
                raise TypeError(f"Color component {channel} must be int, got {type(c).__name__}")
            if not (0 <= c <= 255):
                raise ValueError(f"Color component {channel} must be in range [0, 255], got {c}")

        self.name = name
        self.mass = float(mass)
        self.radius = float(radius)
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Body(name={self.name}, mass={self.mass}, radius={self.radius})"

class Universe:
    """
    Represents the entire simulation environment.
    """

    gravitational_constant: float = 6.674e-11  # Default; can be overridden

    def __init__(self, bodies: list[Body], width: float = 1000.0):
        if not isinstance(bodies, list) or not all(isinstance(b, Body) for b in bodies):
            raise TypeError("bodies must be a list of Body objects.")
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError(f"width must be a positive number, got {width}")

        self.bodies = bodies
        self.width = float(width)

    def __repr__(self):
        return f"Universe(n_bodies={len(self.bodies)}, width={self.width})"