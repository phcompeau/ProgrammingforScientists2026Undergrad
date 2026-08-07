import time

# GCD(0, a) = a if a >= 0

# GCD(50, 375) = GCD(50, 325)
#               = GCD(50, 275)
#               = GCD(50, 225)
# ...
#               = GCD(50, 25)
#               = GCD(50, 375%50)
# GCD(50, 25)   = GCD(50 % 25, 25)
# GCD(0, 25)    = 25

def faster_euclid_gcd(a:int, b:int) -> int:
    """
    Returns the GCD of two integers using Euclid's algorithm.

    Parameters:
    - a (int)
    - b (int)

    Returns:
    int: GCD of a and b
    """

    # if you have negative values, flip their signs
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    # we're going to keep going for how long?
    while (a != 0) and (b != 0):
        if a > b:
            a = a%b
        else:  # b >= a
            b = b%a

    # so if we make it here, either a or b is zero (they might both be zero) ... we are in the realm of the mathematicians
    if a == 0:
        return b
    else:
        # b = 0
        return a

def euclid_gcd(a:int, b:int) -> int:
    """
    Returns the GCD of two integers using Euclid's algorithm from 2400 years ago.

    Parameters:
    - a (int)
    - b (int)

    Returns:
    int: GCD of a and b
    """

    # if you have negative values, flip their signs
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    # GCD(0, n) = n
    if a == 0:
        return b  # this works even if they're both 0

    if b == 0:
        return a

    while a != b:
        # check which is bigger, and set the bigger equal to the bigger minus the smaller
        if a > b:
            a = a-b
        else:
            # know that b > a
            b = b-a

    # what do we know if we're here? a == b, and they are both equal to the GCD
    return a  # or b

    # critical fact: GCD(a, b) = GCD(a-b, b) when a > b
    # GCD(63, 42) = GCD(21, 42) = GCD(21, 21) = 21
    # GCD(-63, 42) = 21

def trivial_gcd(a:int, b:int) -> int:
    """
    Returns the GCD of two integers using a trivial algorithm that tries every possible divisor of a and b.

    Parameters:
    - a (int)
    - b (int)

    Returns:
    int: GCD of a and b
    """
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    # GCD(0, n) = n
    if a == 0:
        return b  # this works even if they're both 0

    if b == 0:
        return a

    d = 1
    m = min(a, b)

    # try every possible candidate divisor up to and including m, and update d every time we find a divisor
    for p in range(2, m+1):
        # if p is a divisor of both, then d = p
        if (a % p == 0) and (b % p == 0):
            d = p
            # if the first statement in an and is False, then the whole thing is immediately False and the second condition isn't even read

    return d

#   x       y       x and y     x or y
#   True    True    True        True
#   True    False   False       True
#   False   True    False       True
#   False   False   False       False

# if first statement (x) is True, x or y short circuits to True

def main():
    print("Studying GCD algorithms.")

    print("The GCD of 670 and 30 is", trivial_gcd(670, 30))
    print("The GCD of 670 and 30 is", euclid_gcd(670, 30))
    print("The GCD of 42 and 63 is", faster_euclid_gcd(63, 42))

    x = 378202621
    y = 273147907

    # time the trivial approach
    start = time.time()   # starts a stopwatch
    trivial_gcd(x, y)
    elapsed_trivial = time.time() - start  # stops the watch

    # print the time in a pretty way
    print(f"trivial_gcd took {elapsed_trivial:.6f} seconds.")

    start = time.time()
    euclid_gcd(x,y)
    elapsed_euclid = time.time() - start

    print(f"euclid_gcd took {elapsed_euclid:.6f} seconds.")

    # the speedup provided by an algorithm 1 compared to algorithm 2 is the ratio of the runtime of algorithm 2 to algorithm 1
    # e.g., if algorithm 2 takes 8 seconds and algorithm 1 takes 2 seconds, the speedup is 4 x

    if elapsed_euclid > 0:
        speedup = elapsed_trivial/elapsed_euclid
        print(f"Speedup of Euclid vs. Trivial: {speedup:.2f}x faster")

    start = time.time()
    faster_euclid_gcd(x,y)
    elapsed_faster_euclid = time.time() - start

    print(f"faster_euclid_gcd took {elapsed_faster_euclid:.6f} seconds.")

    if elapsed_faster_euclid > 0:
        speedup = elapsed_euclid/elapsed_faster_euclid
        print(f"Speedup of Fast Euclid vs. Normal Euclid: {speedup:.2f}x faster")


if __name__ == "__main__":
    main()
