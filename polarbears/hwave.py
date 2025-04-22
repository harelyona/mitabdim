import matplotlib.pyplot as plt

from Malos import *

def half_wave_ff(x, a, b, c):
    return a * np.cos(np.deg2rad(x - b))**2 + c

def plot_half_wave(angles:np.ndarray, intensities:np.ndarray, uncertainties:np.ndarray, save=False):
    coefficients30_deg, cov_mat30_deg = curve_fit(half_wave_ff, angles, intensities)
    intensities0deg = extract_averages_from_folder(f"half wave{os.sep}no angle")
    coefficients0_deg, cov_mat0_deg = curve_fit(half_wave_ff, angles, intensities0deg)
    uncertainties_0deg = extract_uncertainties_from_folder(f"half wave{os.sep}no angle")

    plt.errorbar(angles, intensities, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties, fmt='o', color=DATA_COLOR, ecolor=ERRORBARS_COLOR, capsize=5, label='30 angle', ms=DATA_POINTs_SIZE)
    x_fit = np.linspace(min(angles), max(angles), 1000)
    plt.plot(x_fit, half_wave_ff(x_fit, *coefficients30_deg), color='black', label=rf'$I = {coefficients30_deg[0]:.2e} \cos^2(\theta + {coefficients30_deg[1]:.2f}) + {coefficients30_deg[2]:.2e}$')
    plt.errorbar(angles, intensities0deg, xerr=ANGLE_UNCERTAINTY, yerr=uncertainties_0deg, fmt='o', color="red", ecolor=ERRORBARS_COLOR, capsize=5, label='no angle', ms=DATA_POINTs_SIZE)
    plt.plot(x_fit, half_wave_ff(x_fit, *coefficients0_deg), color='red', label=rf'$I = {coefficients0_deg[0]:.2e} \cos^2(\theta - {coefficients0_deg[1]:.2f}) + {coefficients0_deg[2]:.2e}$')
    plot_config(DEG_LABEL, INTENSITY_LABEL, "Intensity vs Angle")
    if save:
        plt.savefig(f"figures{os.sep}half wave.pdf", format="pdf")
    plt.show()
    return coefficients30_deg, cov_mat30_deg, coefficients0_deg, cov_mat0_deg

if __name__== "__main__":
    angles_30 = np.array([0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220])
    intensities_30 = extract_averages_from_folder(f"half wave{os.sep}30 angle")
    uncertainties_30 = extract_uncertainties_from_folder(f"half wave{os.sep}30 angle")
    (A30, B30, C30), cov_mat30, (A0, B0, C0), cov_mat0 = plot_half_wave(angles_30, intensities_30, uncertainties_30, save=True)
    print(rf"A &=& {A30:.2e}\pm {cov_mat30[0][0]:.2e}\\")
    print(rf"B &=& {B30:.2f}\pm {cov_mat30[1][1]:.2f}\\")
    print(rf"C &=& {C30:.2e}\pm {cov_mat30[2][2]:.2e}\\")
    print(B0 - B30)