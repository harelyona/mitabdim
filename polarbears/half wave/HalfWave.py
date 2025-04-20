import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from typing import Tuple

# Plot constants
GRAPH_TITLE_SIZE = 20
INTENSITY_LABEL = 'Intensity [V]'
DEG_LABEL = "Angle [Deg]"
DATA_COLOR = ["blue", "green", "red"]
LABELS = ["No Angle", "30° Angle", "50° Angle"]
DATA_POINTs_SIZE = 5
FIGURE_SIZE = (8, 6)
AXIS_LABEL_SIZE = 20

matplotlib.use('TkAgg')


def intensity_average(file: str) -> float:
    df = pd.read_excel(file)
    # Extract column B starting from the seventh row (index 6 in zero-based index)
    column_b_values = df.iloc[6:, 1]  # Column B (index 1)
    # Compute the average and store in the list
    return column_b_values.mean()

def extract_averages_from_folder(folder_path: str) -> list[float]:
    files = os.listdir(folder_path)
    files = [f for f in files if f.endswith(".xlsx")]
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else f)
    return [intensity_average(os.path.join(folder_path, file)) for file in files]

def cos2_fit_func(x, a, b, c):
    return a * np.cos(np.deg2rad(x) - b)**2 + c


def plot_intensity_and_polar(intensities_by_type: list[list[float]]):
    angles_deg_all = [np.linspace(0, 180, len(intensities)) for intensities in intensities_by_type]
    angles_rad_all = [np.deg2rad(angles) for angles in angles_deg_all]

    # Create the figure and both axes separately
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, projection='polar')

    # Regular plot
    for i, (angles_deg, intensities) in enumerate(zip(angles_deg_all, intensities_by_type)):
        ax1.plot(angles_deg, intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])
    ax1.set_xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    ax1.set_ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    ax1.legend()
    ax1.set_title("Intensity vs Angle", fontsize=GRAPH_TITLE_SIZE)

    # Polar plot
    for i, (angles_rad, intensities) in enumerate(zip(angles_rad_all, intensities_by_type)):
        ax2.plot(angles_rad, intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])
    ax2.set_title("Polar Plot", fontsize=GRAPH_TITLE_SIZE)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

def plot_regular_with_fit(intensities_by_type: list[list[float]]):
    plt.figure(figsize=FIGURE_SIZE)

    angles_deg_list = [
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # No Angle
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # 30°
        [0, 10, 20, 30, 40, 120, 110, 100, 180, 190, 200, 210, 220],  # 50°
    ]

    initial_guesses = [
        [-0.01, 0, 0.0],  # No Angle
        [-0.1, 0.87, 0.1],   # 30°
        [-0.1, -0.13, 0.2],  # 50°
    ]
    bounds_list = [
        ([-0.1, -0.1, -1], [0.001, 1, 0]),  # No Angle
        ([-1, -np.pi, -np.inf], [-0.0001, np.pi, np.inf]),  # 30°
        ([-1, -np.pi, -np.inf], [-0.0001, np.pi, np.inf]),  # 50°
    ]

    for i, intensities in enumerate(intensities_by_type):
        angles_deg = angles_deg_list[i]
        initial_guess = initial_guesses[i]
        lower_bounds, upper_bounds = bounds_list[i]

        try:
            popt, _ = curve_fit(
                cos2_fit_func,
                angles_deg,
                intensities,
                p0=initial_guess,
                bounds=(lower_bounds, upper_bounds)
            )
        except RuntimeError:
            print(f"Fit failed for {LABELS[i]}")
            continue

        fitted_vals = cos2_fit_func(angles_deg, *popt)

        # Plot data and fit
        plt.plot(angles_deg, intensities, 'o', label=f"{LABELS[i]} Data", color=DATA_COLOR[i])
        plt.plot(angles_deg, fitted_vals, '-', label=f"{LABELS[i]} Fit", color=DATA_COLOR[i])

        # Print fitted parameters
        a, b, c = popt
        #phi_deg = np.rad2deg(phi_rad)
        #print(f"{LABELS[i]} Fit Params:\n  Amplitude a = {a:.3f}\n  Phase φ = {phi_deg:.2f}°\n  Offset c = {c:.3f}\n")
        print(a, b, c)

    plt.xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.title("Intensity vs Angle with Cos² Fit", fontsize=GRAPH_TITLE_SIZE)
    plt.legend()
    plt.tight_layout()
    plt.show()



def plot_polar(intensities_by_type: list[list[float]]):
    angles_rad_all = [np.deg2rad(np.linspace(0, 180, len(intensities))) for intensities in intensities_by_type]

    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='polar')

    for i, (angles_rad, intensities) in enumerate(zip(angles_rad_all, intensities_by_type)):
        ax.plot(angles_rad, intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])

    ax.set_title("Polar Plot", fontsize=GRAPH_TITLE_SIZE)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

folder_names = ["no angle", "30 angle", "50 angle"]
intensities = [extract_averages_from_folder(name) for name in folder_names]

plot_regular_with_fit(intensities)
# plot_polar(intensities)
