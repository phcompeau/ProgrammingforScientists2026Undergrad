"""
Pseudocode (from Learning Objectives)

RollDie()
    roll ← RandIntn(6)
    return roll + 1

PlayCrapsOnce()
    numDice ← 2
    firstRoll ← SumDice(numDice)
    if firstRoll = 2, 3, or 12
        return false (player loses)
    else if firstRoll = 7 or 11
        return true (player wins)
    else
        while true
            newRoll ← SumDice(numDice)
            if newRoll = firstRoll 
               return true
            else if newRoll = 7
                return false

ComputeCrapsHouseEdge(numTrials)
    count ← 0
    for numTrials total trials
        outcome ← PlayCrapsOnce()
        if outcome = true
            count ← count + 1
        else
            count ← count − 1
    return count/numTrials

Built-in PRNG references
- RandIntn(n)  → Python: random.randrange(a, b) returns integer in [a, b-1]
- RandFloat()  → Python: random.random() returns float in [0, 1)
"""

import random


def roll_die() -> int:
    """
    Simulates the roll of a die.
    Returns:
    - int: A pseudorandom integer between 1 and 6, inclusively.
    """
    # TODO: Implement this function
    pass


def sum_dice(num_dice: int) -> int:
    """
    Simulates the process of summing n dice.
    Parameters:
    - num_dice (int): The number of dice to sum.
    Returns:
    - int: The sum of num_dice simulated dice.
    """
    if num_dice <= 0:
        raise ValueError("num_dice must be a positive integer.")
    # TODO: Implement this function
    pass


def play_craps_once() -> bool:
    """
    Simulates one game of craps.
    Returns:
    - bool: True if the game is a win, False if it's a loss.
    """
    # TODO: Implement this function
    pass


def compute_craps_house_edge(num_trials: int) -> float:
    """
    Estimates the "house edge" of craps over multiple simulations.
    Parameters:
    - num_trials (int): The number of simulations.
    Returns:
    - float: The house edge of craps (average amount won or lost per game, per unit bet).
    Positive means player profit; negative means house profit.
    """
    if num_trials <= 0:
        raise ValueError("num_trials must be a positive integer.")
    # TODO: Implement this function
    pass



def main():
    print("Rolling dice and playing craps.")


if __name__ == "__main__":
    main()
