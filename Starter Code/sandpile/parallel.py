from datatypes import Board
import multiprocessing
from serial import (
    number_of_coins_in,
    number_of_coins_out,
    make_empty_board,
    deep_copy_board
)
from helper_functions import num_rows, num_cols

def simulate_sandpiles_parallel(current_board: Board,
                                num_procs: int | None = None) -> list[Board]:
    #TODO: implement
    pass

def is_converged_multi_procs(b: Board, num_procs: int) -> bool:
    #TODO: implement
    pass

def update_multi_procs(b: Board, num_procs: int) -> Board:
    #TODO: implement
    pass


def update_subboard_single_proc(b: Board,
                   row_start: int,
                   row_end: int,
                   result_queue: multiprocessing.Queue) -> None:
    #TODO: implement
    pass


def make_row_chunks(total_rows: int, num_procs: int) -> list[tuple[int, int]]:
    #TODO: implement
    pass