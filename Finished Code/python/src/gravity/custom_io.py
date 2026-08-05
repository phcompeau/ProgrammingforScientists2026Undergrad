from datatypes import Body, OrderedPair, Universe


def parse_ordered_pair(line: str) -> OrderedPair:
    """
    Parse a string containing two comma-separated floats into an OrderedPair.

    Args:
        line: A string like "1.2, -3.4".

    Returns:
        An OrderedPair(x, y).

    Raises:
        ValueError: If the input cannot be parsed into exactly two floats.
    """
    line = line.replace("−", "-")  # normalize minus sign (copy/paste from docs)
    parts = line.split(",")
    if len(parts) != 2:
        raise ValueError(f"Invalid ordered pair: {line!r}")
    try:
        x = float(parts[0].strip())
        y = float(parts[1].strip())
    except ValueError as e:
        raise ValueError(f"Invalid ordered pair numeric values: {line!r}") from e
    return OrderedPair(x, y)


def parse_rgb(line: str) -> tuple[int, int, int]:
    """
    Parse a string containing three comma-separated integers into an RGB tuple.

    Args:
        line: A string like "255, 128, 64".

    Returns:
        A tuple (red, green, blue), each 0–255.

    Raises:
        ValueError: If the input cannot be parsed into exactly three integers.
    """
    parts = line.split(",")
    if len(parts) != 3:
        raise ValueError(f"Invalid RGB format: {line!r}")
    try:
        red = int(parts[0].strip())
        green = int(parts[1].strip())
        blue = int(parts[2].strip())
    except ValueError as e:
        raise ValueError(f"Invalid RGB numeric values: {line!r}") from e
    for c, name in ((red, "red"), (green, "green"), (blue, "blue")):
        if not (0 <= c <= 255):
            raise ValueError(f"RGB component {name} out of range [0,255]: {c}")
    return red, green, blue


def read_universe(filename: str) -> Universe:
    """
    Read a universe configuration file and construct a Universe object.

    Expected file format:
        Line 1: universe width (float)
        Line 2: gravitational constant (float)
        Then, for each body (6 lines per body):
            >BodyName
            r, g, b
            mass
            radius
            x, y
            vx, vy

    Args:
        filename: Path to the configuration file.

    Returns:
        A Universe populated with bodies and width.
        Also updates Universe.gravitational_constant globally.

    Raises:
        FileNotFoundError: If the file cannot be opened.
        ValueError: If the file contents are invalid or incomplete.
    """
    with open(filename, "r", encoding="utf-8") as file:
        # Keep non-empty, non-comment lines; strip BOM if present
        raw_lines = [line.rstrip("\n") for line in file]
    if raw_lines and raw_lines[0].startswith("\ufeff"):
        raw_lines[0] = raw_lines[0].lstrip("\ufeff")

    lines = [ln.strip() for ln in raw_lines if ln.strip() and not ln.lstrip().startswith("#")]
    if len(lines) < 2:
        raise ValueError("Universe file must have at least two lines: width and G.")

    # Line 1: width
    try:
        width = float(lines[0])
    except ValueError as e:
        raise ValueError(f"Invalid universe width on line 1: {lines[0]!r}") from e
    if width <= 0:
        raise ValueError(f"Universe width must be > 0, got {width}")

    # Line 2: gravitational constant (class attribute)
    try:
        g_const = float(lines[1])
    except ValueError as e:
        raise ValueError(f"Invalid gravitational constant on line 2: {lines[1]!r}") from e
    if g_const <= 0:
        raise ValueError(f"Gravitational constant must be > 0, got {g_const}")
    Universe.gravitational_constant = g_const

    bodies: list[Body] = []

    # Each body consumes 6 lines. Track original line numbers for better errors.
    i = 2
    while i < len(lines):
        # Expect name line starting with ">"
        if not lines[i].startswith(">"):
            raise ValueError(f"Expected body name starting with '>' at line {i+1}: {lines[i]!r}")
        name = lines[i][1:].strip()
        if not name:
            raise ValueError(f"Empty body name at line {i+1}")

        # Ensure there are enough lines left
        if i + 5 >= len(lines):
            raise ValueError(f"Incomplete body block for '{name}' starting at line {i+1}")

        # Parse RGB
        try:
            red, green, blue = parse_rgb(lines[i + 1])
        except ValueError as e:
            raise ValueError(f"Invalid RGB for '{name}' at line {i+2}: {e}") from e

        # Mass
        try:
            mass = float(lines[i + 2])
        except ValueError as e:
            raise ValueError(f"Invalid mass for '{name}' at line {i+3}: {lines[i+2]!r}") from e
        if mass <= 0:
            raise ValueError(f"Mass for '{name}' must be > 0, got {mass}")

        # Radius
        try:
            radius = float(lines[i + 3])
        except ValueError as e:
            raise ValueError(f"Invalid radius for '{name}' at line {i+4}: {lines[i+3]!r}") from e
        if radius < 0:
            raise ValueError(f"Radius for '{name}' must be >= 0, got {radius}")

        # Position and velocity
        try:
            position = parse_ordered_pair(lines[i + 4])
        except ValueError as e:
            raise ValueError(f"Invalid position for '{name}' at line {i+5}: {e}") from e

        try:
            velocity = parse_ordered_pair(lines[i + 5])
        except ValueError as e:
            raise ValueError(f"Invalid velocity for '{name}' at line {i+6}: {e}") from e

        body = Body(
            name, mass, radius,
            position, velocity, OrderedPair(0.0, 0.0),
            red, green, blue
        )
        bodies.append(body)
        i += 6

    return Universe(bodies, width)