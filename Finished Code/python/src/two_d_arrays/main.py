def main():
    print("Two-dimensional arrays (tuples and lists).")

    # here is a mystery 3 x 3 matrix from HW3

    # a 2-d tuple is a tuple whose elements are tuples
    kernel = (
        (0.05, 0.20, 0.05),
        (0.20, 0, 0.20),
        (0.05, 0.20, 0.05),
    )

    print(kernel)

    # I can access individual elements 
    # kernel[r][c] gives element at row r, col c
    print(kernel[0][2])
    print(kernel[1][1])
    print(kernel[2][1])

    # we can isolate rows too 
    print("Row 1 is", kernel[1])

    # tuples are immutable, so not that practical most of time 
    # kernel[1][1] = 0.3 # type error!

    # say we want to make a 2-d list with 7 rows and 4 columns 

    # remember: ...
    a = [0] * 7
    print(a)

    # declaring a 7 x 4 list
    a = [[0] * 4] * 7  # this creates one list of length 4 and 7 "references" to it

    for r in range(7):
        print(a[r])

    # changing an element 
    a[1][3] = 5

    print("List has been changed!")

    for r in range(7):
        print(a[r])

    # this is the ugly of python 
    # what happened? We created only one list of length 4, and we created 7 references to it ?!!!

    a = []
    for row in range(7):
        new_row = [0] * 4
        a.append(new_row)

    print("a has been updated.")

    print(a)

    print("Changing one value? Yes :)")

    a[1][3] = 5
    for r in range(7):
        print(a[r])

    # we also have len()
    print("Number of rows of a is", len(a)) # number of rows

    # how about columns?
    print("Number of columns is", len(a[0]))

    # this works because we know that a has at least one row and is rectangular

    num_rows = 4 
    board = [] 

    # make rows of board 
    for row in range(num_rows):
        current_row = [False] * row
        board.append(current_row)

    print(board)

    # let's add a False element to each row 
    for row in range(len(board)):
        # current row is board[row]
        board[row].append(False)

    print(board)

    set_first_element_to_true(board)

    print("I tried to set the top left element to True.")

    print(board)

    # just as with one-d lists, two-d lists are pass by reference

# def print_game_of_life_board(board: list[list[bool]]) -> None:
# we could write this, but I would rather use what we learned about drawing to write to file

"""
This is the function we will write next week.
def play_game_of_life(board: list[list[bool]]) -> list[list[list[bool]]]:
    # this is what we want to write, and it has nothing to do with printing 
"""


def set_first_element_to_true(a: list[list[bool]]) -> None:
    """
    Set the top left element of a 2-D boolean list to True.
    """
    if len(a) == 0 or len(a[0]) == 0:
        raise ValueError("Board is empty or has no first row length.")
    
    a[0][0] = True


if __name__ == "__main__":
    main()