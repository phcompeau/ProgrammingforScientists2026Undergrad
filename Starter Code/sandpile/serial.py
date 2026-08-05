import random
from datatypes import Board
from helper_functions import contains, deep_copy_board, num_cols, num_rows, make_empty_board

def create_board(r: int,
                 c: int,
                 pile: int,
                 center: bool = True,
                 num_piles: int = 1) -> Board:
    """Create an r x c board and place grains either centrally or randomly.

    Args:
        r: Number of rows.
        c: Number of columns.
        pile: Number of grains (must be positive).
        center: If True, place all grains at center. If False, use random placement.
        num_piles: When center=False, number of random cells receiving pile/num_piles grains.

    Returns:
        A board with grains placed according to the mode selected.
    """
    if pile <= 0:
        raise ValueError("Error: stack size must be positive.")

    if not center and num_piles <= 0:
        raise ValueError("Error: num_piles must be positive for random placement.")

    # Start with an empty board
    b = make_empty_board(r, c)

    if center:
        # Place all grains in the center cell
        center_row = r // 2
        center_col = c // 2
        b[center_row][center_col] = pile
        return b

    # Otherwise: random placement across num_piles random locations
    grains_per_pile = pile // num_piles

    for _ in range(num_piles):
        row = random.randrange(r)
        col = random.randrange(c)
        b[row][col] = grains_per_pile

    return b

def simulate_sandpiles(initial_board: Board) -> list[Board]:
    #TODO: implement
    pass


def is_converged(b: Board) -> bool:
    #TODO: implement
    pass


def update(b: Board) -> Board:
    #TODO: implement
    pass


def number_of_coins_out(b: Board, r: int, c: int) -> int:
    #TODO: implement
    pass


def number_of_coins_in(b: Board, r: int, c: int) -> int:
    #TODO: implement
    pass

