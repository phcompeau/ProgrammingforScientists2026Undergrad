# Cell contains two attributes corresponding to
# the concentration of prey (0-th element) and predator (1-st element) in the cell
Cell = tuple[float, float]

# Board is a two-dimensional slice of Cells
Board = list[list[Cell]]
