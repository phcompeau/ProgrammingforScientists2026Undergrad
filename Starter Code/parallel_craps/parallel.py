"""
parallel.py

Parallel craps simulation using multiprocessing.Process + Queue.

Divide num_trials evenly across num_procs worker processes, run
play_craps_once in each, and combine the per-worker totals to get the
house edge.
"""

import multiprocessing

from serial import play_craps_once


def compute_craps_house_edge_parallel(num_trials: int, num_procs: int) -> float:
    """
    Simulate num_trials trials of craps in parallel, divided over
    num_procs worker processes, and return the house edge of the game
    as the amount won/lost (+/-) divided by num_trials.
    """
    pass


def total_win_one_proc(num_trials_one_proc: int,
                       result_queue: multiprocessing.Queue) -> None:
    """
    One worker bee playing craps num_trials_one_proc times.
    It places its amount won/lost (+/-) into the input queue.
    """
    pass
