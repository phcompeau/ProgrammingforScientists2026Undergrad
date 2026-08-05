import math
from datatypes import Universe, Body, OrderedPair


# ------------------------- Validation Helpers -------------------------

def _is_finite_number(x: float) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)

def _validate_pair(p: OrderedPair, name: str) -> None:
    if not isinstance(p, OrderedPair):
        raise TypeError(f"{name} must be an OrderedPair")
    if not _is_finite_number(p.x) or not _is_finite_number(p.y):
        raise ValueError(f"{name} must contain finite numeric components")

def _validate_body(b: Body, idx_hint: str = "") -> None:
    if not isinstance(b, Body):
        raise TypeError(f"Body{idx_hint} must be a Body")
    if not _is_finite_number(b.mass) or b.mass <= 0:
        raise ValueError(f"Body{idx_hint}.mass must be a positive finite number")
    if not _is_finite_number(b.radius) or b.radius < 0:
        raise ValueError(f"Body{idx_hint}.radius must be a nonnegative finite number")
    _validate_pair(b.position, f"Body{idx_hint}.position")
    _validate_pair(b.velocity, f"Body{idx_hint}.velocity")
    _validate_pair(b.acceleration, f"Body{idx_hint}.acceleration")

def _validate_universe(u: Universe) -> None:
    if not isinstance(u, Universe):
        raise TypeError("initial_universe/current_universe must be a Universe")
    if not _is_finite_number(u.width) or u.width <= 0:
        raise ValueError("Universe.width must be a positive finite number")
    if not isinstance(u.bodies, list):
        raise TypeError("Universe.bodies must be a list[Body]")
    for i, b in enumerate(u.bodies):
        _validate_body(b, idx_hint=f"[{i}]")

def _validate_time_step(time: float) -> None:
    if not _is_finite_number(time) or time <= 0:
        raise ValueError("time step (Δt) must be a positive finite number")

def _validate_num_gens(num_gens: int) -> None:
    if not isinstance(num_gens, int) or num_gens < 0:
        raise ValueError("num_gens must be an integer >= 0")

def _validate_gravitational_constant(G: float) -> None:
    if not _is_finite_number(G) or G <= 0:
        raise ValueError("Universe.gravitational_constant must be a positive finite number")


# ------------------------- Simulation API -------------------------

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
    _validate_universe(initial_universe)
    _validate_num_gens(num_gens)
    _validate_time_step(time)
    _validate_gravitational_constant(Universe.gravitational_constant)

    time_points = [initial_universe]

    # range from 1 to num_gens, and call update_universe to fill time_points[i]
    for i in range(1, num_gens + 1):
        updated = update_universe(time_points[i - 1], time)
        time_points.append(updated)

    return time_points


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
    _validate_universe(current_universe)
    _validate_time_step(time)
    _validate_gravitational_constant(Universe.gravitational_constant)

    new_universe = copy_universe(current_universe)

    # Update every body in the cloned universe based on forces from current_universe
    for b in new_universe.bodies:
        old_acc, old_vel = b.acceleration, b.velocity
        b.acceleration = update_acceleration(current_universe, b)
        b.velocity = update_velocity(b, old_acc, time)
        b.position = update_position(b, old_acc, old_vel, time)

    return new_universe


def update_velocity(b: Body, old_acceleration: OrderedPair, time: float) -> OrderedPair:
    """
    Update velocity using average acceleration over the step.

    v_{t+Δt} = v_t + 0.5 * (a_t + a_{t+Δt}) * Δt
    """
    _validate_body(b)
    _validate_pair(old_acceleration, "old_acceleration")
    _validate_time_step(time)

    vx = b.velocity.x + 0.5 * (b.acceleration.x + old_acceleration.x) * time
    vy = b.velocity.y + 0.5 * (b.acceleration.y + old_acceleration.y) * time
    return OrderedPair(vx, vy)


def update_position(b: Body, old_acc: OrderedPair, old_vel: OrderedPair, time: float) -> OrderedPair:
    """
    Update position using constant-acceleration kinematics.

    p_{t+Δt} = p_t + v_t * Δt + 0.5 * a_t * Δt^2
    """
    _validate_body(b)
    _validate_pair(old_acc, "old_acc")
    _validate_pair(old_vel, "old_vel")
    _validate_time_step(time)

    px = b.position.x + old_vel.x * time + 0.5 * old_acc.x * time * time
    py = b.position.y + old_vel.y * time + 0.5 * old_acc.y * time * time
    return OrderedPair(px, py)


def update_acceleration(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute acceleration from the net gravitational force on a body (a = F / m).
    """
    _validate_universe(current_universe)
    _validate_body(b)
    _validate_gravitational_constant(Universe.gravitational_constant)

    force = compute_net_force(current_universe, b)
    return OrderedPair(force.x / b.mass, force.y / b.mass)


def compute_net_force(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute the net gravitational force on a body from all other bodies.
    """
    _validate_universe(current_universe)
    _validate_body(b)
    _validate_gravitational_constant(Universe.gravitational_constant)

    net_force = OrderedPair(0.0, 0.0)
    G = Universe.gravitational_constant

    for cur_body in current_universe.bodies:
        if cur_body is b:
            continue
        # We validate bodies in _validate_universe, but be robust if lists change:
        _validate_body(cur_body)
        current_force = compute_force(b, cur_body, G)
        net_force.x += current_force.x
        net_force.y += current_force.y

    return net_force


def compute_force(b1: Body, b2: Body, G: float) -> OrderedPair:
    """
    Gravitational force exerted on b1 by b2.

    Newton's law: F = G * m1 * m2 / r^2, along the line b1→b2.
    """
    _validate_body(b1, idx_hint="(b1)")
    _validate_body(b2, idx_hint="(b2)")
    _validate_gravitational_constant(G)

    dx = b2.position.x - b1.position.x
    dy = b2.position.y - b1.position.y
    d = math.hypot(dx, dy)  # distance

    if d == 0.0:
        return OrderedPair(0.0, 0.0)

    F_mag = G * b1.mass * b2.mass / (d * d)
    return OrderedPair(F_mag * dx / d, F_mag * dy / d)


def copy_universe(current_universe: Universe) -> Universe:
    """
    Deep-copy a Universe (bodies and width). G is a class attribute.
    """
    _validate_universe(current_universe)
    new_bodies = [copy_body(b) for b in current_universe.bodies]
    return Universe(new_bodies, current_universe.width)


def copy_body(b: Body) -> Body:
    """
    Deep-copy a Body, including position, velocity, and acceleration.
    """
    _validate_body(b)
    return Body(
        b.name, b.mass, b.radius,
        OrderedPair(b.position.x, b.position.y),
        OrderedPair(b.velocity.x, b.velocity.y),
        OrderedPair(b.acceleration.x, b.acceleration.y),
        b.red, b.green, b.blue,
    )