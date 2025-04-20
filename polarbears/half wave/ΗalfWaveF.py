import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Plot constants
GRAPH_TITLE_SIZE = 20
DATA_POINTs_SIZE = 5
INTENSITY_LABEL = 'Intensity [V]'
DEG_LABEL = "Angle [Deg]"
DATA_COLOR = ["orange", "magenta", "red"]
LABELS = ["No Angle", "30° Angle", "50° Angle"]
FIGURE_SIZE = (8, 6)
AXIS_LABEL_SIZE = 20

matplotlib.use('TkAgg')

def measurement_uncertainty(file: str) -> float:
    """Extract measurement uncertainty from an Excel file"""
    df = pd.read_excel(file)
    intensities = df.iloc[6:, 1]
    mean = intensities.mean()
    max_intensity = intensities.max()
    min_intensity = intensities.min()
    return max(max_intensity - mean, mean - min_intensity)

def intensity_average(file: str) -> float:
    df = pd.read_excel(file)
    return df.iloc[6:, 1].mean()  # Column B starting from row 7


def extract_averages_from_folder(folder_path: str) -> tuple[list[float], list[float]]:
    files = os.listdir(folder_path)
    files = [f for f in files if f.endswith(".xlsx")]
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else f)

    means = []
    uncertainties = []
    for file in files:
        full_path = os.path.join(folder_path, file)
        means.append(intensity_average(full_path))
        uncertainties.append(measurement_uncertainty(full_path))
    return means, uncertainties


def cos2_fit_func(x, a, b, c):
    return a * np.cos(np.deg2rad(x - b))**2 + c


def plot_regular_with_fit(
    intensities_by_type: list[list[float]],
    uncertainties_by_type: list[list[float]]
):
    plt.figure(figsize=FIGURE_SIZE)

    angles_deg_list = [
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # No Angle
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # 30° Angle
    ]

    angle_uncertainty = 0.5  # degrees — set to a constant or make per-point if needed

    for i in range(2):  # Only No Angle and 30°
        angles_deg = angles_deg_list[i]
        intensities = intensities_by_type[i]
        uncertainties = uncertainties_by_type[i]
        label = LABELS[i]
        color = DATA_COLOR[i]

        def cos2_fit_func(x, a, b, c):
            return a * np.cos(np.deg2rad(x - b))**2 + c

        initial_guess = [0.001, 90, 0]
        bounds = ([0, 0, -1], [1, 180, 1])

        try:
            popt, _ = curve_fit(
                cos2_fit_func,
                angles_deg,
                intensities,
                p0=initial_guess,
                bounds=bounds
            )
        except RuntimeError:
            print(f"Fit failed for {label}")
            continue

        fine_x = np.linspace(min(angles_deg), max(angles_deg), 500)
        fitted_vals = cos2_fit_func(fine_x, *popt)

        # Styled errorbar plot
        plt.errorbar(
            angles_deg,
            intensities,
            xerr=angle_uncertainty,
            yerr=uncertainties,
            fmt='o',
            color=color,
            ecolor='black',        # Use your ERRORBARS_COLOR variable if defined
            elinewidth=1.5,
            capsize=5,
            capthick=1,
            label=f"{label} Data",
            ms=DATA_POINTs_SIZE
        )

        plt.plot(fine_x, fitted_vals, label=f"{label} Fit", color=color)

        a, b, c = popt
        print(f"{label} Fit Params:\n  a = {a:.6f}\n  center = {b:.2f}°\n  offset = {c:.6f}")

    plt.xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.title("Intensity vs Angle with Cos² Fit", fontsize=GRAPH_TITLE_SIZE)
    plt.legend()
    plt.tight_layout()
    plt.show()



def plot_polar(intensities_by_type: list[list[float]]):
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='polar')

    angles_deg_list = [
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # No Angle
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # 30° Angle
    ]

    for i in range(2):  # Skip 50° Angle
        angles_deg = angles_deg_list[i]
        angles_rad = np.deg2rad(angles_deg)
        intensities = intensities_by_type[i]

        # Mirror data for 0–360°
        full_angles = np.concatenate([angles_rad, angles_rad + np.pi])
        full_intensities = np.concatenate([intensities, intensities])

        ax.plot(full_angles, full_intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])

    ax.set_title("Polar Plot (0–360°)", fontsize=GRAPH_TITLE_SIZE)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()



# --- Run ---

folder_names = ["no angle", "30 angle", "50 angle"]
intensities = []
uncertainties = []

for folder in folder_names:
    means, errors = extract_averages_from_folder(folder)
    intensities.append(means)
    uncertainties.append(errors)

plot_regular_with_fit(intensities, uncertainties)
#plot_polar(intensities[:2])  # Optional
