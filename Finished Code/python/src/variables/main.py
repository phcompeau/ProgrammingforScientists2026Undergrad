def main():
    print("Variables in Python.")
    # This is a comment.
    # Comments are not executed.

    # Four basic types of variables
    # int: integer (-3)
    # float: decimal numeric variable (14.3)
    # bool: "boolean" variable that can be True/False
    # string: word or text of symbols "Hello"

    # a variable is like a box that holds some value
    # (the value can change)

    # Let's declare some variables
    j = 14  #Python gives this type int
    x = -2.3 #type: float 
    yo_world = "Hi" #type: string 
    statement = True # type: bool

    #Note: multi-word variable names use snake_case

    print(j)
    print(x)
    print(yo_world)
    print(statement)

    # the point of variables is that they can change 
    j = -7


    # let's print them on one line 
    print("j is", j)
    print("x is", x)
    print("yo_world is", yo_world)
    print("statement is", statement)

    print(type(statement))
    print(type(j))
    print(type(yo_world))
    print(type(x))

    # don't do this! All variables should start and end with the same type
    statement = "I hate python"
    print("statement now has type", type(statement))

    j = 14
    print(2 * (j+5))
    print(x/4 + 3.16)

    # some languages don't like you combining variables of different types with operations 
    print(x*j) # Python is happy :) .. will give float

    # three more operators: power, int division, and remainder 
    print(14/3) # this is our old friend 4.666666666666667
    print(14 // 3) # this is integer division (prints 4)
    print(14 % 3) # this is the remainder after division (2)
    print(14 ** 3) # this is 14 to the power of 3

if __name__ == "__main__":
    main()