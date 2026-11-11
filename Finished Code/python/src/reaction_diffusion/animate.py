"""
animate.py

Convert a sequence of pygame surfaces into an MP4 video.
"""

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
    # Open an MP4 writer with libx264 (good quality + nearly universal
    # playback support) and feed each surface through the converter into
    # the writer one frame at a time.
    writer = imageio.get_writer(video_path, fps=fps, codec="libx264", quality=8)

    for surface in surfaces:
        writer.append_data(pygame_surface_to_numpy(surface))

    writer.close()
    print(f"  Animation written to {video_path}  "
          f"({len(surfaces)} frames @ {fps} fps)")


def pygame_surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """Convert a pygame.Surface to a NumPy RGB array.

    Args:
        surface: The pygame surface to convert.

    Returns:
        numpy.ndarray of shape (height, width, 3), dtype uint8.
    """
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)
