from datatypes import Body, OrderedPair, Universe


def read_universe(filename: str) -> Universe:
    """
    Read a universe configuration file and construct a Universe object.
    """
    if not isinstance(filename, str) or not filename.strip():
        raise TypeError("filename must be a non-empty string")

    with open(filename, "r", encoding="utf-8") as file:
        raw_lines: list[str] = [line.rstrip("\n") for line in file]

    if raw_lines and raw_lines[0].startswith("\ufeff"):
        raw_lines[0] = raw_lines[0].lstrip("\ufeff")

    lines: list[str] = []
    for ln in raw_lines:
        stripped = ln.strip()
        if stripped and not stripped.lstrip().startswith("#"):
            lines.append(stripped)

    if len(lines) < 2:
        raise ValueError("Universe file must have at least two lines: width and G.")

    width: float = float(lines[0])
    if width <= 0:
        raise ValueError(f"Universe width must be > 0, got {width}")

    g_const: float = float(lines[1])
    if g_const <= 0:
        raise ValueError(f"Gravitational constant must be > 0, got {g_const}")
    Universe.gravitational_constant = g_const

    bodies: list[Body] = []
    i: int = 2

    while i < len(lines):
        if not lines[i].startswith(">"):
            raise ValueError(f"Expected body name starting with '>' at line {i+1}: {lines[i]!r}")
        body_name: str = lines[i][1:].strip()
        if not body_name:
            raise ValueError(f"Empty body name at line {i+1}")

        if i + 5 >= len(lines):
            raise ValueError(f"Incomplete body block for '{body_name}' starting at line {i+1}")

        red, green, blue = parse_rgb(lines[i + 1])

        mass: float = float(lines[i + 2])
        if mass <= 0:
            raise ValueError(f"Mass for '{body_name}' must be > 0, got {mass}")

        radius: float = float(lines[i + 3])
        if radius < 0:
            raise ValueError(f"Radius for '{body_name}' must be >= 0, got {radius}")

        position: OrderedPair = parse_ordered_pair(lines[i + 4])
        velocity: OrderedPair = parse_ordered_pair(lines[i + 5])

        body = Body(
            name=body_name,
            mass=mass,
            radius=radius,
            position=position,
            velocity=velocity,
            acceleration=OrderedPair(0.0, 0.0),
            red=red,
            green=green,
            blue=blue,
        )
        bodies.append(body)
        i += 6

    return Universe(bodies, width)


def parse_ordered_pair(line: str) -> OrderedPair:
    """
    Parse 'x, y' into an OrderedPair.
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")

    line = line.replace("−", "-")  # normalize minus
    parts = line.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid ordered pair: {line!r}")

    x_str, y_str = parts[0].strip(), parts[1].strip()
    if not x_str or not y_str:
        raise ValueError(f"Invalid ordered pair (empty component): {line!r}")

    x: float = float(x_str)
    y: float = float(y_str)
    return OrderedPair(x, y)


def parse_rgb(line: str) -> tuple[int, int, int]:
    """
    Parse 'r, g, b' into a 3-tuple of ints in [0, 255].
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")

    parts = line.split(",")
    if len(parts) != 3:
        raise ValueError(f"Invalid RGB format: {line!r}")

    r_str, g_str, b_str = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if not r_str or not g_str or not b_str:
        raise ValueError(f"Invalid RGB format (empty component): {line!r}")

    red: int = int(r_str)
    green: int = int(g_str)
    blue: int = int(b_str)

    if not (0 <= red <= 255):
        raise ValueError(f"RGB component red out of range [0,255]: {red}")
    if not (0 <= green <= 255):
        raise ValueError(f"RGB component green out of range [0,255]: {green}")
    if not (0 <= blue <= 255):
        raise ValueError(f"RGB component blue out of range [0,255]: {blue}")

    return red, green, blue