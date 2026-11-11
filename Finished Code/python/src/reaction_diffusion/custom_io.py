"""
custom_io.py

Loading and saving particle configurations and reaction tables.

Reaction table CSV format
--------------------------
A reaction table is a list of directives plus a sparse list of contact
reactions. Each species must declare its own diffusion rate; reactions
list only the (catalyst, substrate) pairs that actually do something.

Directives (one per line, in any order):
    diffusion,<species>,<rate>             -- step length per random-walk tick
    name,<species>,<string>                -- display name (optional; defaults "Species N")
    color,<species>,<r>,<g>,<b>            -- particle color (RGB ints 0-255)
    background,<r>,<g>,<b>                 -- canvas background (optional; defaults white)
    birth,<species>,<rate>                 -- spontaneous spawn (per batch)
    death,<species>,<rate>                 -- spontaneous removal (per batch)
    spontaneous,<from>,<to>,<rate>         -- contact-free conversion

Reaction rows (4 numbers each):
    <catalyst>,<substrate>,<product>,<rate>
        -- when species <catalyst> contacts species <substrate>, the
           substrate becomes species <product> with the given per-contact
           probability. The catalyst is unchanged.

The number of species is inferred from the diffusion directives, which
must cover species 0..N-1 exactly once. Self-meetings are allowed (i==j).
Listing the same (catalyst, substrate) pair more than once is an error.

Example (3-species rock-paper-scissors with rate 1.0):

    diffusion,0,8
    diffusion,1,8
    diffusion,2,8
    color,0,160,160,160
    color,1,76,155,232
    color,2,232,105,76
    background,18,18,31
    0,2,0,1.0     # rock beats scissors
    1,0,1,1.0     # paper beats rock
    2,1,2,1.0     # scissors beats paper

Particle CSV format
--------------------
First line:  # width=<float> height=<float>
Header row:  x,y,species,radius,diffusion_rate
Data rows:   one particle per row
"""

import csv
import os
import random

from datatypes import (
    OrderedPair, Particle, ReactionTable,
    ContactReaction, UnaryReaction, BirthReaction, DeathReaction,
)


def load_reaction_table(path: str) -> ReactionTable:
    """Load a reaction table from a CSV file.

    Args:
        path: Path to the reaction table CSV.

    Returns:
        ReactionTable with table, num_species, diffusion_rates, colors,
        and any unary/birth/death directives populated.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is malformed, references unknown species,
                    or lists the same (catalyst, substrate) twice.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Reaction table not found: '{path}'")

    color_map:        dict[int, tuple[int, int, int]] = {}
    name_map:         dict[int, str]                  = {}
    background_color: tuple[int, int, int]            = (255, 255, 255)
    diffusion_map:    dict[int, float]                = {}
    reactions:        list[ContactReaction]           = []
    unary_reactions:  list[UnaryReaction]             = []
    birth_reactions:  list[BirthReaction]             = []
    death_reactions:  list[DeathReaction]             = []

    # Track which species have already been claimed by each kind of unary
    # rule. Each species is allowed at most one birth, one death, and one
    # spontaneous-conversion rule -- this constraint lets the simulation
    # loop process them without "first match wins" branching.
    birth_species_seen: set[int] = set()
    death_species_seen: set[int] = set()
    unary_from_seen:    set[int] = set()

    # First pass: read every line of the file, drop blanks and full-line
    # comments (anything starting with `#`), and collect the rest. Done as
    # a separate pass so the CSV reader sees only data and directive lines.
    with open(path, "r", newline="") as f:
        raw_lines: list[str] = []
        for raw in f.read().splitlines():
            line = raw.strip()
            if len(line) > 0 and not line.startswith("#"):
                raw_lines.append(raw)

    # Second pass: parse each line as CSV. The first field is the keyword
    # ("diffusion", "color", "name", "background", "birth", "death",
    # "spontaneous") which selects the directive's parser. Anything else
    # is treated as a contact-reaction row.
    reader = csv.reader(raw_lines)
    for row in reader:
        fields: list[str] = []
        for field in row:
            stripped = field.strip()
            # Drop trailing inline comments like "1,0,1,0.1   # rabbit eats grass".
            if "#" in stripped:
                stripped = stripped.split("#", 1)[0].strip()
            if len(stripped) > 0:
                fields.append(stripped)

        # Skip rows that ended up empty (all fields were stripped away).
        if len(fields) > 0:
            key = fields[0]

            if key == "diffusion":
                species, rate = parse_species_rate(fields, "diffusion")
                if species in diffusion_map:
                    raise ValueError(
                        f"Duplicate diffusion directive for species {species}."
                    )
                diffusion_map[species] = rate
            elif key == "color":
                species, rgb = parse_species_rgb(fields, "color")
                if species in color_map:
                    raise ValueError(
                        f"Duplicate color directive for species {species}."
                    )
                color_map[species] = rgb
            elif key == "name":
                species, name = parse_species_name(fields)
                if species in name_map:
                    raise ValueError(
                        f"Duplicate name directive for species {species}."
                    )
                name_map[species] = name
            elif key == "background":
                background_color = parse_rgb(fields, "background")
            elif key == "birth":
                species, rate = parse_species_rate(fields, "birth")
                if species in birth_species_seen:
                    raise ValueError(
                        f"Duplicate birth rule for species {species}."
                    )
                birth_species_seen.add(species)
                birth_reactions.append(BirthReaction(rate=rate, species=species))
            elif key == "death":
                species, rate = parse_species_rate(fields, "death")
                if species in death_species_seen:
                    raise ValueError(
                        f"Duplicate death rule for species {species}."
                    )
                death_species_seen.add(species)
                death_reactions.append(DeathReaction(rate=rate, species=species))
            elif key == "spontaneous":
                from_s, to_s, rate = parse_spontaneous(fields)
                if from_s in unary_from_seen:
                    raise ValueError(
                        f"Duplicate spontaneous rule for source species {from_s}."
                    )
                unary_from_seen.add(from_s)
                unary_reactions.append(UnaryReaction(
                    rate=rate, from_species=from_s, to_species=to_s,
                ))
            else:
                catalyst, substrate, product, rate = parse_reaction(fields)
                reactions.append(ContactReaction(
                    rate=rate, catalyst=catalyst, substrate=substrate, product=product,
                ))

    # The diffusion directives also serve as our species census: the number
    # of species is the number of distinct diffusion entries, and they must
    # cover 0..N-1 with no gaps.
    if len(diffusion_map) == 0:
        raise ValueError(
            "Reaction file must declare a diffusion rate for each species."
        )

    n = len(diffusion_map)
    diffusion_rates: list[float] = []
    for s in range(n):
        if s not in diffusion_map:
            raise ValueError(
                f"Diffusion directives must cover species 0..{n - 1}; "
                f"missing species {s}."
            )
        diffusion_rates.append(diffusion_map[s])

    # Verify every species id mentioned in any rule is in range [0, n).
    validate_species_references(reactions, unary_reactions,
                                 birth_reactions, death_reactions, n)

    # Expand the sparse list of (catalyst, substrate, product, rate) tuples
    # into an N x N grid so the simulation loop can do O(1) lookups by
    # species pair.
    table = build_reaction_grid(reactions, n)

    # Colors are required if any are given (must cover all species). If
    # none are given, fall back to an auto-generated palette.
    colors: list[tuple[int, int, int]] = []
    if len(color_map) == 0:
        colors = auto_rgb_colors(n)
    else:
        for s in range(n):
            if s not in color_map:
                raise ValueError(
                    f"Color directives must cover species 0..{n - 1}; "
                    f"missing species {s}."
                )
            colors.append(color_map[s])

    # Names are optional: anything not given gets a "Species N" placeholder
    # so plot legends always have something to show.
    names: list[str] = []
    for s in range(n):
        if s in name_map:
            names.append(name_map[s])
        else:
            names.append(f"Species {s}")

    return ReactionTable(
        table             = table,
        num_species       = n,
        diffusion_rates   = diffusion_rates,
        names             = names,
        colors            = colors,
        background_color  = background_color,
        unary_reactions   = unary_reactions,
        birth_reactions   = birth_reactions,
        death_reactions   = death_reactions,
    )


def build_reaction_grid(reactions: list[ContactReaction],
                         n: int) -> list[list[ContactReaction | None]]:
    """Assemble an N x N grid of ContactReaction cells from a sparse reaction list.

    Cells not listed default to None (no reaction). Listing the same
    (catalyst, substrate) twice is an error.
    """
    # Start with an N x N grid of None ("no reaction here").
    table: list[list[ContactReaction | None]] = []
    for i in range(n):
        row: list[ContactReaction | None] = []
        for j in range(n):
            row.append(None)
        table.append(row)

    # Drop each declared reaction into its (catalyst, substrate) cell. We
    # track which cells we've filled so duplicates raise instead of silently
    # overwriting.
    seen: set[tuple[int, int]] = set()
    for r in reactions:
        if (r.catalyst, r.substrate) in seen:
            raise ValueError(
                f"Duplicate reaction for (catalyst={r.catalyst}, substrate={r.substrate})."
            )
        seen.add((r.catalyst, r.substrate))
        table[r.catalyst][r.substrate] = r

    return table


def validate_species_references(reactions:       list[ContactReaction],
                                 unary_reactions: list[UnaryReaction],
                                 birth_reactions: list[BirthReaction],
                                 death_reactions: list[DeathReaction],
                                 n: int) -> None:
    """Ensure every species id used in any directive is in [0, n)."""
    for r in reactions:
        for s in (r.catalyst, r.substrate, r.product):
            if s < 0 or s >= n:
                raise ValueError(
                    f"Reaction references species {s}, "
                    f"out of range [0, {n - 1}]."
                )
        if r.rate < 0.0:
            raise ValueError(f"Reaction rate must be >= 0, got {r.rate}.")

    for u in unary_reactions:
        for s in (u.from_species, u.to_species):
            if s < 0 or s >= n:
                raise ValueError(
                    f"spontaneous references species {s}, "
                    f"out of range [0, {n - 1}]."
                )

    for b in birth_reactions:
        if b.species < 0 or b.species >= n:
            raise ValueError(
                f"birth references species {b.species}, "
                f"out of range [0, {n - 1}]."
            )

    for d in death_reactions:
        if d.species < 0 or d.species >= n:
            raise ValueError(
                f"death references species {d.species}, "
                f"out of range [0, {n - 1}]."
            )


def parse_reaction(fields: list[str]) -> tuple[int, int, int, float]:
    """Parse a reaction row '<catalyst>,<substrate>,<product>,<rate>'."""
    if len(fields) != 4:
        raise ValueError(
            f"Reaction row must have 4 fields "
            f"(catalyst,substrate,product,rate), got: {fields}"
        )
    try:
        return (int(fields[0]), int(fields[1]),
                int(fields[2]), float(fields[3]))
    except ValueError:
        raise ValueError(f"Could not parse reaction row: {fields}")


def parse_species_rate(fields: list[str], name: str) -> tuple[int, float]:
    """Parse a directive of the form 'name,<species>,<rate>'."""
    if len(fields) != 3:
        raise ValueError(
            f"{name} line must have 3 fields ({name},species,rate), got: {fields}"
        )
    try:
        return int(fields[1]), float(fields[2])
    except ValueError:
        raise ValueError(f"Could not parse {name} fields in: {fields}")


def parse_species_name(fields: list[str]) -> tuple[int, str]:
    """Parse a directive of the form 'name,<species>,<string>'.

    The name string itself may contain spaces but not commas; everything
    after the species id is treated as the name (commas inside names are
    not supported because the file is comma-delimited).
    """
    if len(fields) != 3:
        raise ValueError(
            f"name line must have 3 fields (name,species,string), got: {fields}"
        )
    try:
        species = int(fields[1])
    except ValueError:
        raise ValueError(f"Could not parse species id in: {fields}")
    return species, fields[2]


def parse_species_rgb(fields: list[str],
                       name: str) -> tuple[int, tuple[int, int, int]]:
    """Parse a directive of the form 'name,<species>,<r>,<g>,<b>'."""
    if len(fields) != 5:
        raise ValueError(
            f"{name} line must have 5 fields ({name},species,r,g,b), got: {fields}"
        )
    try:
        species = int(fields[1])
        r = int(fields[2])
        g = int(fields[3])
        b = int(fields[4])
    except ValueError:
        raise ValueError(f"Could not parse {name} fields in: {fields}")
    validate_rgb(r, g, b, name)
    return species, (r, g, b)


def parse_rgb(fields: list[str], name: str) -> tuple[int, int, int]:
    """Parse a directive of the form 'name,<r>,<g>,<b>'."""
    if len(fields) != 4:
        raise ValueError(
            f"{name} line must have 4 fields ({name},r,g,b), got: {fields}"
        )
    try:
        r = int(fields[1])
        g = int(fields[2])
        b = int(fields[3])
    except ValueError:
        raise ValueError(f"Could not parse {name} fields in: {fields}")
    validate_rgb(r, g, b, name)
    return (r, g, b)


def validate_rgb(r: int, g: int, b: int, name: str) -> None:
    """Ensure r, g, b are integers in [0, 255]."""
    for component in (r, g, b):
        if component < 0 or component > 255:
            raise ValueError(
                f"{name} RGB component {component} out of range [0, 255]."
            )


def parse_spontaneous(fields: list[str]) -> tuple[int, int, float]:
    """Parse a directive of the form 'spontaneous,<from>,<to>,<rate>'."""
    if len(fields) != 4:
        raise ValueError(
            f"spontaneous line must have 4 fields "
            f"(spontaneous,from,to,rate), got: {fields}"
        )
    try:
        return int(fields[1]), int(fields[2]), float(fields[3])
    except ValueError:
        raise ValueError(f"Could not parse spontaneous fields in: {fields}")


def auto_rgb_colors(n: int) -> list[tuple[int, int, int]]:
    """Generate n visually distinct RGB colors."""
    palette: list[tuple[int, int, int]] = [
        ( 76, 155, 232), (232, 105,  76), ( 93, 191, 122), (184, 127, 217),
        (232, 196,  76), ( 76, 207, 207), (232,  76, 138), (160, 160, 160),
        (232, 122,  76), ( 76, 232, 176), (138,  76, 232), (232, 232,  76),
    ]
    colors: list[tuple[int, int, int]] = []
    for i in range(n):
        colors.append(palette[i % len(palette)])
    return colors


def load_particles(path: str) -> tuple[list[Particle], float, float]:
    """Load a particle configuration from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        (particles, width, height).
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: '{path}'")

    width:  float = -1.0
    height: float = -1.0
    particles: list[Particle] = []

    with open(path, "r", newline="") as f:
        first_line = f.readline().strip()
        if not first_line.startswith("# width="):
            raise ValueError(f"Expected '# width=<v> height=<v>', got: '{first_line}'")

        for part in first_line.lstrip("# ").split():
            if part.startswith("width="):
                width = float(part.split("=")[1])
            elif part.startswith("height="):
                height = float(part.split("=")[1])

        if width <= 0.0 or height <= 0.0:
            raise ValueError(f"Could not parse box size from: '{first_line}'")

        reader = csv.DictReader(f)
        for row in reader:
            particles.append(Particle(
                position       = OrderedPair(x=float(row["x"]), y=float(row["y"])),
                species        = int(row["species"]),
                radius         = float(row["radius"]),
                diffusion_rate = float(row["diffusion_rate"]),
            ))

    return particles, width, height


def make_random_particles(counts: list[int],
                          num_species: int,
                          width: float, height: float,
                          diffusion_rates: list[float],
                          radius: float = 5.0) -> list[Particle]:
    """Place particles randomly across the box.

    Args:
        counts:          Number of particles per species (length = num_species).
        num_species:     Total number of species.
        width:           Box width.
        height:          Box height.
        diffusion_rates: Step length per species (length = num_species).
        radius:          Particle radius.

    Returns:
        Flat list of all particles in species order.
    """
    particles: list[Particle] = []

    for species in range(num_species):
        for _ in range(counts[species]):
            position = OrderedPair(
                x = random.uniform(radius, width  - radius),
                y = random.uniform(radius, height - radius),
            )
            particles.append(Particle(
                position       = position,
                species        = species,
                radius         = radius,
                diffusion_rate = diffusion_rates[species],
            ))

    return particles


def make_clustered_particles(counts: list[int],
                             num_species: int,
                             width: float, height: float,
                             diffusion_rates: list[float],
                             radius: float = 5.0) -> list[Particle]:
    """Each species starts in its own vertical band of the box.

    Args:
        counts:          Number of particles per species (length = num_species).
        num_species:     Total number of species.
        width:           Box width.
        height:          Box height.
        diffusion_rates: Step length per species (length = num_species).
        radius:          Particle radius.

    Returns:
        Flat list of all particles in species order.
    """
    particles: list[Particle] = []
    band_width = width / num_species

    for species in range(num_species):
        x_lo = species * band_width
        x_hi = x_lo + band_width
        for _ in range(counts[species]):
            position = OrderedPair(
                x = random.uniform(x_lo + radius, x_hi - radius),
                y = random.uniform(radius, height - radius),
            )
            particles.append(Particle(
                position       = position,
                species        = species,
                radius         = radius,
                diffusion_rate = diffusion_rates[species],
            ))

    return particles
