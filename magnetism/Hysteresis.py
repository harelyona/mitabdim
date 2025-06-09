import os
from typing import Tuple, Optional, List, Union
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import use

# Constants
DATA_SIZE = 0.5  # Size of scatter points
AXIS_LABEL_SIZE = 13
TITLE_SIZE = 13
LEGEND_SIZE = 8
AXIS_LOC = (0.94, 0.84)
TITLE_LOC = 0.96

use('TkAgg')


def extract_voltages(file: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Read a CSV file and return (times, v1, v2) as numpy arrays.
    Assumes:
      - Column 3 = time,
      - Column 4 = V1 (→ H),
      - Column 10 = V2 (→ B).
    """
    df = pd.read_csv(file)
    times = df.iloc[:, 3].values
    v1 = df.iloc[:, 4].values
    v2 = df.iloc[:, 10].values
    return times, v1, v2


def plot_config(ax, x_label: str, y_label: str, title: str):
    """
    Style the axes:
      - Move left/bottom spines to zero
      - Hide top/right spines
      - Add arrowheads on +x and +y
      - Draw a dashed grid
      - Place the legend outside on the right (two columns)
      - Label axes and set title
      - Use auto aspect so X and Y scale independently
    """
    ax.legend(fontsize=LEGEND_SIZE, bbox_to_anchor=(1.02, 1), loc='upper left', ncol=2)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.plot((1, 0), (0, 0), '>k', transform=ax.transAxes)
    ax.plot((0, 0), (1, 0), '^k', transform=ax.transAxes)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel(x_label, fontsize=16, labelpad=10, x=AXIS_LOC[0])
    ax.set_ylabel(y_label, fontsize=16, labelpad=10, y=AXIS_LOC[1])
    ax.set_title(title, fontsize=TITLE_SIZE, y=TITLE_LOC)
    ax.set_aspect('auto')


def _parse_resistance_from_filename(fname: str) -> Optional[int]:
    """
    Extract any digits in `fname` to form an integer.
    Returns None if no digits found.
    Example: "1000Ω.csv" → 1000, "abc.csv" → None
    """
    digits = "".join(filter(str.isdigit, fname))
    if digits == "":
        return None
    return int(digits)


def plot_heshels(
    folder: str,
    save: bool = False,
    use_scatter: bool = False,
    resistances: Optional[List[int]] = None
):
    """
    Plot hysteresis loops from CSVs in `folder` (different resistances).

    Parameters:
    - folder: the directory containing CSV files
    - save: if True, save the figure to 'plots/{folder_basename}[_scatter].png'
    - use_scatter: if True, use a scatter plot; otherwise, line plot
    - resistances: optional list of integers (e.g. [0, 1000, 5000]).
      Only files whose numeric resistance matches one of these values are plotted.
      If None, all files in `folder` are used.

    Behavior:
    1. Gathers and sorts all CSV filenames, then filters by resistances if provided.
    2. Computes Hmax = max|V1| and Bmax = max|V2| across the selected files.
    3. Plots each loop in the chosen style (scatter vs. line).
    4. Fixes xlim = ±(Hmax + 5%) and ylim = ±(Bmax + 5%).
    5. If save=True, writes 'plots/{folder_basename}.png' or
       'plots/{folder_basename}_scatter.png' (when use_scatter=True).
    """
    # Create a new figure (8 × 5 inches)
    plt.figure(figsize=(8, 5))
    ax = plt.gca()

    # List and sort CSV filenames by any digits in the name
    all_files = sorted(os.listdir(folder), key=lambda f: int("".join(filter(str.isdigit, f)) or 0))

    # Filter by resistances if provided
    if resistances is not None:
        files = []
        for fname in all_files:
            R = _parse_resistance_from_filename(fname)
            if (R is not None) and (R in resistances):
                files.append(fname)
    else:
        files = all_files

    if not files:
        raise ValueError(f"No matching files in '{folder}' for resistances={resistances}")

    # Determine Hmax and Bmax over selected files
    Hmax = 0.0
    Bmax = 0.0
    for fname in files:
        _, v1, v2 = extract_voltages(os.path.join(folder, fname))
        Hmax = max(Hmax, np.max(np.abs(v1)))
        Bmax = max(Bmax, np.max(np.abs(v2)))

    # Plot each loop
    for fname in files:
        _, v1, v2 = extract_voltages(os.path.join(folder, fname))
        R_val = _parse_resistance_from_filename(fname)
        label_text = f"{R_val} Ω" if R_val is not None else fname
        if use_scatter:
            ax.scatter(v1, v2, s=DATA_SIZE, alpha=0.7, label=label_text)
        else:
            ax.plot(v1, v2, linewidth=0.5, alpha=0.7, label=label_text)

    # Compute padding (5%) for each axis
    padding_H = 0.05 * Hmax
    padding_B = 0.05 * Bmax

    # Fix X‐ and Y‐limits explicitly
    ax.set_xlim(-Hmax - padding_H, Hmax + padding_H)
    ax.set_ylim(-Bmax - padding_B, Bmax + padding_B)

    # Style the plot
    # new:
    plot_config(ax, "$H\\,[V]$", "$B\\,[V]$", f"Hysteresis loops for {folder}")

    # Save figure if requested, naming it after the folder
    if save:
        os.makedirs("plots", exist_ok=True)
        base = os.path.basename(folder)
        safe_name = base.replace(os.sep, "_")
        suffix = "_scatter" if use_scatter else ""
        out_path = f"plots{os.sep}{safe_name}{suffix}.png"
        plt.savefig(out_path, dpi=300, bbox_inches='tight')

    plt.show()


###############################################################################
# Example calls for Task 1:
###############################################################################
if __name__ == "__main__":
    plot_heshels("different R material 1", save=True, use_scatter=False, resistances=None)
    plot_heshels(
        folder="different R material 1",
        save=True,
        use_scatter=True,
        resistances=[0, 1300, 2600, 3300, 7500 , 14000]
    )
    plot_heshels("different R material 2", save=True, use_scatter=False, resistances=None)
    plot_heshels(
        folder="different R material 2",
        save=True,
        use_scatter=True,
        resistances=[0, 1000, 2000, 3000, 7000, 12000]
    )
    plot_heshels("different R material 3", save=True, use_scatter=False, resistances=None)
    plot_heshels(
        folder="different R material 3",
        save=True,
        use_scatter=True,
        resistances=[0, 1000, 4000, 6000, 8000, 12000]
    )
    plot_heshels("different R material 1 2 plates", save=True, use_scatter=False, resistances=None)
    plot_heshels(
        folder="different R material 1 2 plates",
        save=True,
        use_scatter=True,
        resistances=[0, 1000, 2000, 4000, 5000, 6000]
    )

###############################################################################
# Task 2: Six‐panel grid for “heshel vs plates” in hotpink, with titles "material {R_val}"
###############################################################################
def plot_heshel_plates_grid(
    folder: str,
    save: bool = False,
    plate_resistances: Optional[List[int]] = None,
    use_scatter: bool = False
):
    """
    Plot up to six hysteresis loops from `folder` (different plates, same resistance),
    each on its own subplot (2×3 grid). All subplots share the same x/y limits.
    - color set to 'hotpink'
    - subplot titles formatted as "material {R_val}"
    """
    all_files = sorted(os.listdir(folder), key=lambda f: int("".join(filter(str.isdigit, f)) or 0))

    if plate_resistances is not None:
        selected = []
        for fname in all_files:
            R = _parse_resistance_from_filename(fname)
            if (R is not None) and (R in plate_resistances):
                selected.append(fname)
        files = selected[:6]
    else:
        files = all_files[:6]

    if not files:
        raise ValueError(f"No matching plate files in '{folder}' for plate_resistances={plate_resistances}")

    Hmax = 0.0
    Bmax = 0.0
    for fname in files:
        _, v1, v2 = extract_voltages(os.path.join(folder, fname))
        Hmax = max(Hmax, np.max(np.abs(v1)))
        Bmax = max(Bmax, np.max(np.abs(v2)))

    padding_H = 0.05 * Hmax
    padding_B = 0.05 * Bmax

    fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)
    axes = axes.flatten()

    for idx, fname in enumerate(files):
        ax = axes[idx]
        _, v1, v2 = extract_voltages(os.path.join(folder, fname))

        R_val = _parse_resistance_from_filename(fname)
        title_text = f"material {R_val}" if R_val is not None else fname
        if use_scatter:
            ax.scatter(v1, v2, s=DATA_SIZE, alpha=0.7, color="hotpink")
        else:
            ax.plot(v1, v2, linewidth=0.5, alpha=0.7, color="hotpink")

        # Move spines and add arrowheads per subplot
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.plot((1, 0), (0, 0), '>k', transform=ax.transAxes)
        ax.plot((0, 0), (1, 0), '^k', transform=ax.transAxes)

        # Dashed grid
        ax.grid(True, which='both', linestyle='--', linewidth=0.3)

        # Fix identical axis limits
        ax.set_xlim(-Hmax - padding_H, Hmax + padding_H)
        ax.set_ylim(-Bmax - padding_B, Bmax + padding_B)

        # Title for each subplot
        ax.set_title(title_text, fontsize=10, pad=10)

    # Remove any unused axes if fewer than 6 plates
    for j in range(len(files), 6):
        fig.delaxes(axes[j])

    # Add single X/Y label and overall title
    fig.text(0.5, 0.04, "$H\\,[V]$", ha='center', va='center', fontsize=14)
    fig.text(0.07, 0.5, "$B\\,[V]$", ha='center', va='center', rotation='vertical', fontsize=14)
    fig.suptitle("Hysteresis Loops for Six Different Plates (Same Resistance)", fontsize=16, y=0.98)

    plt.tight_layout(rect=[0.03, 0.05, 1, 0.95])

    if save:
        os.makedirs("plots", exist_ok=True)
        base = os.path.basename(folder).replace(os.sep, "_")
        suffix = "_scatter_grid" if use_scatter else "_grid"
        out_path = f"plots{os.sep}{base}{suffix}.png"
        plt.savefig(out_path, dpi=300, bbox_inches='tight')

    plt.show()


###############################################################################
# Example call for Task 2 (six‐panel grid with scatter in hotpink):
###############################################################################
if __name__ == "__main__":
    plot_heshel_plates_grid(
        folder="different materials same R",
        save=True,
        plate_resistances=[9, 3, 1, 7, 5, 4],
        use_scatter=True
    )
    plot_heshels("different materials same R", save=True, use_scatter=False, resistances=None)