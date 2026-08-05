def main():
    print("While loops in Python.")
    n = 10
    m = factorial(n)
    print(m)

    print(sum_first_n_integers(100))

def gauss_sum(n: int) -> int:
    return (n * (n+1) // 2)

def sum_first_n_integers(n: int) -> int:
    """
    Takes as input an integer n and returns sum of the first n positive integers, n + (n-1) + ... + 2 + 1
    """

    # let's ensure that n >= 0
    if n < 0:
        print("n is", n)
        raise ValueError("Error: negative input given to sum.")
    
    s = 0 
    j = 1

    while j <= n:
        s += j # equivalent to s = s + i
        j += 1 # equiv to j = j + 1
        # python does not have j++

    return s 

def factorial(n: int) -> int:
    """
    Takes as input an integer n, return n!
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

    # i lives here ... which is not great

    return product


if __name__ == "__main__":
    main()