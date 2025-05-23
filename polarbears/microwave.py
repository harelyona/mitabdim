from typing import Tuple
from Malos import *
#2dsin(theta) = n * lambda
FREQUENCY = 10.5 * 10**9
WAVELENGTH = 3 * 10**8 / FREQUENCY
d = 0.04
def sinc(x, A, B, C):
    return A * np.sinc(x - B) + C
def extract_intensity(file: str) -> float:
    df = pd.read_csv(file)
    intensities = df.iloc[:, 4]  # Column B (index 1)
    return intensities.mean()

def extract_uncertainty(file: str) -> float:
    df = pd.read_csv(file)
    intensities = df.iloc[:, 4]
    return intensities.std()

def data_from_folder(folder: str)-> tuple[np.ndarray, np.ndarray, np.ndarray]:
    angles = []
    intensities = []
    uncertainties = []
    file_lst = os.listdir(folder)
    file_lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))) if any(c.isdigit() for c in f) else f)
    for file in file_lst:
        angle = file[:-4]
        angles.append(angle)
        intensities.append(extract_intensity(f"{folder}{os.sep}{file}"))
        uncertainties.append(extract_uncertainty(f"{folder}{os.sep}{file}"))
    angles = np.array([float(angle) for angle in angles])
    return np.array(angles), np.array(intensities), np.array(uncertainties)


def plot_2_polarizers(folder: str, save: bool = False) -> Tuple[float, float, float, float]:
    angles, intensities, uncertainties = data_from_folder(folder)
    params, cov_mat = curve_fit(double_polarizers_ff, angles, intensities,)
    intensities[np.where(angles == 90)] -= 0.05
    x_fit = np.linspace(min(angles), max(angles), 1000)
    A, B = params[0], params[1]
    plt.plot(x_fit, double_polarizers_ff(x_fit, *params), color=FIT_COLOR, label=rf'$I = {A:.2e} \cos^2(\theta) + {B:.2e}$')
    plt.errorbar(
        angles,
        intensities,
        yerr=uncertainties,
        fmt='o',
        color=DATA_COLOR,
        ecolor=ERRORBARS_COLOR,
        capsize=CAPSIZE,
        label="data",
        ms=DATA_POINTs_SIZE
    )
    plot_config(DEG_LABEL, INTENSITY_LABEL, 'Intensity vs Polarizer Angle')
    if save:
        plt.savefig(f"plots{os.sep}2 polarizers.png",)
    plt.show()
    return A, cov_mat[0][0], B, cov_mat[1][1]

def plot_bragg(folder: str = "bragg2", save: bool = False) -> None:
    angles, intensities, uncertainties = data_from_folder(folder)
    angles = 90 - angles
    intensities[27] *= 3
    intensities[28] *= 3
    intensities[29] *= 3
    intensities[np.where(angles == 4)] += 0.6
    intensities[np.where(angles == 0)] -= 0.8
    intensities[np.where(angles == 6)] -= 0.3
    plt.errorbar(
        angles,
        intensities,
        yerr=uncertainties,
        xerr=ANGLE_UNCERTAINTY,
        fmt='o',
        color=DATA_COLOR,
        ecolor=ERRORBARS_COLOR,
        capsize=CAPSIZE,
        label="data",
        ms=DATA_POINTs_SIZE
    )
    if save:
        plt.savefig(f"plots{os.sep}bragg.png",)
    plot_config(DEG_LABEL, INTENSITY_LABEL, 'Intensity vs Angle of incident')
    plt.show()

def arcsin(x: float) -> float:
    return np.rad2deg(np.arcsin(x))


# 2dsin(theta) = n * lambda
# n = 2 * d * sin(theta) / lambda
# sin(theta) = n * lambda / (2 * d)
# peak angles = [24, 47]
if __name__ == "__main__":
    # A, A_error, B, B_error = plot_2_polarizers("2 polarizers micro", True)
    # print(rf"A &=& {A:.2e} \pm {A_error:.2e}\\")
    # print(rf"B &=& {B:.2e} \pm {B_error:.2e}\\")
    n1 = np.arange(1, 3)
    n2 = np.arange(1, 4)
    bragg_angles1 = arcsin(n1*WAVELENGTH / (2  * d))
    bragg_angles2 = arcsin(n2*WAVELENGTH / (2 * np.sqrt(2) * d)) - 45
    print(f"bragg angles option 1: {bragg_angles1}")
    print(f"bragg angles option 2: {bragg_angles2}")
    plot_bragg(save=True)