"""
plotting.py

Matplotlib chart of species populations over time.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datatypes import Particle, ReactionTable


def plot_species_counts(frames: list[list[Particle]],
                        table: ReactionTable,
                        output_path: str = "species_counts.png") -> None:
    """Plot the population of each species over time and save a PNG.

    Args:
        frames:      One snapshot (particle list) per recorded step.
        table:       ReactionTable (provides species count and colors).
        output_path: Output image path.
    """
    # counts[s] is a list of counts of species s over time, one entry per
    # recorded frame.
    counts: list[list[int]] = []
    for s in range(table.num_species):
        counts.append([])

    # For each frame, tally how many particles belong to each species and
    # append the per-species counts to the time series.
    for snapshot in frames:
        step_counts = [0] * table.num_species
        for p in snapshot:
            step_counts[p.species] += 1
        for s in range(table.num_species):
            counts[s].append(step_counts[s])

    steps = list(range(len(frames)))

    # Plot one line per species, using the species's own color (matplotlib
    # wants RGB floats in [0, 1] so we divide by 255) and its display name
    # in the legend.
    fig, ax = plt.subplots(figsize=(10, 4))
    for s in range(table.num_species):
        r, g, b = table.colors[s]
        ax.plot(steps, counts[s], color=(r / 255.0, g / 255.0, b / 255.0),
                linewidth=1.5, label=table.names[s])

    ax.set_xlabel("Step")
    ax.set_ylabel("Particle count")
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=120)
    plt.close(fig)
    print(f"  Species count plot saved to {output_path}")
