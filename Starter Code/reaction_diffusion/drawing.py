"""
drawing.py

Render simulation frames to pygame surfaces.
"""

import pygame

from datatypes import Particle, ReactionTable, SimulationParameters


def frames_to_surfaces(frames: list[list[Particle]],
                       table: ReactionTable,
                       params: SimulationParameters,
                       drawing_frequency: int = 1) -> list[pygame.Surface]:
    """Render simulation frames to pygame surfaces, colored by species.

    A surface is produced for frames whose index is a multiple of
    drawing_frequency.

    Args:
        frames:            One particle-list snapshot per recorded step.
        table:             ReactionTable (provides species colors and background).
        params:            SimulationParameters (provides box dimensions).
        drawing_frequency: Render a frame when i % drawing_frequency == 0.

    Returns:
        One pygame.Surface per drawn frame, drawn at native box size.
    """
    canvas_width  = int(params.width)
    canvas_height = int(params.height)

    surfaces: list[pygame.Surface] = []
    for i, snapshot in enumerate(frames):
        if i % drawing_frequency == 0:
            surfaces.append(draw_frame(snapshot, table.colors,
                                       table.background_color,
                                       canvas_width, canvas_height))
    return surfaces


def draw_frame(particles: list[Particle],
               species_colors: list[tuple[int, int, int]],
               background_color: tuple[int, int, int],
               canvas_width: int,
               canvas_height: int) -> pygame.Surface:
    """Draw one frame's particles to a fresh pygame.Surface.

    Particles near an edge bleed in from the opposite edge so the torus
    topology is visually obvious.

    Args:
        particles:        The particles to draw in this frame.
        species_colors:   RGB tuple per species index.
        background_color: RGB tuple for the canvas fill.
        canvas_width:     Surface width (pixels).
        canvas_height:    Surface height (pixels).

    Returns:
        A new pygame.Surface with the background filled and every particle
        drawn as a filled circle (with edge-wrap copies as needed).
    """
    # Start from a clean canvas painted with the scenario's background color.
    surface = pygame.Surface((canvas_width, canvas_height))
    surface.fill(background_color)

    for p in particles:
        color  = species_colors[p.species]
        x      = int(p.position.x)
        y      = int(p.position.y)
        radius = int(p.radius)

        # A particle right at the edge needs an extra "ghost" copy drawn
        # on the opposite side, since the simulation box is a torus. We
        # collect the offsets we'll need along each axis -- always 0
        # (the particle's actual position), plus a wrap offset if it's
        # close to a boundary.
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

        # Draw a circle for every (x_offset, y_offset) combination -- so an
        # edge particle gets its main copy plus 1, 2, or 3 wrap copies
        # depending on which corners/sides it touches.
        for dx in x_offsets:
            for dy in y_offsets:
                pygame.draw.circle(surface, color,
                                   (x + dx, y + dy), radius)

    return surface
