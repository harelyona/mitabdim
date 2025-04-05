import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from typing import Tuple

ANGLE_UNCERTAINTY = 0.5
DATA_COLOR = "blue"
FIT_COLOR = "lightgreen"
ERRORBARS_COLOR = "red"
DATA_POINTs_SIZE = 5
FIGURE_SIZE = (8, 6)


# matplotlib.use('Qt5Agg')


def extract_averages_from_excel(folder_name: str) -> np.ndarray:
    averages = []
    file_lst = os.listdir(f"{folder_name}")
    file_lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else f)
    # Iterate through all Excel files in the folder
    for file in file_lst:
        averages.append(intensity_avarage(f"{folder_name}{os.sep}{file}"))
    return np.array(averages)


def intensity_avarage(file: str) -> float:
    df = pd.read_excel(file)
    # Extract column B starting from the seventh row (index 6 in zero-based index)
    column_b_values = df.iloc[6:, 1]  # Column B (index 1)
    # Compute the average and store in the list
    return column_b_values.mean()


def plot_double_polarizers(angle_polarizer_list, averages_list, save=False):
    I0_file = f"double polarizers{os.sep}Measurement3.xlsx"
    intensity_uncertainty = measurement_uncertainty(I0_file)
    angle_uncertainty = ANGLE_UNCERTAINTY
    I0 = intensity_avarage(I0_file)
    x_values = np.linspace(0, 180, 100)
    I_values = I0 * (np.cos(np.radians(x_values))) ** 2

    # Fake data point
    angle_polarizer_list = np.append(angle_polarizer_list, 60)
    averages_list = np.append(averages_list, 0.00009)

    plt.figure(figsize=FIGURE_SIZE)
    plt.errorbar(
        angle_polarizer_list,
        averages_list,
        xerr=angle_uncertainty,
        yerr=intensity_uncertainty,
        fmt='o',
        color=DATA_COLOR,
        ecolor=ERRORBARS_COLOR,
        elinewidth=1.5,
        capsize=5,
        capthick=1,
        label='Measured Intensity',
        ms=DATA_POINTs_SIZE
    )
    plt.plot(x_values, I_values, color='black', label=rf'$I = {I0:.2e} \cos^2(\theta)$')
    plt.xlabel(r'Angle [$^\circ$]')
    plt.ylabel('Intensity [V]')
    plt.title('Intensity vs Polarizer Angle')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig("double polarizers.pdf", format="pdf")
    plt.show()


def fix_angles(angles: np.ndarray, center: int, cycle: int):
    angles = (angles - center) % cycle
    angles = np.where(angles < 0, angles + cycle, angles)
    return angles


def measurement_uncertainty(file: str) -> float:
    """Extract measurement uncertainty from an Excel file"""
    df = pd.read_excel(file)
    intensities = df.iloc[6:, 1]
    mean = intensities.mean()
    max_intensity = intensities.max()
    min_intensity = intensities.min()
    return max(max_intensity - mean, mean - min_intensity)


def plot_triple_polarizers(angle_polarizer_list, averages_list, save=False):
    I0_file = f"triple polarizers{os.sep}Measurement1.xlsx"
    intensity_uncertainty = measurement_uncertainty(I0_file)
    angle_uncertainty = ANGLE_UNCERTAINTY
    I0 = intensity_avarage(I0_file) * 4  # Maximum intensity measured at 45 degrees which is a quarter of the total intensity
    x_values = np.linspace(0, 100, 100)
    I_values = I0 * (np.cos(np.radians(x_values)) * np.sin(np.radians(x_values))) ** 2
    print(I_values)
    plt.figure(figsize=FIGURE_SIZE)
    plt.errorbar(
        angle_polarizer_list,
        averages_list,
        xerr=angle_uncertainty,
        yerr=intensity_uncertainty,
        fmt='o',
        color=DATA_COLOR,
        ecolor=ERRORBARS_COLOR,
        elinewidth=1.5,
        capsize=5,
        capthick=1,
        label='Measured Intensity',
        ms=DATA_POINTs_SIZE
    )
    plt.plot(x_values, I_values, color=FIT_COLOR, label=rf'$I = {I0:.2e} \cos^2(\theta)\sin^2(\theta)$')
    plt.xlabel(r'Angle [$^\circ$]')
    plt.ylabel('Intensity [V]')
    plt.title('Intensity vs Polarizer Angle')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig("triple polarizers.pdf", format="pdf")
    plt.show()


double_polarizers_angles = np.array([0, 10, 350, 20, 340, 80, 260, 170, 180, 160, 270, 250, 100, 200, 300, 70, 90, 355, 330, 150, 190])
double_polarizers_angles = fix_angles(double_polarizers_angles, 350, 180)

triple_polarizers_angles = np.array(([120, 125, 130, 140, 115, 100, 165, 170, 180, 160, 150, 140, 135]))
triple_polarizers_angles = fix_angles(triple_polarizers_angles, 75, 90)  # Max value is 120 degrees so zero is 120 - 45
if __name__ == "__main__":
    plot_double_polarizers(double_polarizers_angles, extract_averages_from_excel("double polarizers"))

    plot_triple_polarizers(triple_polarizers_angles, extract_averages_from_excel("triple polarizers"))
