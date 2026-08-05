import random  # for generating random numbers
# import election_io
# let's import specific functions from election_io
from election_io import read_electoral_votes, read_polling_data

# final way: import all functions from package
# from election_io import *

# also should import functions from election_io.py

def main():
     print("Let's simulate an election!")

     electoral_vote_file = "data/electoralVotes.csv"

     polling_file = "data/debates.csv"

     electoral_votes = read_electoral_votes(electoral_vote_file)
     polling_data = read_polling_data(polling_file)

     print("Data read!")

     print("Simulating the election!")

     num_trials = 1000000
     margin_of_error = 0.1

     print("Running", num_trials, "simulations.")

     probability_1, probability_2, probability_tie = simulate_multiple_elections(polling_data, electoral_votes, num_trials, margin_of_error)

     print("Election simulated!")

     print("Probability of candidate 1 winning:", probability_1)

     print("Probability of candidate 2 winning:", probability_2)

     print("Probability of tie :( ):", probability_tie)






"""
SimulateMultipleElections(pollingData, numTrials, marginOfError)
    winCount1 ← 0
    winCount2 ← 0
    tieCount ← 0
    for numTrials total trials
        votes1,votes2 ← SimulateOneElection(pollingData, marginOfError)
        if votes1 > votes2
            winCount1 ← winCount1 + 1
        else if votes2 > votes1
            winCount2 ← winCount2 + 1
        else (tie!)
            tieCount ← tieCount + 1
    probability1 ← winCount1/numTrials
    probability2 ← winCount2/numTrials
    probabilityTie ← tieCount/numTrials
    return probability1, probability2, probabilityTie
"""

def simulate_multiple_elections(polls: dict[str, float], electoral_votes: dict[str, int], num_trials: int, margin_of_error: float) -> tuple[float, float, float]:
    """
    Simulates election multiple times, calculating winning "probabilities".

    Parameters:
    - polls: maps state names to candidate 1 percentages
    - electoral_votes: maps state names to electoral college votes 
    - num_trials: number of trials to simulate 
    - margin_of_error: margin of error of each poll

    Returns:
    - tuple of 3 floats corresponding to percentages of simulations won by candidate 1, candidate 2, and a tie
    """

    if num_trials <= 0:
         raise ValueError("Number of trials must be positive.")
    if margin_of_error < 0:
         raise ValueError("Margin of error must be non-negative.")

    # keep track of number of simulations won in each of three cases
    win_count_1 = 0
    win_count_2 = 0
    tie_count = 0

    # simulations go here

    for _ in range(num_trials):
        # simulate one election, giving EC votes for candidate 1 and 2
        votes_1, votes_2 = simulate_one_election(polls, electoral_votes, margin_of_error)
        # who won? 
        if votes_1 > votes_2:
           win_count_1 += 1 # candidate 1 
        elif votes_2 > votes_1:
             win_count_2 += 1 # candidate 2
        else:
             # worst possible outcome, tie! 
             tie_count += 1

    probability_1 = win_count_1/num_trials 
    probability_2 = win_count_2/num_trials 
    probability_tie = tie_count/num_trials 

    return probability_1, probability_2, probability_tie

def simulate_one_election(polls: dict[str, float], electoral_votes: dict[str, int], margin_of_error: float) -> tuple[int, int]:
    """
    Simulates one presidential election between two candidates using polling data and a given margin of error, and returns the # of electoral college votes for each candidate.

    Parameters:
    - polls: maps state names to candidate 1 percentages
    - electoral_votes: maps state names to electoral college votes 
    - margin_of_error: margin of error of each poll
    
    Returns:
    - tuple of 2 integers corresponding to # of EC votes for candidate 1 and candidate 2, respectively, after one simulation
    """

    if margin_of_error < 0:
         raise ValueError("MOE can't be negative.")
    
    # etc.
    
    # variables to store number of EC votes for each candidate 
    college_votes_1 = 0
    college_votes_2 = 0
    
    # range over all of the states (keys of either polls or electoral_votes), and simulate an election in each one 
    for state_name, polling_value in polls.items():
         # we also need to know how many votes this state is worth 
         num_votes = electoral_votes[state_name]

         # we need to bump the polling value in a random direction 
         adjusted_polling_value = add_noise(polling_value, margin_of_error)

         # based on who won, we add num_votes to their tally

         if adjusted_polling_value > 0.5:
              # candidate 1 wins!
              college_votes_1 += num_votes 
         else:
              # candidate 2 wins!
              college_votes_2 += num_votes

    return college_votes_1, college_votes_2

def add_noise(polling_value: float, margin_of_error: float) -> float:
     """
     Adds random noise to a polling value.

     Parameters:
     - polling_value (float): The polling value for candidate 1.
     - margin_of_error (float): The margin of error for this poll.

     Returns:
     - float: The adjusted polling value after assigning some noise for candidate 1 with the given margin of error.
     """

     """
     Approach 1 
     # grab a number from the standard normal 
     x = random.gauss(0, 1)

     # for a standard normal, the margin of error is 2 x the standard_deviation

     # what we wanted to generate is something with a standard deviation of margin_of_error/2

     x /= 2.0 # now the standard deviation is 0.5, and MOE is 1

     # now multiply it by margin_of_error 
     x *= margin_of_error # now the standard dev is 0.5 * MOE, and the margin of error is MOE :)

     polling_value += x

     return polling_value
     """

     # Approach 2: just generate a number with standard deviation you want 
     st_dev = 0.5 * margin_of_error
     x = random.gauss(0, st_dev)

     return polling_value + x


if __name__ == "__main__":
    main()