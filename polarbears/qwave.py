import matplotlib.pyplot as plt
import numpy as np

from Malos import *
def plot_q_wave(angles:np.ndarray, intensities:np.ndarray, uncertainties:np.ndarray, save=False):
    coefficients, cov_mat = np.polyfit(angles, intensities, 0, cov=True)
    ff = np.poly1d(coefficients)
    x_fit = np.linspace(min(angles), max(angles), 1000)
    average_intensity = np.average(q_wave_intensities)
    difference = cov_mat - average_intensity
    plt.axhline(y=average_intensity, color='black', label='Average Intensity')
    plt.errorbar(q_wave_angles, q_wave_intensities, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties, fmt='o', color=DATA_COLOR, ecolor=ERRORBARS_COLOR, capsize=5, label='Measured Intensity', ms=DATA_POINTs_SIZE)
    plot_config(DEG_LABEL, INTENSITY_LABEL, "Intensity vs Angle")

    if save:
        plt.savefig(f"figures{os.sep}q wave.pdf", format="pdf")
    plt.show()

    return coefficients, cov_mat


def plot_q_wave_polar(angles: np.ndarray, intensities: np.ndarray, uncertainties: np.ndarray, save=False):
    coefficients, cov_mat = np.polyfit(angles, intensities, 1, cov=True)
    ff = np.poly1d(coefficients)

    # Create x_fit from 0 to 360 degrees for a full circle
    x_fit = np.linspace(0, 360, 1000)

    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, polar=True)

    # Plot the fit line
    ax.plot(np.deg2rad(x_fit), ff(x_fit), color=FIT_COLOR, label=rf'$I = {coefficients[0]:.2e} \theta + {coefficients[1]:.2e}$')

    # Plot the measured data points with error bars
    ax.errorbar(np.deg2rad(angles), intensities,
                xerr=np.deg2rad(ANGLE_UNCERTAINTY), yerr=uncertainties,
                fmt='o', color=DATA_COLOR, ecolor=ERRORBARS_COLOR,
                capsize=5, label='Measured Intensity', ms=DATA_POINTs_SIZE)
    max_intensity = max(np.max(intensities), np.max(ff(x_fit)))
    ax.set_rlim(0, max_intensity * 1.2)  # 20% headroom above highest point
    # Match the polar plot configuration
    ax.set_theta_zero_location('E')  # 0° to the right
    ax.set_theta_direction(-1)       # Angles increase clockwise

    # Set title and legend
    ax.set_title("Intensity vs Angle", size=GRAPH_TITLE_SIZE)
    ax.legend(fontsize=LEGEND_SIZE)
    ax.grid(True)
    plt.tight_layout()

    if save:
        plt.savefig(f"figures{os.sep}q wave polar.pdf", format="pdf")
    plt.show()

    return coefficients, cov_mat


#q_wave_angles = np.array([340, 350, 0, 10, 20, 80, 90, 100, 250, 170, 180, 190])
q_wave_angles = np.array([340, 10, 40, 70, 100, 130, 160, 190, 210, 240, 270, 300])


if __name__ == "__main__":
    q_wave_uncertainties = extract_uncertainties_from_folder("q wave")[-12:]
    q_wave_intensities = extract_averages_from_folder("q wave")[-12:]
