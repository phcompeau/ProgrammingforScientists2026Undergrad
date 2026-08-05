import time
import random
from multiprocessing import Process, Queue, cpu_count

def main():
    print("Parallel programming and craps.")

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


if __name__ == "__main__":
    main()
