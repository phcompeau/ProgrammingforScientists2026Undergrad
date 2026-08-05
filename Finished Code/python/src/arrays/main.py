def main():
    print("Arrays (Tuples, lists) in Python.")

    # Python represents arrays in two ways

    # way #1 is called a "Tuple"
    primes = (2, 3, 5, 9, 11)

    # tuples are great when the length of the array is short and fixed
    # we use them for returning multiple values from a function

    print(primes)

    # elements of primes are primes[i], where i ranges from 0 up to and including 4
    print(primes[2])

    # we need to update primes to fix our mistake 
    # primes[3] = 7
    # This gives an error!
    # We cannot update individual elements of a tuple
    # Tuples are immutable: we can't change individual elements, and we can't append an element to them 

    # we can update the whole tuple 
    primes = (2, 3, 5, 7, 11)

    print("primes is now", primes)

    # mostly, we will work with lists when we implement arrays 
    empty_list = []

    n = 6 
    a = [0] * n

    print(a)

    # lists can have multiple types in them 
    mixed_list = [1, 3.14, "Hi", True]
    print(mixed_list)

    # lists are mutable, meaning we can set individual elements 
    a[0] = -8
    i = 3
    k = 4
    a[2*i-4] = (k//2) ** 4 + 1 #2*i - 4 = 2
    print(a)

    # python gives a len() function to tell the length of the array 
    print("a has length", len(a))

    # indices of a range from 0 to len(a) - 1
    a[len(a)-1] = 43 # updates final element

    print(a)

    # Python has "negative indexing", where you can go backward through a list 
    a[-2] = 68
    # we will not use this so help me god

    print(a)

    n = 10
    print(factorial_array(n))

    b = [3, 2, 1]
    print(min_integer_array(b))

    # Python has a built in min function to take an arbitrary number of inputs: min(1, 3), or min(1, -3, 4, 80), etc.

    print(min_integers_better(-1, 4, 17))

    c = [0]*6

    print("c starts at", c)

    change_first_element(c)

    print("After function, c is", c)

    # Lists in Python are pass by reference

def change_first_element(a: list[int]):
    a[0] = 1

# Variadic function takes an arbitrary number of parameters
def min_integers(*numbers: int) -> int:
    """"
    Returning the minimum value of an arbitrary collection of integers.
    """
    # In this case, numbers is a tuple

    if len(numbers) == 0:
        raise ValueError("Error: no numbers given to min_integers.")

    m = numbers[0]

    for val in numbers:
        if val < m:
            m = val 

    return m

def min_integers_better(*numbers: int) -> int:
    """
    Returning the minimum value of an arbitrary collection of integers.
    """
    # In this case, numbers is a tuple
    return min_integer_array(list(numbers))

def min_integer_array(a:list[int]) -> int:
    """"
    Returning the minimum value in a list of integers.
    """

    if len(a) == 0:
        raise ValueError("Error: empty list given.") 

    m = 0

    # iterate over list, updating m if we find a smaller value

    for i, val in enumerate(a):
        # ranges over the values in a list
        # if we find a smaller value than the current min 
        # OR we are at the first element, update m
        if val < m or i == 0:
            m = val

    return m


def factorial_array(n: int) -> list[int]:
    """
    Generates a list of factorials, from 0! to n! inclusively.
    """
    # check n < 0 

    # I know how long the array should be, so I create all the data behind the scenes 
    fact = [0]*(n+1)

    fact[0] = 1 #0! = 1
    for k in range(1, n+1):
        # two ways: #1, call a subroutine factorial()
        # fact[k] = factorial(k)
        fact[k] = fact[k-1] * k

    return fact


if __name__ == "__main__":
    main()