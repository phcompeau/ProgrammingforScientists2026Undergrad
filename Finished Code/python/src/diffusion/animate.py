"""
animate.py

Convert a sequence of pygame surfaces into an MP4 video.
"""

import os
import warnings
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")

import imageio
import numpy
import pygame


def animate_surfaces(surfaces: list[pygame.Surface],
                     video_path: str,
                     fps: int = 30) -> None:
    """Encode pygame surfaces as an MP4.

    Args:
        surfaces:   One pygame.Surface per video frame.
        video_path: Output MP4 path.
        fps:        Video frame rate.
    """
    writer = imageio.get_writer(video_path, fps=fps, codec="libx264", quality=8)

    for surface in surfaces:
        writer.append_data(surface_to_numpy(surface))

    writer.close()
    print(f"  Animation written to {video_path}  "
          f"({len(surfaces)} frames @ {fps} fps)")


def surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """Convert a pygame.Surface to a NumPy RGB array.

    Args:
        surface: The pygame surface to convert.

    Returns:
        numpy.ndarray of shape (height, width, 3), dtype uint8.
    """
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)
