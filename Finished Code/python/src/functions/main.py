# def function_name(parameters):

# The definition of functions can occur in any order

# BUT ... when executions are executed, definitions must have already been encountered

# every function we write (unless I'm pressed for time or lazy) will have a docstring

def sum_two_ints(a:int, b:int) -> int:
    """
    Returns the sum of two input integers.

    Parameters:
    - a (int)
    - b (int)

    Returns:
    int: a + b
    """
    return a+b  # this is the output of the function

# Functions can also return more than one value
def double_and_duplicate(x: float) -> tuple[float, float]:
    """
    Double the input variable and return two copies of it.

    Parameters:
    - x (float)

    Returns:
    Two copies of 2*x
    """
    return 2*x, 2*x

def print_hi():
    """
    Takes no input and simply prints "Hi" to the console.
    """
    print("Hi")
    # other things could happen here
    # nothing ultimately gets returned by the function

def add_one(k: int) -> int:
    """
    Add one to the input variable and return the result.

    Parameters:
    - k (int)

    Returns:
    int: k+1
    """
    # when you see variable assignment (x = blah)
    # the left side of the equation is a variable
    # everything on the right side involves values
    k = k+1
    return k
    # k has served its meaningful life

def main():
    """
    Special function that takes no inputs, produces no outputs, but that constitutes the runnable component of our program.
    """
    print("Functions in Python.")

    x = 3
    n = sum_two_ints(x, 4)
    print("The sum of 3 and 4 is", n)

    print(sum_two_ints(-2.1, 4.78))
    print(sum_two_ints("Hi", "YOYO"))
    print(sum_two_ints(True, False))

    # type hints are just that; they are hints. You can still maybe do things that you might not intend due to Python's hyper-flexibility

    print(double_and_duplicate(2.7))

    print_hi()

    # let's call add_one()
    m = 17
    print(add_one(m))

    # we are not changing the underlying value of m
    print("m is now", m)

    # With basic types (str, int, float, etc.) Python uses "pass by value".
    # When a variable is passed into a function as a parameter, a copy is created.

    # "Pass by reference" means that when you pass a variable into a function, you can change it!

    # Python does use pass by reference for some things

    # All of this is not technically quite right.

# the below says, run what is inside def main()
if __name__ == "__main__":
    main()
