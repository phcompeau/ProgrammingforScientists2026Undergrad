import random  # for generating random numbers
from election_io import read_electoral_votes, read_polling_data


def main():
    print("Let's simulate an election!")

    electoral_vote_file = "data/electoral_votes.csv"
    poll_file = "data/debates.csv"

    electoral_votes = read_electoral_votes(electoral_vote_file)
    polls = read_polling_data(poll_file)

    print("Data read!")

    # set simulation parameters
    num_trials = 1000000
    margin_of_error = 0.1

    print("Running", num_trials, "simulations.")

    probability_1, probability_2, probability_tie = simulate_multiple_elections(polls, electoral_votes, num_trials, margin_of_error)

    print("Election simulated!")

    print("Probability of candidate 1 winning:", probability_1)

    print("Probability of candidate 2 winning:", probability_2)

    print("Probability of the dreaded tie:", probability_tie)


def simulate_multiple_elections(
    polls: dict[str, float],
    electoral_votes: dict[str, int],
    num_trials: int,
    margin_of_error: float,
) -> tuple[float, float, float]:
    """
    Simulates multiple elections and calculates winning probabilities.

    Parameters:
    - polls (dict[str, float]): A dictionary of state names to polling percentages for candidate 1.
    - electoral_votes (dict[str, int]): A dictionary of state names to electoral votes.
    - num_trials (int): The number of trials to run.
    - margin_of_error (float): The margin of error in the polls.

    Returns:
    - tuple[float, float, float]: The estimated probabilities of candidate 1 winning,
      candidate 2 winning, and a tie.
    """

    if num_trials <= 0:
        raise ValueError("num_trials must be positive.")
    if margin_of_error < 0:
        raise ValueError("margin_of_error must be non-negative.")

    # keep track of number of simulations won in each of three cases;
    # what we ultimately want is the ratio of these counts to the total
    win_count_1 = 0
    win_count_2 = 0
    tie_count = 0

    # we need to run the simulations
    for _ in range(num_trials):
        # simulate one election, giving EC votes for candidate 1 and 2
        votes_1, votes_2 = simulate_one_election(polls, electoral_votes, margin_of_error)

        # who won?
        if votes_1 > votes_2:
            win_count_1 += 1
        elif votes_2 > votes_1:
            win_count_2 += 1
        else:
            # worst possible outcome, a tie!
            tie_count += 1

    probability_1 = win_count_1/num_trials
    probability_2 = win_count_2/num_trials
    probability_tie = tie_count/num_trials

    return probability_1, probability_2, probability_tie


def simulate_one_election(
    polls: dict[str, float],
    electoral_votes: dict[str, int],
    margin_of_error: float
) -> tuple[int, int]:
    """
    Simulates one election and calculates electoral college votes for each candidate.

    Parameters:
    - polls (dict[str, float]): A dictionary of state names to polling percentages for candidate 1.
    - electoral_votes (dict[str, int]): A dictionary of state names to electoral votes.
    - margin_of_error (float): The margin of error in the polls.

    Returns:
    - tuple[int, int]: The number of electoral college votes for each of the two candidates.
    """
    # basic checks
    if margin_of_error < 0:
        raise ValueError("margin_of_error must be non-negative.")

    # variables to store number of EC votes for each candidate
    college_votes_1 = 0
    college_votes_2 = 0

    # range over all states and simulate each one
    for state, polling_value in polls.items():
        # access the number of EC votes in this state
        num_votes = electoral_votes[state]

        # we need to bump the polling value in a random direction
        adjusted_poll = add_noise(polling_value, margin_of_error)

        # as a result, which candidate is simulated to have won the state?
        if adjusted_poll >= 0.5:
            # candidate 1 wins the state
            college_votes_1 += num_votes
        else:
            # candidate 2 wins the state
            college_votes_2 += num_votes

    return college_votes_1, college_votes_2


def add_noise(polling_value: float, margin_of_error: float) -> float:
    """
    Adds random noise to a polling value.

    Parameters:
    - polling_value (float): The polling value for candidate 1.
    - margin_of_error (float): The margin of error for this poll.

    Returns:
    - float: An adjusted polling value for candidate 1 after adding (subtracting) random noise.
    """
    if margin_of_error < 0 or polling_value < 0 or polling_value > 1:
        raise ValueError("Invalid polling value or margin of error.")

    # the margin of error is the value y such that there is a 95% chance of the
    # true value being in the range [polling_value - y, polling_value + y]

    # for a normal distribution, the margin of error is 2 times the standard deviation,
    # so we just generate a number with the standard deviation that we want
    st_dev = 0.5 * margin_of_error
    x = random.gauss(0, st_dev)

    # adding polling_value gives a value with a 95% chance of being in
    # [polling_value - margin_of_error, polling_value + margin_of_error]
    return polling_value + x


if __name__ == "__main__":
    main()
