"""
drawing.py

Render simulation frames to pygame surfaces.
"""

import os
import warnings

# Suppress pygame's import-time banner. macOS multiprocessing uses spawn,
# so every worker process re-imports this module; without this, the
# banner (and pkg_resources deprecation warning from pygame/pkgdata.py)
# print once per spawn.
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import pygame

from datatypes import Particle


def frames_to_surfaces(frames: list[list[Particle]],
                       width: float,
                       height: float,
                       background_color: tuple[int, int, int],
                       particle_color: tuple[int, int, int],
                       drawing_frequency: int) -> list[pygame.Surface]:
    """Render selected simulation frames to pygame surfaces.

    A surface is produced for frames whose index is a multiple of
    drawing_frequency.

    Args:
        frames:            One particle-list snapshot per simulation step.
        width:             Box width.
        height:            Box height.
        background_color:  RGB tuple for the canvas background.
        particle_color:    RGB tuple for every particle.
        drawing_frequency: Render a frame when i % drawing_frequency == 0.

    Returns:
        One pygame.Surface per drawn frame, drawn at native box size.
    """
    canvas_width  = int(width)
    canvas_height = int(height)

    surfaces: list[pygame.Surface] = []
    for i, snapshot in enumerate(frames):
        if i % drawing_frequency == 0:
            surfaces.append(draw_frame(snapshot, canvas_width, canvas_height,
                                       background_color, particle_color))
    return surfaces


def draw_frame(particles: list[Particle],
               canvas_width: int,
               canvas_height: int,
               background_color: tuple[int, int, int],
               particle_color: tuple[int, int, int]) -> pygame.Surface:
    """Draw one frame's particles to a fresh pygame.Surface.

    Args:
        particles:        The particles to draw in this frame.
        canvas_width:     Surface width (pixels).
        canvas_height:    Surface height (pixels).
        background_color: RGB tuple for the canvas background.
        particle_color:   RGB tuple for every particle.

    Returns:
        A new pygame.Surface with the background filled and every particle
        drawn as a filled circle.
    """
    surface = pygame.Surface((canvas_width, canvas_height))
    surface.fill(background_color)

    for p in particles:
        x      = int(p.position.x)
        y      = int(p.position.y)
        radius = int(p.radius)

        # On a torus, particles near an edge should bleed in from the
        # opposite edge. Draw the circle at the base position plus, if
        # it overlaps an edge, a copy shifted by +/- canvas dimensions.
        x_offsets: list[int] = [0]
        if x - radius < 0:
            x_offsets.append(canvas_width)
        if x + radius >= canvas_width:
            x_offsets.append(-canvas_width)

        y_offsets: list[int] = [0]
        if y - radius < 0:
            y_offsets.append(canvas_height)
        if y + radius >= canvas_height:
            y_offsets.append(-canvas_height)

        for dx in x_offsets:
            for dy in y_offsets:
                pygame.draw.circle(surface, particle_color,
                                   (x + dx, y + dy), radius)

    return surface
