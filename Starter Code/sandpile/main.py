import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1") # hide pygame support prompt
import sys
import time
import imageio
import pygame

from serial import create_board, simulate_sandpiles
from parallel import simulate_sandpiles_parallel
from drawing import animate_boards, animate_boards_parallel


def main() -> None:
    """CLI Call:
        python3 main.py <board_width> <num_coins> <random|central> <cell_width>
        try python3 main.py 50 4000 central 10 
        try python3 main.py 300 20000 central 4 # comment serial out
    """


if __name__ == "__main__":
    main()
