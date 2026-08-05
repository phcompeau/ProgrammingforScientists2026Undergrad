import pygame
import numpy as np
from datatypes import OrderedPair, Boid, Sky


def animate_system(time_points: list[Sky], canvas_width: int, drawing_frequency: int) -> list[np.ndarray]:
    """
    Create a list of rendered frames for every drawing_frequency-th Sky state.
    Each frame is drawn using pygame and returned as a NumPy array (H, W, 3).
    """
    images: list[np.ndarray] = []

    for i, sky in enumerate(time_points):
        if i % drawing_frequency == 0:
            frame = draw_to_canvas(sky, canvas_width)
            images.append(frame)

    return images


def draw_to_canvas(sky: Sky, canvas_width: int) -> np.ndarray:
    """
    Draw a single frame of the sky (set of boids) onto an offscreen pygame surface
    and return it as a NumPy array suitable for video export.
    """
    surface = pygame.Surface((canvas_width, canvas_width))

    # Set background color (light blue)
    surface.fill((173, 216, 230))

    # Draw all boids as triangles
    for b in sky.boids:
        draw_boid(surface, b, sky.width, canvas_width)

    # Convert to NumPy array (swap axes for imageio compatibility)
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)


def draw_boid(surface: pygame.Surface, boid: Boid, sky_width: float, canvas_width: int) -> None:
    """
    Draw a single boid as a triangle oriented in the direction of its velocity.
    The shape and orientation match the Go version's ComputeTrianglePoints.
    """
    # Compute direction angle
    direction = np.arctan2(boid.velocity.y, boid.velocity.x)

    # Compute triangle points (mirrors Go ComputeTrianglePoints)
    point1 = OrderedPair(
        boid.position.x + 80 * np.cos(direction),
        boid.position.y + 80 * np.sin(direction),
    )
    point2 = OrderedPair(
        boid.position.x + 30 * np.cos(direction + 2 * np.pi / 3),
        boid.position.y + 30 * np.sin(direction + 2 * np.pi / 3),
    )
    point3 = OrderedPair(
        boid.position.x + 30 * np.cos(direction + 4 * np.pi / 3),
        boid.position.y + 30 * np.sin(direction + 4 * np.pi / 3),
    )

    # Scale coordinates to canvas space
    def scale(p: OrderedPair):
        return int((p.x / sky_width) * canvas_width), int((p.y / sky_width) * canvas_width)

    p1 = scale(point1)
    p2 = scale(point2)
    p3 = scale(point3)

    # Draw filled triangle (white)
    pygame.draw.polygon(surface, (255, 255, 255), [p1, p2, p3])

    # Draw black outline
    pygame.draw.polygon(surface, (0, 0, 0), [p1, p2, p3], width=1)