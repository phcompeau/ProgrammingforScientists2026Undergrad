
from typing import Iterable
from pathlib import Path
import csv

# --- Reading utilities -------------------------------------------------------

def read_frequency_map_from_file(filename: str) -> dict[str, int]:
    """
    Read a frequency map from a text file.

    Each non-empty, non-comment line should be one of:
      - "pattern<TAB>count"
      - "pattern,count"
      - "pattern"                (defaults to count=1)

    Lines starting with '#' are ignored.

    Parameters
    ----------
    filename : str
        Path to the input file.

    Returns
    -------
    dict[str, int]
        A frequency map: pattern -> count.
    """
    freq: dict[str, int] = {}

    p = Path(filename)
    with p.open("r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            if s.startswith("#"):
                continue

            key: str
            cnt: int

            if "\t" in s:
                parts = s.split("\t", 1)
                key = parts[0]
                try:
                    cnt = int(parts[1].strip())
                except ValueError:
                    # Skip lines with invalid counts
                    continue
            elif "," in s:
                parts = s.split(",", 1)
                key = parts[0]
                try:
                    cnt = int(parts[1].strip())
                except ValueError:
                    continue
            else:
                key = s
                cnt = 1

            # accumulate
            existing = freq.get(key, 0)
            freq[key] = existing + cnt

    return freq


def read_samples_from_directory(directory: str) -> dict[str, dict[str, int]]:
    """
    Read all files within a directory as separate samples.

    The sample name is the file's basename without extension.

    Parameters
    ----------
    directory : str
        Path to a directory containing sample files.

    Returns
    -------
    dict[str, dict[str, int]]
        Mapping: sample_name -> frequency map.
    """
    out: dict[str, dict[str, int]] = {}

    d = Path(directory)
    for path in sorted(d.iterdir()):
        if path.is_file():
            name = path.stem
            freq = read_frequency_map_from_file(str(path))
            out[name] = freq

    return out


# --- Writing utilities -------------------------------------------------------

def write_beta_diversity_matrix_to_file(
    mtx: list[list[float]],
    sample_names: list[str],
    filename: str
) -> None:
    """
    Write a square distance matrix to CSV with a leading header row/column.

    Parameters
    ----------
    mtx : list[list[float]]
        Square distance matrix aligned with `sample_names`.
    sample_names : list[str]
        Names of samples corresponding to matrix rows/columns.
    filename : str
        Output CSV path.
    """
    p = Path(filename)
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)

        # header row
        header: list[str] = [""]
        i = 0
        while i < len(sample_names):
            header.append(sample_names[i])
            i += 1
        w.writerow(header)

        # rows
        r = 0
        while r < len(sample_names):
            row: list[str] = [sample_names[r]]
            c = 0
            while c < len(mtx[r]):
                row.append(f"{mtx[r][c]:.6f}")
                c += 1
            w.writerow(row)
            r += 1


def write_simpsons_map_to_file(simpson: dict[str, float], filename: str) -> None:
    """
    Write per-sample Simpson's index values to CSV.

    Parameters
    ----------
    simpson : dict[str, float]
        Mapping: sample_name -> Simpson's index.
    filename : str
        Output CSV path.
    """
    p = Path(filename)
    with p.open("w", encoding='utf-8', newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample", "simpsons_index"])

        # deterministic order
        names = list(simpson.keys())
        names.sort()

        i = 0
        while i < len(names):
            name = names[i]
            w.writerow([name, f"{simpson[name]:.6f}"])
            i += 1