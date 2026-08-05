"""
Rendering helpers for animating a Universe with pygame.

Notes:
- This module does not use the gravitational constant. Physics updates should
  reference Universe.gravitational_constant in your simulation code.
"""

import math
import pygame
import numpy as np  # only needed if you convert Surfaces to NumPy arrays
from datatypes import Body, OrderedPair, Universe

# Trail rendering parameters
TRAIL_FREQUENCY = 10
NUMBER_OF_TRAIL_FRAMES = 100
JUPITER_MOON_MULTIPLIER = 10.0
TRAIL_THICKNESS_FACTOR = 0.2


# ------------------------- Validation Helpers -------------------------

def _is_finite_number(x: float) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)

def _validate_ordered_pair(p: OrderedPair, name: str) -> None:
    if not isinstance(p, OrderedPair):
        raise TypeError(f"{name} must be an OrderedPair")
    if not _is_finite_number(p.x) or not _is_finite_number(p.y):
        raise ValueError(f"{name} must contain finite numeric components")

def _validate_color(c: int, name: str) -> None:
    if not isinstance(c, int) or not (0 <= c <= 255):
        raise ValueError(f"{name} must be an int in [0, 255]")

def _validate_body_drawable(b: Body, idx_hint: str = "") -> None:
    if not isinstance(b, Body):
        raise TypeError(f"b{idx_hint} must be a Body")
    if not _is_finite_number(b.radius) or b.radius < 0:
        raise ValueError(f"b{idx_hint}.radius must be a nonnegative finite number")
    _validate_ordered_pair(b.position, f"b{idx_hint}.position")
    _validate_color(b.red,   f"b{idx_hint}.red")
    _validate_color(b.green, f"b{idx_hint}.green")
    _validate_color(b.blue,  f"b{idx_hint}.blue")

def _validate_universe_drawable(u: Universe) -> None:
    if not isinstance(u, Universe):
        raise TypeError("u must be a Universe")
    if not isinstance(u.bodies, list):
        raise TypeError("u.bodies must be a list[Body]")
    if not _is_finite_number(u.width) or u.width <= 0:
        raise ValueError("u.width must be a positive finite number")
    for i, b in enumerate(u.bodies):
        _validate_body_drawable(b, idx_hint=f"[{i}]")

def _validate_canvas_width(canvas_width: int) -> None:
    if not isinstance(canvas_width, int) or canvas_width <= 0:
        raise ValueError("canvas_width must be an integer > 0")

def _validate_drawing_frequency(freq: int) -> None:
    if not isinstance(freq, int) or freq <= 0:
        raise ValueError("drawing_frequency must be an integer > 0")

def _validate_trails(trails: dict[int, list[OrderedPair]]) -> None:
    if not isinstance(trails, dict):
        raise TypeError("trails must be a dict[int, list[OrderedPair]]")
    for k, v in trails.items():
        if not isinstance(k, int):
            raise TypeError("trails keys must be ints (body indices)")
        if not isinstance(v, list):
            raise TypeError("trails values must be lists of OrderedPair")
        for p in v:
            _validate_ordered_pair(p, "trail point")


# ------------------------- Public API -------------------------

def animate_system(
    time_points: list[Universe],
    canvas_width: int,
    drawing_frequency: int
) -> list[pygame.Surface]:
    """
    Render selected frames of the system into pygame surfaces.

    Frames are sampled every `drawing_frequency` simulation steps; trail history
    is updated more frequently using `TRAIL_FREQUENCY` so trails look smooth.

    Args:
        time_points: Snapshots of the Universe over time (0..N).
        canvas_width: Width/height (px) of the square canvas.
        drawing_frequency: Draw a frame when i % drawing_frequency == 0.

    Returns:
        A list of pygame.Surface objects (one per drawn frame).
    """
    if not isinstance(time_points, list) or not time_points:
        raise ValueError("time_points must be a non-empty list[Universe]")
    for u in time_points:
        _validate_universe_drawable(u)
    _validate_canvas_width(canvas_width)
    _validate_drawing_frequency(drawing_frequency)

    images: list[pygame.Surface] = []
    trails: dict[int, list[OrderedPair]] = {}

    for i, u in enumerate(time_points):
        # Update trails at the configured frequency for smoother paths
        if (i * TRAIL_FREQUENCY) % drawing_frequency == 0:
            for body_index, body in enumerate(u.bodies):
                if body_index not in trails:
                    trails[body_index] = []
                trails[body_index].append(body.position)

                # Cap trail length (in frames), dropping the oldest points
                if len(trails[body_index]) > NUMBER_OF_TRAIL_FRAMES * TRAIL_FREQUENCY:
                    trails[body_index].pop(0)

        # Emit a drawable frame on schedule
        if i % drawing_frequency == 0:
            surface = draw_to_canvas(u, canvas_width, trails)
            images.append(surface)

    return images


def draw_to_canvas(
    u: Universe,
    canvas_width: int,
    trails: dict[int, list[OrderedPair]],
) -> pygame.Surface:
    """
    Draw a single Universe snapshot onto a new pygame Surface.
    """
    _validate_universe_drawable(u)
    _validate_canvas_width(canvas_width)
    _validate_trails(trails)

    surface = pygame.Surface((canvas_width, canvas_width))
    surface.fill((255, 255, 255))  # white background

    # Trails first (so bodies appear on top)
    draw_trails(surface, trails, u.width, canvas_width, u.bodies)

    # Draw bodies
    for b in u.bodies:
        color = (b.red, b.green, b.blue)
        center_x = int((b.position.x / u.width) * canvas_width)
        center_y = int((b.position.y / u.width) * canvas_width)
        radius = (b.radius / u.width) * canvas_width

        if b.name in {"Io", "Ganymede", "Callisto", "Europa"}:
            radius *= JUPITER_MOON_MULTIPLIER

        pygame.draw.circle(surface, color, (center_x, center_y), int(radius))

    return surface


def pygame_surface_to_numpy(surface: pygame.Surface) -> np.ndarray:
    """
    Convert a pygame Surface to a NumPy RGB array of shape (H, W, 3).

    This is handy for exporting frames via imageio/moviepy later.
    """
    if not isinstance(surface, pygame.Surface):
        raise TypeError("surface must be a pygame.Surface")
    arr = pygame.surfarray.array3d(surface)
    if arr.ndim != 3 or arr.shape[2] != 3:
        raise ValueError("unexpected surface format; expected (W, H, 3) RGB")
    return arr.swapaxes(0, 1)


def draw_trails(
    surface: pygame.Surface,
    trails: dict[int, list[OrderedPair]],
    u_width: float,
    canvas_width: int,
    bodies: list[Body],
) -> None:
    """
    Draw fading trails for each body onto the given surface.
    """
    if not isinstance(surface, pygame.Surface):
        raise TypeError("surface must be a pygame.Surface")
    _validate_trails(trails)
    if not _is_finite_number(u_width) or u_width <= 0:
        raise ValueError("u_width must be a positive finite number")
    _validate_canvas_width(canvas_width)
    if not isinstance(bodies, list):
        raise TypeError("bodies must be a list[Body]")

    for body_index, b in enumerate(bodies):
        _validate_body_drawable(b, idx_hint=f"[{body_index}]")
        trail = trails.get(body_index, [])
        num_trails = len(trail)

        # Line width scales with body radius
        line_width = int((b.radius / u_width) * canvas_width * TRAIL_THICKNESS_FACTOR)

        # Thicker lines for the big Jupiter moons
        if b.name in {"Ganymede", "Io", "Callisto", "Europa"}:
            line_width = int(line_width * JUPITER_MOON_MULTIPLIER)

        if line_width == 0:
            line_width = 1

        # Draw segments with a simple color fade toward the body's color
        for j in range(num_trails - 1):
            alpha = 255.0 * j / num_trails
            red = int((1 - alpha / 255.0) * 255.0 + (alpha / 255.0) * b.red)
            green = int((1 - alpha / 255.0) * 255.0 + (alpha / 255.0) * b.green)
            blue = int((1 - alpha / 255.0) * 255.0 + (alpha / 255.0) * b.blue)

            start_x = int((trail[j].x / u_width) * canvas_width)
            start_y = int((trail[j].y / u_width) * canvas_width)
            end_x = int((trail[j + 1].x / u_width) * canvas_width)
            end_y = int((trail[j + 1].y / u_width) * canvas_width)

            pygame.draw.line(
                surface, (red, green, blue),
                (start_x, start_y), (end_x, end_y), line_width
            )