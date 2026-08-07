def main():
    print("Strings in Python.")
    s = "Hi"
    t = 'Lovers'
    # strings can have single or double quotes

    # concatenation glues together strings
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

    dna = "ACCGAT"
    print(complement(dna))  #TGGCTA
    print("Reverse:", reverse(dna))  #TAGCCA
    print(reverse_complement(dna))  #ATCGGT

def reverse_complement(dna: str) -> str:
    """
    Takes a DNA string (A, C, G, and T symbols only) as input and returns its reverse complement, meaning the string corresponding to a complementary strand (e.g., rev comp of "AGTC" is "GACT").
    """
    # dna = complement(dna)  # complement of "AGTC" is "TCAG"
    # dna = reverse(dna)     # reverses the symbols in string
    # return dna
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

#   i       index of s
#   0       n-1
#   1       n-2
#   2       n-3
#   i       (n-1)-i
#   n-1     0

def complement(dna: str) -> str:
    """
    Finds the complementary strand of a given DNA string (without reversing it).
    e.g., if given ACGT, returns TGCA (A-T, C-G, T-A, G-C)
    """

    dna2 = "" #empty string

    # range over the string, take complement at each position
    # match statements are good for multiple cases (called a switch in other languages)
    for symbol in dna:
        # what is the current symbol in my string?
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
                raise ValueError("Error: symbol in string is not a DNA nucleotide.")

    return dna2


"""
ReverseComplement(pattern)
    pattern ← Reverse(pattern)
    pattern ← Complement(pattern)
    return pattern
"""

if __name__ == "__main__":
    main()
