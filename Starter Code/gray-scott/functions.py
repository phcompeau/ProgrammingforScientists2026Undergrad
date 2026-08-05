from datatypes import Board


def initialize_board(num_rows: int, num_cols: int) -> Board:
    return [[(0.0, 0.0) for _ in range(num_cols)] for _ in range(num_rows)]


# Insert your simulate_gray_scott() function here, along with any subroutines that you need.
