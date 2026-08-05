import math
import random
from datatypes import OrderedPair, Star, Universe  # Adjust this path if needed

G = 6.67408e-11  # gravitational constant
M = 8e36         # mass of black hole

# A Galaxy is just a list of Star objects
Galaxy = list[Star]


def initialize_universe(galaxies: list[Galaxy], w: float) -> Universe:
    """
    Sets up an initial universe from a list of galaxies.
    """
    stars = []
    for galaxy in galaxies:
        for star in galaxy:
            stars.append(star)

    return Universe(width=w, stars=stars)


def initialize_galaxy(num_of_stars: int, r: float, x: float, y: float) -> Galaxy:
    """
    Creates a galaxy of stars orbiting a central black hole at position (x, y).
    """
    galaxy = []

    for _ in range(num_of_stars):
        # First choose distance to center of galaxy and multiply by factor of r
        dist = (random.random() + 1.0) / 2.0 * r

        # Next choose the angle in radians to represent the rotation
        angle = random.random() * 2 * math.pi

        # convert polar coordinates to Cartesian
        pos_x = x + dist * math.cos(angle)
        pos_y = y + dist * math.sin(angle)
        position = OrderedPair(pos_x, pos_y)

        # orbital velocity approximation
        speed = math.sqrt(G * M / dist)
        vel_x = speed * math.cos(angle + math.pi / 2)
        vel_y = speed * math.sin(angle + math.pi / 2)
        velocity = OrderedPair(vel_x, vel_y)

        # create star
        star = Star(
            position=position,
            velocity=velocity,
            acceleration=OrderedPair(0, 0),
            mass=1.989e30,       # set the mass = mass of sun by default
            radius=696340000,    # set the radius equal to radius of sun in m
            red=255,
            green=255,
            blue=255
        )

        galaxy.append(star)

    # Add black hole to the center of the galaxy
    blackhole = Star(
        position=OrderedPair(x, y),
        velocity=OrderedPair(0, 0),
        acceleration=OrderedPair(0, 0),
        mass=M,
        radius=6963400000,
        red=0,
        green=0,
        blue=255
    )

    galaxy.append(blackhole)
    return galaxy


def push(galaxy: Galaxy, v: OrderedPair) -> None:
    """
    Adds velocity vector `v` to every star in the galaxy.
    """
    for star in galaxy:
        star.velocity = OrderedPair(star.velocity.x + v.x, star.velocity.y + v.y)