"""
Pseudocode below.

IsPrime(p)
    if p < 2
        return false
    for every integer k between 2 and √p
        if k is a divisor of p
            return false
    return true

SieveOfEratosthenes(n)
    primeBooleans ← array of n+1 true boolean variables
    primeBooleans[0] ← false
    primeBooleans[1] ← false
    for every integer p between 2 and √n
        if primeBooleans[p] = true
            primeBooleans ← CrossOffMultiples(primeBooleans, p)
    return primeBooleans

CrossOffMultiples(primeBooleans, p)
    n ← length(primeBooleans) - 1
    for every multiple k of p (from 2p to n)
        primeBooleans[k] ← false
    return primeBooleans

TrivialPrimeFinder(n)
    primeBooleans ← array of n+1 false boolean variables
    for every integer p from 2 to n
        if IsPrime(p) is true
            primeBooleans[p] ← true
    return primeBooleans
"""

import math

import time

import matplotlib.pyplot as pyplot

def trivial_prime_finder(n: int) -> list[bool]:
    """
    Finds all prime numbers up to and possibly including n.

    Parameters:
    - n: int

    Output:
    list[bool]: list of length n+1 whose element at index p will be True if p is prime and False if it is not
    (i.e., prime_booleans[p] = True if p is prime)
    """

    if n < 0:
        raise ValueError("Error: negative integer given as input.")

    prime_booleans = [False]*(n+1)  # set default values

    for p in range(2, n+1):  # we know 0 and 1 are not prime
        # is it the case that p is prime?
        prime_booleans[p] = is_prime(p)

    return prime_booleans

def is_prime(p: int) -> bool:
    """
    Returns True if input integer is prime and False otherwise.

    Parameters:
    - p (int)

    Output:
    bool: True if p is prime and False otherwise.
    """

    if p < 0:
        raise ValueError("Error: negative integer given as input.")

    # easy cases: p = 0 or 1 (False)
    if p < 2:
        return False

    # we need to check every possible candidate divisor of p
    for k in range(2, int(math.sqrt(p))+1):
        # is k a divisor of p?
        if p%k == 0:
            # yes, divisor of p, so p is not prime
            return False

    # if we survive all the divisor checks, we know that p is prime
    return True

# if p = k * b with k <= b, then k <= sqrt(p)
# if k > sqrt(p) (so b > sqrt(p))
# then k * b > (sqrt(p)*sqrt(p)) = p
# so k > sqrt(p) cannot be true :)

def sieve_of_eratosthenes(n: int) -> list[bool]:
    """
    Finds all prime numbers up to and possibly including n, using Eratosthenes' approach from ancient Greece.

    Parameters:
    - n: int

    Output:
    list[bool]: list of length n+1 whose element at index p will be True if p is prime and False if it is not
    (i.e., prime_booleans[p] = True if p is prime)
    """

    if n <= 0:
        raise ValueError("Error: invalid integer given as input.")

    prime_booleans = [True] * (n+1)

    # 0 and 1 are definitely not prime
    prime_booleans[0] = False
    prime_booleans[1] = False

    # range p from 2 to sqrt(n)
    for p in range(2, int(math.sqrt(n)) + 1):
        if prime_booleans[p]:  # think of this as a gray value in the table
            # we know that p is prime, so cross off its multiples (i.e., set its multiples to False)
            prime_booleans = cross_off_multiples(prime_booleans, p)

    return prime_booleans

def cross_off_multiples(prime_booleans: list[bool], p:int) -> list[bool]:
    """
    Crosses off all the multiples of a given integer in a table holding primality of collection of integers between 0 and n+1.

    Parameters:
    - prime_booleans (list[bool])
    - p (int)

    Output:
    list[bool]: updated version of prime_booleans corresponding to setting prime_booleans[k] = False for every integer k that is a multiple of p
    """
    if p < 2:
        raise ValueError("Error: value of p too small.")

    if len(prime_booleans) < 2:
        raise ValueError("Error: prime booleans list too short.")

    # make sure that n is declared
    # len(prime_booleans) = n+1
    # len(prime_booleans) - 1 = n
    n = len(prime_booleans)-1

    # range over all indices of prime_booleans that are multiples of p and "cross them off"
    for k in range(2*p, n+1, p):
        # is it the case that k is a multiple of p? YES
        prime_booleans[k] = False

    return prime_booleans

def list_primes(n: int) -> list[int]:
    """
    Returns a list of all primes up to and (possibly including) n.

    Parameters:
    - n: int

    Output:
    list[int]: list of all primes up to and including n.
    """
    if n < 0:
        raise ValueError("Error: negative integer given as input.")

    # I don't know how big the list is going to ultimately be. And that's OK.

    prime_list = []  # or list()

    # we already have code to find the primes :)
    prime_booleans = sieve_of_eratosthenes(n)

    # range through this list and identify which ones are True
    for p in range(0, len(prime_booleans)):
        if prime_booleans[p]:
            # append the current integer to list of primes
            prime_list.append(p)

    return prime_list

# how many prime numbers are there?
# Infinite! Why? It's proven!

# How many prime numbers are there <= n?
# Is there a formula in terms of n?

# Let's plot all the primes up to n

def prime_count_array(n: int) -> list[int]:
    """
    Produces a list storing the number of primes encountered up to a given integer.

    Parameters:
    - n: int

    Output:
    list[int]: list having length n+1 whose k-th element is equal to the number of primes less than or equal to k
    """

    if n < 0:
        raise ValueError("Error: negative integer given.")

    # first, get all the prime values as True or False
    prime_booleans = sieve_of_eratosthenes(n)

    # next, let's make the list we care about
    result = [0] * (n+1)

    # we need to keep track of how many primes we have encountered up to a point in time
    prime_counter = 0

    # range over list of primes
    for i in range(0, len(prime_booleans)):
        # is current number prime?
        if prime_booleans[i]:
            # found a prime! so update counter
            prime_counter += 1
        # set the current value of my list equal to num of primes encountered thus far
        result[i] = prime_counter

    return result

def plot_primes(n: int, step: int):
    """
    Plots the number of prime numbers as a line graph, where (x, y) corresponds to: x = integer k, y = # of primes encountered up to and including k, where we skip every step x-values for some step parameter.

    Parameters:
    - n (int)
    - step (int)

    Output:
    (nothing, produces plot)
    """
    if n < 0 or step < 1:
        raise ValueError("Invalid value given.")

    # function for number of primes up to and including k is called pi(k)
    pi = prime_count_array(n)

    # make lists of x and y values
    x_values = []

    # x-values are all the values of k, where we increase by step size each time
    for x in range(2, n+1, step):
        x_values.append(x)

    # make list of y values
    y_values = []

    # for a given x, the y-value is pi(x), the number of primes that I have encountered thus far
    for x in x_values:
        y_values.append(pi[x])

    # let's have another collection of y_values corresponding to n/log(n)
    y_values_approx = []
    for x in x_values:
        y_values_approx.append(x/math.log(x))

    # Now, plot
    pyplot.figure(figsize=(9,6))  # width and height in inches

    pyplot.plot(x_values, y_values, label="pi(n), prime count")

    # add in a plot for the n/log(n) function
    pyplot.plot(x_values, y_values_approx, linestyle="--", label="n/log n")

    pyplot.title("Prime Counting Function pi(n) vs. n/log n")

    pyplot.xlabel("n")

    pyplot.ylabel("pi(n)")

    pyplot.legend()
    pyplot.tight_layout()  # ensure that automatically resized
    pyplot.show()   # we're ready to draw :)

# pi(n) is very similar to n/log(n), where log is the natural logarithm

def main():
    print("Prime finding.")

    n = 11
    prime_booleans = trivial_prime_finder(n)

    print(prime_booleans)

    print(is_prime(7))

    print(sieve_of_eratosthenes(n))

    # timing the two algorithms
    n = 2000
    start = time.time()
    trivial_prime_finder(n)
    elapsed_trivial = time.time() - start
    print(f"Trivial prime finder took {elapsed_trivial:.6f} seconds.")

    start = time.time()
    sieve_of_eratosthenes(n)
    elapsed_sieve = time.time() - start
    print(f"Sieve of Eratosthenes took {elapsed_sieve:.6f} seconds.")

    # print the speedup
    if elapsed_sieve > 0:
        speedup = elapsed_trivial/elapsed_sieve
        print(f"Speedup: {speedup:.2f}x faster")

    n = 23
    prime_list = list_primes(n)
    print("The primes up to", n, "are", prime_list)

    print(prime_count_array(23))

    n = 10000000
    step = 100
    plot_primes(n, step)

if __name__ == "__main__":
    main()
