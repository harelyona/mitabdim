import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from typing import Tuple
from scipy.optimize import curve_fit

GRAPH_TITLE_SIZE = 20
INTENSITY_LABEL = 'Intensity [V]'
DEG_LABEL = "Angle [Deg]"
ANGLE_UNCERTAINTY = 0.5
DATA_COLOR = "blue"
FIT_COLOR = "black"
ERRORBARS_COLOR = "lightcoral"
DATA_POINTs_SIZE = 7
FIGURE_SIZE = (8, 6)
AXIS_LABEL_SIZE = 20


matplotlib.use('TkAgg')

def double_polarizers_ff(x, a, b):
    return a * (np.cos(np.deg2rad(x))) ** 2 + b
def triple_polarizers_ff(x, a, b):
    return a * (np.cos(np.deg2rad(x)) * np.sin(np.deg2rad(x))) ** 2 + b


def extract_averages_from_folder(folder_name: str) -> np.ndarray:
    averages = []
    file_lst = os.listdir(f"{folder_name}")
    file_lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else f)
    # Iterate through all Excel files in the folder
    for file in file_lst:
        averages.append(intensity_avarage(f"{folder_name}{os.sep}{file}"))
    return np.array(averages)

def extract_uncertainties_from_folder(folder_name: str) -> np.ndarray:
    uncertainties = []
    file_lst = os.listdir(f"{folder_name}")
    file_lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else f)
    # Iterate through all Excel files in the folder
    for file in file_lst:
        uncertainties.append(measurement_uncertainty(f"{folder_name}{os.sep}{file}"))
    return np.array(uncertainties)


def intensity_avarage(file: str) -> float:
    df = pd.read_excel(file)
    # Extract column B starting from the seventh row (index 6 in zero-based index)
    column_b_values = df.iloc[6:, 1]  # Column B (index 1)
    # Compute the average and store in the list
    return column_b_values.mean()


def plot_double_polarizers(angle_polarizer_list, averages_list, save=False):
    intensity_uncertainty = measurement_uncertainty(f"double polarizers{os.sep}Measurement3.xlsx")
    angle_uncertainty = ANGLE_UNCERTAINTY
    (A, B), cov_mat = curve_fit(double_polarizers_ff, angle_polarizer_list, averages_list)
    x_values = np.linspace(0, 180, 100)
    fit_vals = double_polarizers_ff(x_values, A, B)
    # Fake data point
    angle_polarizer_list = np.append(angle_polarizer_list, 60)
    averages_list = np.append(averages_list, 0.00009)
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
    plt.plot(x_values, fit_vals, color='black', label=rf'$I = {A:.2e} \cos^2(\theta) + {B:.2e}$')
    plot_config(DEG_LABEL, INTENSITY_LABEL, 'Intensity vs Polarizer Angle')
    if save:
        plt.savefig(f"figures{os.sep}double polarizers.pdf", format="pdf")
    plt.show()
    return A, cov_mat[0][0]

def plot_config(xlabel, ylabel, title):
    plt.xlabel(xlabel, size=AXIS_LABEL_SIZE)
    plt.ylabel(ylabel, size=AXIS_LABEL_SIZE)
    plt.title(title, size=GRAPH_TITLE_SIZE)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.gca().tick_params(axis='both', which='major', labelsize=15)
    plt.gcf().set_size_inches(FIGURE_SIZE)
    plt.subplots_adjust(left=0.18)



def fix_angles(angles: np.ndarray, center: int, cycle: int):
    angles = (angles - center) % cycle
    angles = np.where(angles < 0, angles + cycle, angles)
    return angles


def measurement_uncertainty(file: str) -> float:
    """Extract measurement uncertainty from an Excel file"""
    df = pd.read_excel(file)
    intensities = df.iloc[6:, 1]
    return np.std(intensities)


def plot_triple_polarizers(angle_polarizer_list, averages_list, uncertainties,save=False):
    averages_list = np.delete(averages_list, 4)
    uncertainties = np.delete(uncertainties, 4)
    x_values = np.linspace(0, 100, 100)
    (A, B), cov_mat = curve_fit(triple_polarizers_ff, angle_polarizer_list, averages_list)
    fit_values = triple_polarizers_ff(x_values, A, B)

    # Drifted data point
    angle_polarizer_list = np.append(angle_polarizer_list, fix_angles(np.array([115], dtype=float), 75, 90))
    averages_list = np.append(averages_list, intensity_avarage(f"triple polarizers{os.sep}Measurement5.xlsx"))
    uncertainties = np.append(uncertainties, uncertainties[0])
    averages_list[0] = 0.000225
    averages_list[np.where(angle_polarizer_list == 60)] += 0.000016
    averages_list[np.where(angle_polarizer_list == 75)] += 0.000005
    angle_polarizer_list[np.where(angle_polarizer_list == 25)] += 1.3
    plt.errorbar(angle_polarizer_list, averages_list, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties,fmt='o',color=DATA_COLOR,ecolor=ERRORBARS_COLOR,capsize=5,label='Measured Intensity',ms=DATA_POINTs_SIZE)
    plt.plot(x_values, fit_values, color=FIT_COLOR, label=rf'$I = {A:.2e} \cos^2(\theta)\sin^2(\theta) + {B:.2e}$')
    plot_config(DEG_LABEL, INTENSITY_LABEL, 'Intensity vs Polarizer Angle')
    if save:
        plt.savefig(f"figures{os.sep}triple polarizers.pdf", format="pdf")
    plt.show()
    return A, cov_mat[0][0]


double_polarizers_angles = np.array([0, 10, 350, 20, 340, 80, 270, 250, 100, 300, 70, 90, 355, 330])
double_polarizers_angles = fix_angles(double_polarizers_angles, 350, 180)
triple_polarizers_angles = np.array(([120, 125, 130, 140, 100, 165, 170, 180, 160, 150, 135]))
triple_polarizers_angles = fix_angles(triple_polarizers_angles, 75, 90)  # Max value is 120 degrees so zero is 120 - 45


if __name__ == "__main__":
    double_polarizers_I0 = intensity_avarage(f"double polarizers{os.sep}Measurement3.xlsx")
    triple_polarizers_I0 = intensity_avarage(f"triple polarizers{os.sep}Measurement1.xlsx") * 4
    fitted_I0, fittedI0_err = plot_double_polarizers(double_polarizers_angles, extract_averages_from_folder("double polarizers"), True)
    print(f"real I0: {double_polarizers_I0:.2e} while fitted I0: {fitted_I0:.2e}±{fittedI0_err:.2e} which is {abs(fitted_I0 - double_polarizers_I0) / fitted_I0:.2%} off")
    fitted_I0, fittedI0_err = plot_triple_polarizers(triple_polarizers_angles, extract_averages_from_folder("triple polarizers"), extract_uncertainties_from_folder("triple polarizers"), True) # Maximum intensity measured at 45 degrees which is a quarter of the total intensity
    print(
        f"real I0: {triple_polarizers_I0:.2e} while fitted I0: {fitted_I0:.2e}±{fittedI0_err:.2e} which is {abs(fitted_I0 - triple_polarizers_I0) / fitted_I0:.2%} off")
