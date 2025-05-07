import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

from Malos import *  # Assumes this includes: ANGLE_UNCERTAINTY, ERRORBARS_COLOR, CAPSIZE, DATA_POINTs_SIZE, plot_config, DEG_LABEL, INTENSITY_LABEL

VERTICAL_COLOR = "blue"
HORIZONTAL_COLOR = "hotpink"


def rp(angle_deg, nout):
    angle = np.deg2rad(angle_deg)
    nin = 1
    sin_t = nin / nout * np.sin(angle)
    sin_t = np.clip(sin_t, -1, 1)
    cos_t = np.sqrt(1 - sin_t ** 2)
    numerator = nout * np.cos(angle) - nin * cos_t
    denominator = nout * np.cos(angle) + nin * cos_t
    return numerator / denominator


def rs(angle_deg, nout):
    angle = np.deg2rad(angle_deg)
    nin = 1
    sin_t = nin / nout * np.sin(angle)
    sin_t = np.clip(sin_t, -1, 1)
    cos_t = np.sqrt(1 - sin_t ** 2)
    numerator = nin * np.cos(angle) - nout * cos_t
    denominator = nin * np.cos(angle) + nout * cos_t
    return numerator / denominator


def Rp(angle_deg, nout): return abs(rp(angle_deg, nout)) ** 2


def Rs(angle_deg, nout): return abs(rs(angle_deg, nout)) ** 2


def scaled_offset_Rp(angle_deg, scale, offset): return scale * Rp(angle_deg, 1.49) + offset


def scaled_offset_Rs(angle_deg, scale, offset): return scale * Rs(angle_deg, 1.49) + offset


def chi_squared(observed, expected, error):
    return np.sum(((observed - expected) / error) ** 2)


def brewster_angle(nin, nout):
    return np.rad2deg(np.arctan(nout / nin))


def print_fresnel_and_brewster():
    nout = 1.49
    angles = np.array([55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65])
    Rp_vals = Rp(angles, nout)
    Rs_vals = Rs(angles, nout)
    print("Fresnel coefficients near Brewster angle:")
    for a, rp_val, rs_val in zip(angles, Rp_vals, Rs_vals):
        print(f"Angle: {a}°, Rp: {rp_val:.4f}, Rs: {rs_val:.4f}")
    brewster_theoretical = brewster_angle(1, nout)
    brewster_fitted = brewster_angle(1, horizontal_n)
    print(f"Theoretical Brewster angle (n = {nout}): {brewster_theoretical:.2f}°")
    print(f"Fitted Brewster angle (n = {horizontal_n:.3f}): {brewster_fitted:.2f}°): {brewster_angle(1, nout):.2f}°")


def plot_fresnel_with_and_without_brewster():
    x_fit = np.linspace(min(angles), max(angles), 1000)

    # Plot 1: With Brewster angle line
    plt.figure(figsize=FIGURE_SIZE)
    plt.plot(x_fit, scaled_offset_Rp(x_fit, horizontal_scale, horizontal_offset), color="pink", label="Rp fit")
    plt.plot(x_fit, scaled_offset_Rs(x_fit, vertical_scale, vertical_offset), color="lightblue", label="Rs fit")
    plt.errorbar(angles, horizontal_intensities / np.max(horizontal_intensities), xerr=ANGLE_UNCERTAINTY,
                 yerr=horizontal_uncertainties / np.max(horizontal_intensities), fmt='s', color=HORIZONTAL_COLOR,
                 capsize=CAPSIZE, label='Measured Horizontal', ms=DATA_POINTs_SIZE)
    plt.errorbar(angles[:len(vertical_intensities)], vertical_intensities / np.max(vertical_intensities),
                 xerr=ANGLE_UNCERTAINTY,
                 yerr=vertical_uncertainties / np.max(vertical_intensities), fmt='o', color=VERTICAL_COLOR,
                 capsize=CAPSIZE, label='Measured Vertical', ms=DATA_POINTs_SIZE)
    plt.axvline(x=brewster_angle(1, 1.49), color='gray', linestyle='--', label='Brewster angle')
    plt.title("Fresnel Fit with Brewster Angle", fontsize=GRAPH_TITLE_SIZE)
    plt.xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"figures{os.sep}fresnel_with_brewster.pdf")

    # Plot 2: Without Brewster line
    plt.figure(figsize=FIGURE_SIZE)
    plt.plot(x_fit, scaled_offset_Rp(x_fit, horizontal_scale, horizontal_offset), color="pink", label="Rp fit")
    plt.plot(x_fit, scaled_offset_Rs(x_fit, vertical_scale, vertical_offset), color="lightblue", label="Rs fit")
    plt.errorbar(angles, horizontal_intensities / np.max(horizontal_intensities), xerr=ANGLE_UNCERTAINTY,
                 yerr=horizontal_uncertainties / np.max(horizontal_intensities), fmt='s', color=HORIZONTAL_COLOR,
                 capsize=CAPSIZE, label='Measured Horizontal', ms=DATA_POINTs_SIZE)
    plt.errorbar(angles[:len(vertical_intensities)], vertical_intensities / np.max(vertical_intensities),
                 xerr=ANGLE_UNCERTAINTY,
                 yerr=vertical_uncertainties / np.max(vertical_intensities), fmt='o', color=VERTICAL_COLOR,
                 capsize=CAPSIZE, label='Measured Vertical', ms=DATA_POINTs_SIZE)
    plt.title("Fresnel Fit", fontsize=GRAPH_TITLE_SIZE)
    plt.xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"figures{os.sep}fresnel_no_brewster.pdf")

    plt.show()


def plot_horizontal(angles: np.ndarray, intensities: np.ndarray, uncertainties: np.ndarray, save=False):
    intensities = intensities / np.max(intensities)
    uncertainties = uncertainties / np.max(intensities)
    coefficients, cov_mat = curve_fit(scaled_offset_Rp, angles, intensities, p0=[0.9, 0.01], bounds=([0, -1], [10, 1]))
    x_fit = np.linspace(min(angles), max(angles), 1000)
    fit_vals = scaled_offset_Rp(angles, *coefficients)
    plt.plot(x_fit, scaled_offset_Rp(x_fit, *coefficients), color=HORIZONTAL_COLOR, label="horizontal fit")
    plt.errorbar(angles, intensities, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties, fmt='o', color=HORIZONTAL_COLOR,
                 ecolor=ERRORBARS_COLOR, capsize=CAPSIZE, label="horizontal data", ms=DATA_POINTs_SIZE)
    plot_config(DEG_LABEL, INTENSITY_LABEL, "Intensity vs Angle")
    if save:
        plt.savefig(f"figures{os.sep}horizontal.pdf", format="pdf")

    chi2 = chi_squared(intensities, fit_vals, uncertainties)
    print(f"Chi-squared (horizontal): {chi2:.2f}")
    return coefficients, cov_mat


def plot_vertical(angles: np.ndarray, intensities: np.ndarray, uncertainties: np.ndarray, save=False):
    intensities = intensities / np.max(intensities)
    uncertainties = uncertainties / np.max(intensities)
    coefficients, cov_mat = curve_fit(scaled_offset_Rs, angles, intensities, p0=[0.9, 0.01], bounds=([0, -1], [10, 1]))
    x_fit = np.linspace(min(angles), max(angles), 1000)
    fit_vals = scaled_offset_Rs(angles, *coefficients)
    plt.plot(x_fit, scaled_offset_Rs(x_fit, *coefficients), color=VERTICAL_COLOR, label="vertical fit")
    plt.errorbar(angles, intensities, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties, fmt='o', color=VERTICAL_COLOR,
                 ecolor=ERRORBARS_COLOR, capsize=CAPSIZE, label="vertical data", ms=DATA_POINTs_SIZE)
    plot_config(DEG_LABEL, INTENSITY_LABEL, "Intensity vs Angle")
    if save:
        plt.savefig(f"figures{os.sep}vertical.pdf", format="pdf")

    chi2 = chi_squared(intensities, fit_vals, uncertainties)
    print(f"Chi-squared (vertical): {chi2:.2f}")
    return coefficients, cov_mat


if __name__ == "__main__":
    angles = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 25, 20, 15, 10])
    brewster_angles = np.array([55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 50, 51, 52, 53, 54, 55])
    vertical_intensities = extract_averages_from_folder(f"refraction{os.sep}vertical")
    horizontal_intensities = extract_averages_from_folder(f"refraction{os.sep}horizontal")
    brewster_intensities = extract_averages_from_folder(f"refraction{os.sep}brewster")
    vertical_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}vertical")
    horizontal_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}horizontal")
    brewster_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}brewster")

    (vertical_scale, vertical_offset), vertical_cov = plot_vertical(angles, vertical_intensities,
                                                                    vertical_uncertainties, save=True)
    global vertical_n
    vertical_n = 1.49  # Fixed in fit, for completeness

    angles = np.append(angles, brewster_angles)
    horizontal_intensities = np.append(horizontal_intensities, brewster_intensities)
    horizontal_uncertainties = np.append(horizontal_uncertainties, brewster_uncertainties)
    (horizontal_scale, horizontal_offset), horizontal_cov = plot_horizontal(angles, horizontal_intensities,
                                                                            horizontal_uncertainties, save=True)
    global horizontal_n
    horizontal_n = 1.49  # Fixed in fit, but needed for derived Brewster

    print(f"Vertical fit: scale = {vertical_scale:.3e}, offset = {vertical_offset:.3e}")
    print(f"Horizontal fit: scale = {horizontal_scale:.3e}, offset = {horizontal_offset:.3e}")

    print_fresnel_and_brewster()
    plot_fresnel_with_and_without_brewster()

    plt.show()

