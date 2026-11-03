import time
import multiprocessing

from serial import compute_craps_house_edge_serial
from parallel import compute_craps_house_edge_parallel


def main() -> None:
    print("Parallel programming and craps.")

    num_procs = multiprocessing.cpu_count()
    num_trials = 1000

    # time the parallel approach
    start_parallel = time.time()
    compute_craps_house_edge_parallel(num_trials, num_procs)
    end_parallel = time.time()
    total_parallel = end_parallel - start_parallel
    print(f"Time taken for parallel craps house edge computation of {num_trials} trials using {num_procs} processes is: {total_parallel}")

    # time the serial approach
    start_serial = time.time()
    compute_craps_house_edge_serial(num_trials)
    end_serial = time.time()
    total_serial = end_serial - start_serial
    print(f"Time taken for serial craps house edge computation of {num_trials} trials is: {total_serial}")

    print(f"Speedup provided by parallel approach: {total_serial / total_parallel}")


if __name__ == "__main__":
    main()
