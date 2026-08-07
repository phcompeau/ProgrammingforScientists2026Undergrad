import random

def main():
    print("For loops in Python.")

    print(another_factorial(5))
    print(yet_another_factorial(5))

    say_hi_five_times()

    #pittsburgh_january()

# General rule: use a for loop any time you can

# Use a while loop when you're waiting on a condition
# (e.g., user input, randomness, convergence)

# range(a, b) in Python represents the integers between a and b-1, inclusively

# range() has a third parameter, which is a "step size", that allows us to jump the variable by this amount each time through the loop

def say_hi_five_times():
    # print Hello World five times
    # if the bottom index is 0, you can omit it
    for _ in range(5):
        # _ indicates that we don't need the variable
        print("Hello, World!")

def sum_even(k: int) -> int:
    """
    Sums all the even positive integers up to and (possibly including) k.

    Parameters:
    - k: int

    Returns:
    - int: sum of the even positive integers up to k.
    """
    if k < 0:
        raise ValueError("Error: Negative k given to function.")

    s = 0

    """
    # solution 1
    for j in range(2, k+1):
        # is j even?
        if j % 2 == 0:
            # yes, so add it to sum
            s += j
    """

    # solution 2: skip the odd numbers
    for j in range(2, k+1, 2):  # note: step size of 2 means that we add 2 to j every time through
        s += j

    # 2 + 4 + ... + k = 2 * (1 + 2 + ... + k/2)
    """
    # solution 3: use gauss
    return 2*gauss_sum(k//2)
    """

    return s

def yet_another_factorial(n: int) -> int:
    """
    Produces n! = n * (n-1) * ... (2) * 1

    Parameters:
    - n (int)

    Returns:
    int: n!

    Raises an error if n < 0.
    """
    if n < 0:
        # handle negative input with an error
        raise ValueError("Error: negative input given to factorial().")

    p = 1  # think of p as the container that will represent my growing product

    # for every integer i between 1 and n, p = p*i
    for i in range(n, 0, -1):  #-1 means decrease i by 1 each time
        # i lives only within this loop
        p = p*i   # left side: variable, right side: value

    # we are here in the function when i > n
    return p

def pittsburgh_january():
    """
    Simulates Pittsburgh winter.
    Each day has an 80% chance of snow.
    The loop continues until it stops snowing, and I move to Florida.
    """

    day = 1  # date
    dream = True  # start off dreaming

    while dream == True:
        # generate a random number between 0 and 1
        x = random.random()
        if x < 0.8:
            print("It is January", day, "and it is snowing.")
            print("Continue dream of Tampa.")
            day += 1
        else:
            # it didn't snow!
            dream = False
            print("It is January", day, "and no snow.")
            print("Headed to Tampa.")

def another_factorial(n: int) -> int:
    """
    Produces n! = n * (n-1) * ... (2) * 1

    Parameters:
    - n (int)

    Returns:
    int: n!

    Raises an error if n < 0.
    """
    if n < 0:
        # handle negative input with an error
        raise ValueError("Error: negative input given to factorial().")

    p = 1  # think of p as the container that will represent my growing product

    # for every integer i between 1 and n, p = p*i
    for i in range(1, n+1): # adds 1 to i automatically
        # i lives only within this loop
        p = p*i   # left side: variable, right side: value

    # we are here in the function when i > n
    return p

if __name__ == "__main__":
    main()
