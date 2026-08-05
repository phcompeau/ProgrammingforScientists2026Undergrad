def main():
    print("Conditionals in Python.")

    print("The min of 3 and 4 is", min_2(4, 3))
    print(which_is_greater(3, 3))
    # print(min(3, 4, 5, 1, -20))

# comparison operators: >, <, >=, <=, ==

def positive_difference(a:int, b:int) -> int:
    """
    Takes two integers, returns their positive difference.
    """
    if a > b:
        return a - b
    else:
        return b - a
    
# positive_difference is built into Python, so we could just use abs(a-b) (or abs(b-a))

def same_sign(x:int, y:int) -> bool:
    """
    Takes integers x, y as input and returns True if they have the same sign, False otherwise.
    Zero is considered to have the same sign as all numbers.
    """
    # both nonnegative?
    if x >= 0 and y >= 0:
        return True 
    elif x <= 0 and y <= 0:
        # both non positive
        return True
    else:
        # at this point, we know they don't have same sign
        return False
    
# Faster way: if x and y have same sign, what do we know about x * y? It's positive (or zero)
def same_sign_faster(x:int, y:int) -> bool:
    if x*y >= 0:
        return True 
    return False

def same_sign_annoying(x:int, y:int) -> bool:
    return x*y >= 0



# let's see multiple cases 
def which_is_greater(x: int, y:int) -> int:
    """
    Takes two ints x, y as input and returns 1 if x > y, -1 if y > x, and 0 if they're equal
    """
    if x == y:
        return 0
    elif x < y:
        return -1
    else:
        # we know that x > y
        return 1


# Note: Python has a built in function min() that takes min of any # of numbers
def min_2(a: int, b:int) -> int: 
    """
    Takes two integers as input and returns their min.
    """
    if a < b:
        return a
    # if I make it here, I know b <= a
    return b

if __name__ == "__main__":
    main()