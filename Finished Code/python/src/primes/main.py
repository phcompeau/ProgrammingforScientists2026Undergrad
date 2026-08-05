import math

import time

def main():
    print("Prime finding.")

    n = 10
    

    prime_booleans = trivial_prime_finder(n)

    print(prime_booleans)

    prime_booleans = sieve_of_eratosthenes(n)

    print(prime_booleans)

    prime_list = list_primes(n)

    print("The primes up to", n, "are", prime_list)

    # timing trivial_prime_finder

    n = 10000000

    start = time.time() # START
    trivial_prime_finder(n)
    elapsed_trivial = time.time() - start # STOP
    print(f"trivial_prime_finder took {elapsed_trivial:.6f} seconds.")

    #timing sieve
    start = time.time()
    sieve_of_eratosthenes(n)
    elapsed_sieve = time.time() - start # STOP
    print(f"sieve_of_eratosthenes took {elapsed_sieve:.6f} seconds.")

    # print the speedup
    if elapsed_sieve > 0:
        speedup = elapsed_trivial/elapsed_sieve
        print(f"Speedup: {speedup:.2f} times faster.")


"""
Pseudocode below.

TrivialPrimeFinder(n)
    primeBooleans ← array of n+1 false boolean variables
    for every integer p from 2 to n
        if IsPrime(p) is true
            primeBooleans[p] ← true
    return primeBooleans

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
"""

def trivial_prime_finder(n: int) -> list[bool]:
    """
    Returns a list of boolean variables storing the primality of each nonnegative integer up to and including n.
    Parameters:
    - n (int): an integer
    Returns:
    list[bool]: a list of boolean variables storing the primality of each nonnegative integer up to and including n.
    """

    if n < 0:
        raise ValueError("n must be nonnegative.")
    
    # initialize a bunch of values to False
    prime_booleans = [False] * (n+1)

    # range over all integers from 2 to n, checking if each one is prime 
    for p in range(2, n+1):
        prime_booleans[p] = is_prime(p)

    return prime_booleans

def is_prime(p: int) -> bool:
    """
    Test if p is prime.
    Parameters:
    - p (int): an integer
    Returns:
    bool: True if p is prime and False otherwise.
    """

    if p < 2:
        return False 
    
    # range over all possible divisors between 2 and sqrt(p), and if we find one that is a divisor of p, it can't be prime 
    for k in range(2, int(math.sqrt(p)+1)):
        # if k is a divisor of p, return false 
        if p % k == 0:
            return False
        
    # if we make it here, we never found a divisor of p, which must be prime 
    return True

def sieve_of_eratosthenes(n: int) -> list[bool]:
    """
    Returns a list of boolean variables storing the primality of each nonnegative integer up to and including n,
    implementing the "sieve of Eratosthenes" algorithm.
    Parameters:
    - n (int): an integer
    Returns:
    list: a list of boolean variables storing the primality of each nonnegative integer up to and including n.
    """

    if n < 0:
        raise ValueError("n must be nonnegative.")
    
    prime_booleans = [True]*(n+1)

    # we know that 0 and 1 are not prime 
    prime_booleans[0] = False 
    prime_booleans[1] = False 

    # range over every p between 2 and sqrt(n) and cross off its multiples 
    for p in range(2, int(math.sqrt(n) + 1)):
        if prime_booleans[p] == True:
            # we know that p is prime, so cross off its multiples (i.e., set its multiples to false) 
            prime_booleans = cross_off_multiples(prime_booleans, p)

    return prime_booleans
    
def cross_off_multiples(prime_booleans: list[bool], p:int) -> list[bool]:
    """
    Returns an updated list in which all variables in the list whose indices are multiples of p (greater than p) have
    been set to false.
    Parameters:
    - prime_booleans (list): a list of boolean variables storing the primality of each nonnegative integer
    - p (int): an integer
    Returns:
    list[bool]: a list of boolean variables storing the primality of each nonnegative integer up to and including n with
    multiples of p (greater than p) set to false.
    """

    # we know that len(prime_booleans) = n + 1
    # n = len(prime_booleans) - 1

    if p <= 0:
        raise ValueError("p should be positive.")
    
    if len(prime_booleans) == 0:
        raise ValueError("empty prime_booleans list.")
    
    n = len(prime_booleans) - 1

    for k in range(2*p, n+1, p):
        prime_booleans[k] = False

    return prime_booleans

def list_primes(n: int) -> list[int]:
    """
    List all prime numbers up to and (possibly) including n.
    Parameters:
    - n (int): an integer
    Returns:
    list[int]: a list containing all prime numbers up to and (possibly) including n.
    """

    if n < 0:
        raise ValueError("n should be nonnegative.")
    
    prime_list = [] 
    
    # first, use sieve of Eratosthenes 
    prime_booleans = sieve_of_eratosthenes(n)

    # range over this list of booleans, and if we find something that's prime, add it to prime_list 
    for p in range(0, len(prime_booleans)): 
        if prime_booleans[p] == True:
            # add it to list of primes!
            prime_list.append(p)

    return prime_list

if __name__ == "__main__":
    main()