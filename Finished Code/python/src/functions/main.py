def main():
    print("Functions in Python.")
    x = 3 
    n = sum_two_ints(x, 4)

    print("The sum of 3 and 4 is", n)

    print(sum_two_ints("Hi", "YOYO"))
    print(sum_two_ints(2.78, 3.42))
    print(sum_two_ints(True, False))

    #print(double_and_duplicate(1.5))
    m = 17
    print(add_one(m))
    print(m)

    # all basic types (strings, ints, etc.) use pass by value: copy of variable is created passed into function

# every function we write (unless I'm pressed for time or lazy) will have a docstring

def add_one(k: int) -> int:
    """
    Add one to the input variable and return it.
    """
    k = k + 1
    # k is 18
    return k
    # we always are returning the value 
    # k dies :(


# every function has the format
# def fn_name(parameters):
def sum_two_ints(a:int, b:int) -> int:
    """
    Add two integers and returns their sum.

    Parameters:
    - a (int)
    - b (int)

    Returns:
    int: a+b
    """
    
    return a + b

def double_and_duplicate(x:float) -> tuple[float, float]:
    """
    Double the input variable and return two copies of the result.
    """

    return 2 * x, 2 * x

def print_hi():
    """
    Takes no input and simply prints Hi
    """
    print("Hi")


if __name__ == "__main__":
    main()