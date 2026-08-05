class Cell:
    """
    Represents a single site in the spatial Prisoner's Dilemma grid.
    - strategy: either "C" (cooperate) or "D" (defect)
    - score: floating-point payoff accumulated from interactions
    """
    def __init__(self, strategy, score=0.0):
        self.strategy = strategy
        self.score = score

# A GameBoard is simply a 2D grid (list of lists) of Cell objects.
# Example: game_board[row][col]
GameBoard = list