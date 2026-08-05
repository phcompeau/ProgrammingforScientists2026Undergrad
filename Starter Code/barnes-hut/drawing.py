import pygame
from datatypes import Universe
from engine import barnes_hut_stream


def animate_system(
    time_points: list[Universe],
    canvas_width: int,
    frequency: int,
    scaling_factor: float
) -> list[pygame.Surface]:
    """
    Takes a list of Universe objects and returns a list of Pygame surfaces.
    Every `frequency` steps, it draws the universe on a square canvas.
    """
    images = []

    # For every universe, draw to canvas and grab the image
    for i, universe in enumerate(time_points):
        if i % frequency == 0:
            img = draw_to_canvas(universe, canvas_width, scaling_factor)
            images.append(img)

    return images

import pygame

def draw_to_canvas(universe, canvas_width: int, scaling_factor: float) -> pygame.Surface:
    """
    Draw the universe's stars on a Pygame surface and return the surface.
    The canvas is square (canvas_width x canvas_width).
    """
    surface = pygame.Surface((canvas_width, canvas_width))
    surface.fill((0, 0, 0))  # fill background with black

    if universe.stars is None:
        return surface

    for star in universe.stars:
        color = (star.red, star.green, star.blue)
        cx = int((star.position.x / universe.width) * canvas_width)
        cy = int((star.position.y / universe.width) * canvas_width)
        r = max(1, int(scaling_factor * (star.radius / universe.width) * canvas_width))
        pygame.draw.circle(surface, color, (cx, cy), r)

    return surface