from datatypes import Cell

def count_rows(board: list[list[Cell]]) -> int:
    """
    Count the number of rows in a board.
    """
    if not isinstance(board, list):
        raise ValueError("board must be a list")
    return len(board)

def assert_rectangular(board: list[list[Cell]]) -> None:
    """
    Ensure that the board is rectangular (all rows same length).
    Raises ValueError if not.
    """
    if not isinstance(board, list) or len(board) == 0 or not isinstance(board[0], list):
        raise ValueError("board must be a non-empty 2D list.")

    first_len = len(board[0])
    for row in board[1:]:
        if len(row) != first_len:
            raise ValueError("Error: GameBoard is not rectangular.")


def count_cols(board: list[list[Cell]]) -> int:
    """
    Count the number of columns in a board.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    assert_rectangular(board)
    return len(board[0])


def game_between(c1: Cell, c2: Cell, b: float) -> float:
    """
    Compute payoff contribution of c2 to c1.
    Implements Nowak–May Prisoner's Dilemma payoff.
    """
    if c1.strategy == "C" and c2.strategy == "C":
        return 1.0
    elif c1.strategy == "C" and c2.strategy == "D":
        return 0.0
    elif c1.strategy == "D" and c2.strategy == "C":
        return b
    elif c1.strategy == "D" and c2.strategy == "D":
        return 0.0
    else:
        raise ValueError(f"Unknown strategy: {c1.strategy}, {c2.strategy}")


def create_board(num_rows: int, num_cols: int, fill_strategy: str = "C") -> list[list[Cell]]:
    """
    Create a new board of given size, filling each cell with the given strategy.
    """
    if not isinstance(num_rows, int) or not isinstance(num_cols, int):
        raise ValueError("num_rows and num_cols must be integers.")
    if num_rows <= 0 or num_cols <= 0:
        raise ValueError("num_rows and num_cols must be positive.")

    board: list[list[Cell]] = []
    for i in range(num_rows):
        row: list[Cell] = []
        for j in range(num_cols):
            row.append(Cell(fill_strategy, 0.0))
        board.append(row)
    return board


def copy_board(src: list[list[Cell]]) -> list[list[Cell]]:
    """
    Deep copy a board of Cells.
    """
    assert_rectangular(src)
    rows = count_rows(src)
    cols = count_cols(src)

    dst = create_board(rows, cols, "C")
    for i in range(rows):
        for j in range(cols):
            dst[i][j].strategy = src[i][j].strategy
            dst[i][j].score = src[i][j].score
    return dst


def neighbor_coords(i: int, j: int, rows: int, cols: int) -> list[tuple[int, int]]:
    """
    Return the 8-neighbor coordinates (toroidal).
    """
    coords: list[tuple[int, int]] = []
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            ni = (i + di) % rows
            nj = (j + dj) % cols
            coords.append((ni, nj))
    return coords


def update_scores(dest: list[list[Cell]], src: list[list[Cell]], b: float) -> None:
    """
    Compute scores for each cell in dest based on strategies in src.
    """
    assert_rectangular(src)
    rows = count_rows(src)
    cols = count_cols(src)

    for i in range(rows):
        for j in range(cols):
            s = 0.0
            me = src[i][j]
            nbrs = neighbor_coords(i, j, rows, cols)
            for (ni, nj) in nbrs:
                s += game_between(me, src[ni][nj], b)
            dest[i][j].score = s


def update_strategies(dest: list[list[Cell]], src: list[list[Cell]]) -> None:
    """
    Strategy update using scores from 'dest' (this round) and strategies from 'src' (prior round).

    Rule:
      1) Scores already computed into dest[i][j].score.
      2) Compare self_score to neighbor scores (all from this round).
      3) If self_score >= every neighbor score, KEEP src[i][j].strategy.
         Else adopt the src-strategy of a neighbor with the highest score.
         If multiple neighbors tie for best, prefer 'D' over 'C'.
    """
    assert_rectangular(src)
    rows = count_rows(src)
    cols = count_cols(src)

    # --- snapshot scores so we don't read mutated values mid-pass ---
    score_grid: list[list[float]] = []
    i = 0
    while i < rows:
        row_scores: list[float] = []
        j = 0
        while j < cols:
            row_scores.append(dest[i][j].score)
            j += 1
        score_grid.append(row_scores)
        i += 1

    # --- decide new strategies using the frozen score_grid ---
    i = 0
    while i < rows:
        j = 0
        while j < cols:
            self_score = score_grid[i][j]
            self_strategy = src[i][j].strategy

            best_neighbor_score = float("-inf")
            best_neighbor_strategy = None

            nbrs = neighbor_coords(i, j, rows, cols)
            k = 0
            while k < len(nbrs):
                ni, nj = nbrs[k]
                s = score_grid[ni][nj]          # read from snapshot
                st = src[ni][nj].strategy       # neighbor's strategy to adopt
                if s > best_neighbor_score:
                    best_neighbor_score = s
                    best_neighbor_strategy = st
                elif s == best_neighbor_score:
                    # deterministic neighbor tie-break: prefer 'D'
                    if best_neighbor_strategy == "C" and st == "D":
                        best_neighbor_strategy = "D"
                k += 1

            if self_score >= best_neighbor_score:
                new_strategy = self_strategy
            else:
                new_strategy = best_neighbor_strategy

            dest[i][j].strategy = new_strategy
            j += 1
        i += 1

    # --- reset scores AFTER the whole pass (or keep if you prefer to inspect them) ---
    i = 0
    while i < rows:
        j = 0
        while j < cols:
            dest[i][j].score = 0.0
            j += 1
        i += 1


def update(g1: list[list[Cell]], b: float) -> list[list[Cell]]:
    """
    Perform one synchronous update:
      - compute scores
      - update strategies
    Returns a new board.
    """
    rows = count_rows(g1)
    cols = count_cols(g1)
    g2 = create_board(rows, cols, "C")
    update_scores(g2, g1, b)
    update_strategies(g2, g1)
    return g2


def evolve(initial_board: list[list[Cell]], steps: int, b: float) -> list[list[list[Cell]]]:
    """
    Evolve a board for a given number of steps.
    Returns a list [B0, B1, ..., B_steps].
    """
    if not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a non-negative integer")

    assert_rectangular(initial_board)
    rows = count_rows(initial_board)
    cols = count_cols(initial_board)

    boards: list[list[list[Cell]]] = []
    for _ in range(steps + 1):
        boards.append(create_board(rows, cols, "C"))

    boards[0] = copy_board(initial_board)
    for t in range(1, steps + 1):
        boards[t] = update(boards[t - 1], b)

    return boards