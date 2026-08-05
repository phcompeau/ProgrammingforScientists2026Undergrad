# five fields for rectangle:
# width, height, x1, y1 (center or top left), rotation

# place class declarations between imports and def main

class Rectangle:
    """
    Represents a 2D rectangle with width, height, position, and rotation

    Attributes:
        width: (float)
        height: (float)
        x1: the x-coordinate of the rectangle's origin (float)
        y1: the y-coordinate of the rectangle's origin (float)
        rotation: rotation of shape in degrees (float)
    
    Class Attributes:
        description: describes some characteristic of the object (string) 
    """

    description: str = "boxy"

    # Every class declaration should have a constructor to set fields
    # Also, Python calls fields "attributes"
    # We will allow the user to set attributes of an instance the second it is born
    def __init__(self, width: float=0.0, height: float=0.0, x1: float=0, y1: float=0, rotation: float=0):
        # let's protect the program from a bad user 
        if width < 0.0 or height < 0.0:
            raise ValueError("width and height must be nonnegative.")
        # we could add tests for if variables are all floats, etc.
        
        # what attributes should every Rectangle get?
        self.width = width
        self.height = height
        self.x1 = x1
        self.y1 = y1
        self.rotation = rotation

    def __repr__(self) -> str:
        # let's have a nice f string to print the attributes 
        return f"Rectangle(width={self.width},height={self.height},x1={self.x1}, y1={self.y1}, rotation={self.rotation})"

class Circle:
    """
    Represents a 2D circle via its center and radius.
    
    Attributes:
        x1: the x-coordinate of the center (float)
        y1: the y-coordinate of the center (float)
        radius: the center's radius (float)

    Class Attributes:
        description: describes some characteristic of the object (string) 
    """

    description: str = "round"

    def __init__(self, x1: float=0, y1: float = 0, radius: float = 0):
        if radius < 0.0:
            raise ValueError("width and height must be nonnegative.")
        self.x1 = x1
        self.y1 = y1
        self.radius = radius

    def __repr__(self) -> str:
        # let's have a nice f string to print the attributes 
        return f"Circle(x1={self.x1}, y1={self.y1}, radius={self.radius})"


def main():
    print("Shapes.")

    # these declarations create an INSTANCE of the object with the default attributes
    x1 = 1.0
    y1 = 3.0
    radius = 2.0
    my_circle = Circle(x1, y1, radius)  # x1 = 1.0, y1 = 3.0, radius = 2.0
    
    r = Rectangle(3.0, 5.0)  # some languages might get mad, Python never gets mad
    # other attributes of r get their defaults (0.0)


    """
    # the baby is born and we can update its attributes 
    my_circle.x1 = 1.0 
    my_circle.y1 = 3.0
    my_circle.radius = 2.0

    r.width = 3.0
    r.height = 5.0

    r.name = "Larry"  # you can do this but don't do this
    """

    # let's print the whole thing 
    print("our rectangle is", r)
    print("our circle is", my_circle)

    # just because we initialized attributes doesn't mean we can't change them 
    r.width = 2.0 
    r.height = 4.5
    r.x1 = -1.45
    r.y1 = 2.3

    print("The rectangle has been updated to", r)

    # lesson: you can't name functions the same thing in Python (except when you can, hold on for next week)

    print("Rectangle's area is", area_rectangle(r))
    print("Circle's area is", area_circle(my_circle))

    # are instances of a new class pass by reference or value?
    translate_circle(my_circle, 10.0, 10.0)
    translate_rectangle(r, 30.0, -100.0)

    print("The circle has been translated to", my_circle)
    print("The rectangle has been translated to", r)

    # instances of a new class are pass by REFERENCE
    # 1. you don't have to return the object 
    # 2. be CAREFUL about changing attributes of an object in a function

    # what we really want is just translate() functions that don't take objects as input

    # we can access class attributes in two ways 
    # 1. access it through an instance
    print("Our rectangle is", r.description)

    #2. access it via the name of the class 
    print("Every circle is", Circle.description)

    my_circle.description = "orb-like"
    print("My circle is", my_circle.description)
    # this creates a new (local) attribute of my_circle and doesn't affect any other circle or the class attribute
    # do not ever use this

    # did I overwrite every circle's description?
    print("Every circle is", Circle.description)





def area_rectangle(r: Rectangle) -> float:
    """
    Compute the area of a given rectangle.
    """
    return r.width * r.height

def area_circle(c: Circle) -> float:
    """
    Compute the area of a circle.
    """
    return 3.0 * (c.radius ** 2)

# write perimeter_rectangle() and perimeter_circle() functions

def translate_rectangle(r: Rectangle, a: float, b:float) -> None:
    """
    Move a rectangle by a given amount in x- and y-directions.
    """
    r.x1 += a 
    r.y1 += b 

def translate_circle(c: Circle, a: float, b:float) -> None:
    """
    Move a circle by a given amount in x- and y-directions.
    """
    c.x1 += a
    c.y1 += b

if __name__ == "__main__":
    main()