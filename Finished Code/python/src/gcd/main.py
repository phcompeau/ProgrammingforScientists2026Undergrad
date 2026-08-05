import time 

def main():
    print("GCD algorithms in Python.")
    print(trivial_gcd(670, 30))
    print(euclid_gcd(670, 30))

    x = 378202672
    y = 273147993

    # timing trivial_gcd
    start = time.time() # START
    trivial_gcd(x, y)
    elapsed_trivial = time.time() - start # STOP
    print(f"trivial_gcd took {elapsed_trivial:.6f} seconds.")

    #timing euclid_gcd 
    start = time.time()
    euclid_gcd(x,y)
    elapsed_euclid = time.time() - start # STOP
    print(f"euclid_gcd took {elapsed_euclid:.6f} seconds.")

    # print the speedup
    if elapsed_euclid > 0:
        speedup = elapsed_trivial/elapsed_euclid
        print(f"Speedup: {speedup:.2f} times faster.")



def euclid_gcd(a: int, b: int) -> int:
    """
    Returns the GCD of two integers by applying Euclid's algorithm from 2400 years ago.
    """

    # I should do a check on a and b

    while a != b:
        # check which is bigger, and set the bigger equal to the bigger minus the smaller 
        if a > b:
            a = a-b
        else:
            b = b-a
        
    # as soon as a = b, then they are both = GCD 
    return a # or return b


def trivial_gcd(a: int, b:int) -> int: 
    """
    Returns the GCD of two integers by applying a trivial algorithm trying every possible divisor of a and b
    """

    # I should check that a and b are not negative :)

    d = 1 

    # try every possible divisor of a and b up to their min
    m = min(a, b)

    for p in range(2, m+1):
        # is p a divisor of a AND is it a divisor of b?
        if a % p == 0 and b % p == 0:
            # p is the biggest common divisor  thus far 
            d = p
        # we also have an or keyword
        # x or y produces True if x is True, y is True, or both are True; False otherwise.

    return d

if __name__ == "__main__":
    main()