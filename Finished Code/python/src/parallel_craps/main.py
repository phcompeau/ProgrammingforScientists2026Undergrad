import time
import random
import multiprocessing

def main():
    print("Parallel programming and craps.")

    num_procs = multiprocessing.cpu_count()
    num_trials = 4000000

    # house_edge_parallel = compute_craps_house_edge_parallel(num_trials, num_procs)
    # print("House edge parallel:", house_edge_parallel)

    # house_edge_serial = compute_craps_house_edge_serial(num_trials)
    # print("House edge serial:", house_edge_serial)

    # time the parallel approach
    start_parallel = time.time()
    compute_craps_house_edge_parallel(num_trials, num_procs)
    end_parallel =time.time()
    total_parallel = end_parallel - start_parallel
    print(f"Time taken for parallel craps house edge computation of {num_trials} trials using {num_procs} processes is: {total_parallel}")

    # time the serial approach
    start_serial = time.time()
    compute_craps_house_edge_serial(num_trials)
    end_serial =time.time()
    total_serial = end_serial - start_serial
    print(f"Time taken for serial craps house edge computation of {num_trials} trials is: {total_serial}")

    print(f"Speedup provided by parallel approach: {total_serial/total_parallel}")   


def roll_die() -> int:
    """Simulate rolling a single six-sided die."""
    return random.randint(1, 6)

def sum_dice(num_dice: int) -> int:
    """Simulate rolling num_dice six-sided dice and summing the results."""
    total = 0
    for _ in range(num_dice):
        total += roll_die()
    return total

def play_craps_once() -> bool:
    """
    Simulate a single game of craps.
    Return True if player wins, False if loses.
    """
    first_roll = sum_dice(2)
    if first_roll == 7 or first_roll == 11:
        return True
    elif first_roll == 2 or first_roll == 3 or first_roll == 12:
        return False
    else:
        while True:
            next_roll = sum_dice(2)
            if next_roll == first_roll:
                return True
            elif next_roll == 7:
                return False

def compute_craps_house_edge_serial(num_trials: int) -> float:
    """
    Simulate num_trials games of craps in serial.
    """
    win_total = 0
    for _ in range(num_trials):
        if play_craps_once():
            win_total += 1
        else:
            win_total -= 1
    return win_total / num_trials

def compute_craps_house_edge_parallel(num_trials:int, num_procs: int) -> float:
    """
    Simulate num_trials trials of craps in parallel, divided over
    num_procs worker processes, and return the house edge of the game as the amount won/lost (+/-) divided by num_trials
    """
    win_total = 0

    # create my queue and processes
    result_queue = multiprocessing.Queue()
    processes: list[multiprocessing.Process] = []

    # how many trials should each worker take? (except for last)
    trials_one_proc = num_trials // num_procs

    # start first num_procs - 1 processes 
    for _ in range(num_procs-1):
        p = multiprocessing.Process(target= total_win_one_proc, args = (trials_one_proc, result_queue))
        processes.append(p)
        p.start()

    # start final process
    # extra trails are just remainder of the division 
    extra_trials = num_trials % num_procs  # in range [0, num_procs)
    trials_final_proc = trials_one_proc + extra_trials
    p = multiprocessing.Process(target= total_win_one_proc, args = (trials_final_proc, result_queue))
    processes.append(p)
    p.start()

    # now join to wait on them to finish
    for p in processes:
        p.join()

    # now, collect results 
    for _ in range(num_procs):
        win_total += result_queue.get()

    return win_total / num_trials

def total_win_one_proc(num_trials_one_proc:int, result_queue: multiprocessing.Queue) -> None:
    """
    One worker bee playing craps num_trials_one_proc times.
    It places its amount won/lost (+/-) into the input queue
    """
    win_total = 0
    for _ in range(num_trials_one_proc):
        if play_craps_once():
            win_total += 1
        else:
            win_total -= 1

    result_queue.put(win_total)


if __name__ == "__main__":
    main()
