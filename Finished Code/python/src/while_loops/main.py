def main():
    print("While loops in Python.")

    n = 5
    m = factorial(n)
    print(m)

    print("0! is", factorial(0))
    # n! = n*(n-1)!
    # 1! = 1*0!
    # 1 = 0! :)

    # print(factorial(-100))

    print("Sum of first 100 positive integers is", sum_first_n_integers(100))

    print(gauss_sum(100))


# 1 + 2 + ... + 99 + 100 = (1 + 100) + (2 + 99) + (3 + 98) + ... (50 + 51)
# = 50 * (101) = 5050
# 1 + 2 + ... + n = (n+1)*(n/2)

def gauss_sum(n: int) -> int:
    """
    Sums the first n positive integers using Gauss's formula.

    Parameters:
    - n (int)

    Returns:
    int: Sum of the first n positive integers.

    Raises an error if n < 0.
    """
    if n < 0:
        # handle negative input with an error
        raise ValueError("Error: negative input given to gauss_sum().")

    return (n * (n+1) // 2)

def sum_first_n_integers(n: int) -> int:
    """
    Takes as input an integer n and returns sum of the first n positive integers, n + (n-1) + ... + 2 + 1

    Raises an error if n < 0.
    """

    # let's ensure that n >= 0
    if n < 0:
        print("n is", n)
        raise ValueError("Error: negative input given to sum.")

    s = 0
    j = 1

    while j <= n:
        s += j # equivalent to s = s + j
        j += 1 # equiv to j = j + 1
        # python does not have j++

    # also: s *= j, s /= j, s -= j

    # at this point, we know that j > n

    return s

def factorial(n: int) -> int:
    """
    Takes as input an integer n, returns n! = n * (n-1) * ... (2) * 1

    Raises an error if n < 0.
    """

    # let's ensure that n >= 0
    if n < 0:
        print("n is", n)
        raise ValueError("Error: negative input given to factorial.")

    product = 1
    i = 1
    # i is a variable that we will only use to help us compute the product in a loop
    # i represents "counter" (what is it that we are multiplying into product?)

    while i <= n:
        product = product * i
        # or product *= i
        i = i + 1

    # we are here in the function when i > n
    # i lives here ... which is not great

    return product


if __name__ == "__main__":
    main()
