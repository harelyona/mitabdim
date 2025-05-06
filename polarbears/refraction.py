
from Malos import *
VERTICAL_COLOR = "blue"
HORIZONTAL_COLOR = "yellow"


def rp(angle, nout, A) -> float:
    """Calculate the reflection coefficient for p-polarized light."""
    angle = np.deg2rad(angle)
    nin = 1
    numerator = nout * np.cos(angle) - nin * np.sqrt(1 - (nin / nout) ** 2 * np.sin(angle) ** 2)
    denominator = nout * np.cos(angle) + nin * np.sqrt(1 - (nin / nout) ** 2 * np.sin(angle) ** 2)
    return A*abs(numerator / denominator)

def rs(angle,nout, A) -> float:
    """Calculate the reflection coefficient for s-polarized light."""
    angle = np.deg2rad(angle)
    nin = 1
    numerator = nin * np.cos(angle) - nout * np.sqrt(1 - (nin / nout) ** 2 * np.sin(angle) ** 2)
    denominator = nin * np.cos(angle) + nout * np.sqrt(1 - (nin / nout) ** 2 * np.sin(angle) ** 2)
    return A*abs(numerator / denominator)


def plot_horizontal(angles: np.ndarray, intensities: np.ndarray, uncertainties: np.ndarray, save=False):
    coefficients, cov_mat = curve_fit(rp, angles, intensities)
    x_fit = np.linspace(min(angles), max(angles), 1000)
    plt.plot(x_fit, rp(x_fit, *coefficients), color=HORIZONTAL_COLOR, label="horizontal fit")
    plt.errorbar(angles, intensities, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties, fmt='o', color=HORIZONTAL_COLOR,
                 ecolor=ERRORBARS_COLOR, capsize=CAPSIZE, label="horizontal data", ms=DATA_POINTs_SIZE)
    plot_config(DEG_LABEL, INTENSITY_LABEL, "Intensity vs Angle")
    if save:
        plt.savefig(f"figures{os.sep}horizontal.pdf", format="pdf")
    return coefficients, cov_mat

def plot_vertical(angles: np.ndarray, intensities: np.ndarray, uncertainties: np.ndarray, save=False):
    coefficients, cov_mat = curve_fit(rs, angles, intensities)
    x_fit = np.linspace(min(angles), max(angles), 1000)
    plt.plot(x_fit, rs(x_fit, *coefficients), color=VERTICAL_COLOR, label="vertical fit")
    plt.errorbar(angles, intensities, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties, fmt='o', color=VERTICAL_COLOR,
                 ecolor=ERRORBARS_COLOR, capsize=CAPSIZE, label="vertical data", ms=DATA_POINTs_SIZE)
    plot_config(DEG_LABEL, INTENSITY_LABEL, "Intensity vs Angle")
    if save:
        plt.savefig(f"figures{os.sep}horizontal.pdf", format="pdf")
    return coefficients, cov_mat

# Horizontal is p polarization
# Vertical is s polarization
if __name__ == "__main__":
    angles = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 25, 20, 15, 10])
    brewster_angles = np.array([55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 50, 51, 52, 53, 54, 55])
    vertical_intensities = extract_averages_from_folder(f"refraction{os.sep}vertical")
    horizontal_intensities = extract_averages_from_folder(f"refraction{os.sep}horizontal")
    brewster_intensities = extract_averages_from_folder(f"refraction{os.sep}brewster")
    vertical_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}vertical")
    horizontal_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}horizontal")
    brewster_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}brewster")
    (vertical_n), vertical_cov = plot_vertical(angles, vertical_intensities, vertical_uncertainties, save=False)

    # Add brewster angles and intensities to the plot
    angles = np.append(angles, brewster_angles)
    horizontal_intensities = np.append(horizontal_intensities, brewster_intensities)
    horizontal_uncertainties = np.append(horizontal_uncertainties, brewster_uncertainties)
    (horizontal_n), horizontal_cov = plot_horizontal(angles, horizontal_intensities, horizontal_uncertainties, save=False)

    print(vertical_n)
    print(horizontal_n)
    plt.show()
