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

# Three functions that we covered:
# 1. generate random integer (Python doesn't have support for this)
# 2. generate random integer in a range [0, n)
# 3. generate float in the range [0, 1)

import random # allows pseudorandom number generation

import time 

def main():
    print("Rolling dice and playing craps.")

    num_trials = 10000000 

    edge = compute_craps_house_edge(num_trials) # average amount won/lost per trial 

    print(f"Estimated house edge with {num_trials} trials is: {edge:.6f}")

    # initial_stuff()


def initial_stuff():
    # random.seed(0) # this was the default for some of the history of Python

    # this was useful for testing!

    # random.seed(time.time_ns()) # seed based off time in nanoseconds

    # this happens behind the scenes automatically

    print("Random int", random.randrange(0, 10)) # prints number between 0 and 9, inclusively

    print("Random number in [0, 1)", random.random()) # prints number in [0, 1)

    print("Random int", random.randrange(0, 10)) # prints number between 0 and 9, inclusively

    print("Random number in [0, 1)", random.random()) # prints number in [0, 1)

    for _ in range(10):
        # ten die rolls 
        print("Die roll:", roll_die())

    for _ in range(10):
        print("Rolling two dice gives:", sum_dice(2))



def roll_die() -> int:
    """
    Simulates the roll of a die.
    Returns:
    - int: A pseudorandom integer between 1 and 6, inclusively.
    """
    return random.randrange(1, 7)

"""
This is math. Math is hard!
def sum_two_dice() -> int:
    num = random.random() 
    # num is between 0 and 1 
    if num < 1.0/36.0:
        return 2 
    elif num < 3.0/36.0: # [1/36, 3/36)
        return 3
    elif num < 6.0/36.0: 
        return 4 
"""

def sum_two_dice() -> int:
    return roll_die() + roll_die()

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
    
    total = 0

    for _ in range(num_dice):
        total += roll_die()

    return total

"""
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
"""

def play_craps_once() -> bool:
    """
    Simulates one game of craps.
    Returns:
    - bool: True if the game is a win, False if it's a loss.
    """
    first_roll = sum_dice(2)
    # did we win?
    if first_roll == 7 or first_roll == 11:
        # yes!
        return True
    elif first_roll == 2 or first_roll == 3 or first_roll == 12:
        #lost
        return False 
    else:
        # first_roll is your winner, 7 is a loser 
        while True: #forever
            new_roll = sum_dice(2)
            # is the new_roll 7 or previous roll's value?
            if new_roll == first_roll:
                # won!
                return True 
            elif new_roll == 7:
                # lost :(
                return False
            # else keep rolling


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
    
    count = 0 # winnings/losings 

    # run n trials of the game and keep track of winnings
    for _ in range(num_trials):
        outcome = play_craps_once() # True or False 
        if outcome: # win!
            count += 1
        else: # loss
            count -= 1

    return count/num_trials #averages outcome over all trials


if __name__ == "__main__":
    main()
