def main():
    print("Strings in Python.")
    s = "Hi"
    t = 'Lovers'
    # strings can have single or double quotes 

    u = s + t 
    print(u)

    # multiplication is repeated concatenation
    print(s*3)

    # access symbols of a string like we do elements of a tuple/list
    print("The first symbol of u is", u[0])
    print("The final symbol of u is", u[len(u)-1])

    # print(u[len(u)]) #error!
    
    if t[2] == "v":
        print("Third symbol of t is v.")

    # let's change u from HiLovers to HiLosers
    # u[4] = "s" # this doesn't work!
    # strings, like tuples, are immutable

    # but you can update the string all at once 
    s = "Yo"
    print("s is now", s)
    print("u is still", u)

    s += "-Yo"
    s += " Ma"
    print(s)

    dna = "ACGTAC"

    print(complement(dna))

    print("Reverse:", reverse(dna))

def reverse_complement(dna: str) -> str:
    """
    Takes a DNA string as input and returns its reverse complement (e.g., rev comp of "ACGTAA" is "TTACGT")
    """
    return reverse(complement(dna)) #yay modularity!

def reverse(s: str) -> str:
    """
    Reverses a given string (i.e., symbols are in same order backwards).
    """
    rev = ""

    # build up our string 
    n = len(s)
    for i in range(n):
        rev += s[n-i-1]

    return rev

def complement(dna: str) -> str:
    """
    Finds the complementary strand of a given DNA string.
    e.g., if given ACGT, returns TGCA
    """

    dna2 = "" #empty string

    # match statements are good for multiple cases 
    for symbol in dna:
        match symbol:
            case "A":
                dna2 += "T"
            case "C":
                dna2 += "G"
            case "G":
                dna2 += "C"
            case "T":
                dna2 += "A"
            case _: # anything else
                raise ValueError("Invalid symbol given.")

    return dna2
    

"""
ReverseComplement(pattern)
    pattern ← Reverse(pattern)
    pattern ← Complement(pattern)
    return pattern
"""

if __name__ == "__main__":
    main()