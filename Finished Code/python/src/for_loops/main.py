def main():
    print("For loops in Python.")

    print(another_factorial(10))

def say_hi_five():
    """
    Prints "Hi" five times.
    """
    # if bottom index is 0, you can omit it
    for _ in range(5):
        print("hi")
        # _ indicates that we don't need the variable

def sum_even(k: int) -> int:
    """
    Returns the sum of all even positive integers up to and possibly including k.
    """
    s = 0

    for i in range(2, k+1):
        # is i even?
        if i % 2 == 0:
            #yes 
            s += i

    return s

def another_sum_even(k: int) -> int:
    """
    Returns the sum of all even positive integers up to and possibly including k.
    """
    s = 0

    # the third parameter in range is the "step size";
    # it tells us how much to increase i by each time through the loop
    for i in range(2, k+1, 2):
        s += i
        # i must always be even

    return s

def yet_another_factorial(n: int) -> int:
    """
    Factorial, but with for, and fancy.
    """
    # let's ensure that n >= 0
    if n < 0:
        print("n is", n)
        raise ValueError("Error: negative input given to factorial.")
    
    product = 1 

    # for loops are always preferable IF we know how many iterations through the loop we're going to take 
    # there are other instances where we can only use while
    for i in range(n, 0, -1):
        # i lives only within this loop
        product *= i

    return product

def another_factorial(n: int) -> int:
    """
    Factorial, but with for.
    """
    # let's ensure that n >= 0
    if n < 0:
        print("n is", n)
        raise ValueError("Error: negative input given to factorial.")
    
    product = 1 


    # for loops are always preferable IF we know how many iterations through the loop we're going to take 
    # there are other instances where we can only use while
    for i in range(1, n+1):
        # i lives only within this loop
        product *= i

    return product

if __name__ == "__main__":
    main()