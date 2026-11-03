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
    # 1. create a queue to store our results
    # 2. initialize our worker processes
    # 3. start the processes, which will put their return values into the queue
    # 4. range over all processes and "join" them (wait until all are finished before continuing)
    # 5. grab all results from the queue and combine

    # win_total stores total amount won/lost over all workers
    win_total = 0

    # create our queue and an empty collection of processes
    result_queue = multiprocessing.Queue()
    processes = []

    # how many trials should each worker be given?
    trials_one_proc = num_trials // num_procs

    # be careful: num_trials = 1003, num_procs = 10
    # trials_one_proc = 1003 // 10 = 100
    # final worker should get 3 extra trials

    # start first num_procs - 1 workers
    for _ in range(num_procs - 1):
        p = multiprocessing.Process(target=total_win_one_proc, args=(trials_one_proc, result_queue))
        processes.append(p)
        p.start()

    # start final worker's job too
    # how many extra trials does the final worker get?
    extra_trials = num_trials % num_procs
    trials_final_proc = trials_one_proc + extra_trials
    p = multiprocessing.Process(target=total_win_one_proc, args=(trials_final_proc, result_queue))
    processes.append(p)
    p.start()

    # we need to wait on all the workers to finish
    for p in processes:
        p.join()
        # two ways of thinking of this:
        # 1. every time through the loop, the current process will not allow the code to continue executing unless this process has finished
        # 2. these two lines of code wait for every worker to finish

    # collect results from queue
    # each worker is "reporting back" with amount won/lost
    for _ in range(num_procs):
        win_total += result_queue.get()

    return win_total / num_trials


def total_win_one_proc(num_trials_one_proc: int,
                       result_queue: multiprocessing.Queue) -> None:
    """
    One worker bee playing craps num_trials_one_proc times.
    It places its amount won/lost (+/-) into the input queue.
    """
    win_total = 0

    # range over the number of trials this worker gets, and simulate the game each time, adding in the result to win_total
    for _ in range(num_trials_one_proc):
        if play_craps_once():
            # win!
            win_total += 1
        else:
            # lost :(
            win_total -= 1

    result_queue.put(win_total)
