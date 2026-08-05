import math
from datatypes import Universe, Body, OrderedPair


# Simulation Code

def simulate_gravity(initial_universe: Universe, num_gens: int, time: float) -> list[Universe]:
    """
    Simulate an N-body system for a fixed number of generations.

    Args:
        initial_universe: The starting state of the universe.
        num_gens: Number of simulation steps to advance (>= 0).
        time: Time step (Δt) between generations (> 0).

    Returns:
        A list of Universe snapshots of length num_gens + 1.
    """
    # TODO: add code here
    pass


def update_universe(current_universe: Universe, time: float) -> Universe:
    """
    Advance the universe by a single time step.

    Uses a velocity-Verlet style update: compute new accelerations from the
    current state, then advance velocity and position accordingly.

    Args:
        current_universe: Universe state at the current time.
        time: Time step (Δt) to advance.

    Returns:
        A new Universe instance representing the next state.
    """

    # TODO: add code here
    pass

def update_acceleration(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute the body's acceleration from the net gravitational force.

    Uses:
        a = F / m (Newton's second law)

    Args:
        current_universe (Universe): The universe containing all bodies that
            contribute gravitational force.
        b (Body): The body whose acceleration is being computed.

    Returns:
        OrderedPair: A 2D vector (ax, ay) representing the updated acceleration.
    """

    # TODO: add code here
    pass

def update_velocity(b: Body, old_acceleration: OrderedPair, time: float) -> OrderedPair:
    """
    Update velocity using average acceleration over the step.

    Formula:
        v_{t+Δt} = v_t + 0.5 * (a_t + a_{t+Δt}) * Δt

    Args:
        b (Body): The body whose velocity is being updated. Must have
            a `velocity` attribute (OrderedPair) and a current 
            `acceleration` attribute (OrderedPair).
        old_acceleration (OrderedPair): The acceleration of the body at 
            the previous time step.
        time (float): The time step Δt over which to update the velocity.

    Returns:
        OrderedPair: A new OrderedPair representing the updated velocity 
        components (vx, vy).
    """
    # TODO: add code here
    pass


def update_position(b: Body, old_acc: OrderedPair, old_vel: OrderedPair, time: float) -> OrderedPair:
    """
    Update position using constant-acceleration kinematics.

    Formula:
        p_{t+Δt} = p_t + v_t * Δt + 0.5 * a_t * Δt²

    Args:
        b (Body): The body whose position is being updated. Must have 
            a `position` attribute (OrderedPair).
        old_acc (OrderedPair): The acceleration of the body at the previous 
            time step.
        old_vel (OrderedPair): The velocity of the body at the previous 
            time step.
        time (float): The time step Δt over which to update the position. 
            Must be a positive value.

    Returns:
        OrderedPair: A new OrderedPair containing the updated position 
        components (px, py).
    """
    # TODO: add code here
    pass

def update_velocity(b: Body, old_acceleration: OrderedPair, time: float) -> OrderedPair:
    """
    Update velocity using average acceleration over the step.

    Formula:
        v_{t+Δt} = v_t + 0.5 * (a_t + a_{t+Δt}) * Δt

    Args:
        b (Body): The body whose velocity is being updated. Must have 
            a `velocity` attribute (OrderedPair) and a current 
            `acceleration` attribute (OrderedPair).
        old_acceleration (OrderedPair): The acceleration of the body at 
            the previous time step.
        time (float): The time step Δt over which to update the velocity. 
            Must be a positive value.

    Returns:
        OrderedPair: A new OrderedPair containing the updated velocity 
        components (vx, vy).
    """
    # TODO: add code here
    pass


def compute_net_force(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute the net gravitational force on a body from all other bodies.

    Args:
        current_universe (Universe): The universe containing all bodies. 
            Must have a list of bodies and a valid gravitational constant.
        b (Body): The body on which the net gravitational force is computed.

    Returns:
        OrderedPair: A 2D vector (x, y) representing the net gravitational 
        force acting on the given body.
    """
    # TODO: add code here
    pass


def compute_force(b1: Body, b2: Body, G: float) -> OrderedPair:
    """
    Compute the gravitational force exerted on one body by another.

    Args:
        b1 (Body): The body on which the force is acting.
        b2 (Body): The body exerting the gravitational force.
        G (float): Gravitational constant.

    Returns:
        OrderedPair: A 2D vector (x, y) representing the force exerted 
        on `b1` by `b2`.
    """
    # TODO: add code here
    pass

def distance(p1: OrderedPair, p2: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two position vectors.

    Args:
        p1 (OrderedPair): The first position vector.
        p2 (OrderedPair): The second position vector.

    Returns:
        float: The distance between p1 and p2.
    """
    # TODO: add code here
    pass

def copy_universe(current_universe: Universe) -> Universe:
    """
    Deep-copy a Universe (bodies and width). 
    The gravitational constant `G` is a class attribute and does not need to be copied.

    Args:
        current_universe (Universe): The universe to copy. Must contain 
            a list of bodies and a width value.

    Returns:
        Universe: A new Universe instance with deep-copied bodies and 
        the same width as the original.
    """
    # TODO: add code here
    pass


def copy_body(b: Body) -> Body:
    """
    Deep-copy a Body, including position, velocity, and acceleration.

    Args:
        b (Body): The body to copy. Must contain name, mass, radius, 
        position, velocity, acceleration, and color attributes.

    Returns:
        Body: A new Body instance with identical properties and 
        deep-copied OrderedPair objects for position, velocity, 
        and acceleration.
    """
    # TODO: add code here
    pass