from dataclasses import dataclass
import math

G = 6.67408e-11  # gravitational constant (you can scale this for visualization)

@dataclass
class OrderedPair:
    """
    A simple 2-D point or vector with named coordinates.

    Used to represent positions, velocities, and accelerations of stars
    in the simulation. Supports access via `.x` and `.y` for readability.
    """
    x: float = 0.0
    y: float = 0.0

@dataclass
class Star:
    """
    A celestial body in the simulation.

    Each Star has a position, velocity, acceleration, mass, and radius,
    along with optional RGB color values for visualization.
    The position and motion are expressed as 2D vectors (x, y).
    """
    position: OrderedPair | None = None
    velocity: OrderedPair | None = None
    acceleration: OrderedPair | None = None
    mass: float = 0.0
    radius: float = 0.0
    red: int = 255
    green: int = 255
    blue: int = 255


@dataclass
class Universe:
    """
    A square universe of given width containing a list of stars.

    The universe defines the simulation space. Its width represents the
    side length of a square region with corners at (0, 0) and (width, width).
    """
    width: float = 0.0
    stars: list[Star] = None

    def in_field(self, p: OrderedPair) -> bool:
        """
        Check if a given point is within the bounds of the universe.
        """
        return 0 <= p.x <= self.width and 0 <= p.y <= self.width


@dataclass
class Quadrant:
    """
    A square subregion of the universe given by its lower-left corner (x, y) and width.
    """
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0


@dataclass
class Node:
    """
    A quadtree node. Internal nodes store a dummy 'star' for the center of mass and have children.
    Leaf nodes may store a real star (or be empty) and have no children.
    By convention, child quadrants are ordered [NW, NE, SW, SE].
    """
    sector: Quadrant | None = None
    children: list["Node"] | None = None
    star: Star | None = None

    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf (i.e., is child-free).
        """
        return self.children is None or len(self.children) == 0

    def insert(self, s: Star) -> None:
        # TODO: implement
        pass

    def create_children(self) -> None:
        # TODO: implement
        pass

    # find_child determines the correct quadrant child a star belongs to
    # and returns that child node.
    def find_child(self, s: Star) -> 'Node':
        # TODO: implement
        pass

    def calculate_net_force(self, s: Star, theta: float) -> OrderedPair:
        # TODO: implement
        pass

@dataclass
class QuadTree:
    """
    A wrapper around the root node of a Barnes–Hut quadtree.

    Provides an interface for inserting stars, building the spatial tree,
    and calculating net gravitational forces using hierarchical aggregation.
    """
    root: Node | None = None

    def insert(self, s: Star) -> None:
        self.root.insert(s)

# To prevent circular import issues, we define these functions here.

def center_of_gravity(*stars: Star) -> OrderedPair:
    # TODO: implement
    pass


def compute_force(s1: Star, s2: Star) -> OrderedPair:
    """
    Compute the gravitational force exerted by s1 on s2.
    Uses Newton's law of universal gravitation.
    𝐹 = G * (m1 * m2) / r²
    """
    d = distance(s1.position, s2.position)
    F = G * s1.mass * s2.mass / (d * d)  
    
    delta = (s1.position.x - s2.position.x, s1.position.y - s2.position.y)
    force = OrderedPair(F * (delta[0] / d), F * (delta[1] / d))
    return force


def distance(p1: OrderedPair, p2: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points.
    """
    dx, dy = (p1.x - p2.x, p1.y - p2.y)
    return math.sqrt(dx * dx + dy * dy)