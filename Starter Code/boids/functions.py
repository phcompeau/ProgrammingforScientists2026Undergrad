from datatypes import OrderedPair, Boid, Sky 
import math

#add your additional functions from cogniterra here!

def distance(p0: OrderedPair, p1: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two points in 2D space.
    Input:
        p0 (OrderedPair): The first point, with x and y coordinates.
        p1 (OrderedPair): The second point, with x and y coordinates.
    Output:
        float: The Euclidean distance between p0 and p1.
    """
    dx = p0.x - p1.x
    dy = p0.y - p1.y
    return math.sqrt(dx * dx + dy * dy)

def copy_sky(current_sky: Sky) -> Sky:
    """
    Create a deep copy of a Sky object, duplicating all its parameters and boids.
    Input:
        current_sky (Sky): The Sky instance to be copied, containing boids and 
                           simulation parameters (e.g., width, max speed, proximity).
    Output:
        Sky: A new Sky object with identical properties and boid data as the input, 
             but stored in separate memory so changes to one do not affect the other.
    """
    new_sky = Sky()
    new_sky.width = current_sky.width
    new_sky.max_boid_speed = current_sky.max_boid_speed
    new_sky.proximity = current_sky.proximity
    new_sky.separation_factor = current_sky.separation_factor
    new_sky.alignment_factor = current_sky.alignment_factor
    new_sky.cohesion_factor = current_sky.cohesion_factor

    new_boids = []
    for b in current_sky.boids:
        pos_copy = OrderedPair(b.position.x, b.position.y)
        vel_copy = OrderedPair(b.velocity.x, b.velocity.y)
        acc_copy = OrderedPair(b.acceleration.x, b.acceleration.y)
        new_boids.append(Boid(pos_copy, vel_copy, acc_copy))

    new_sky.boids = new_boids
    return new_sky

