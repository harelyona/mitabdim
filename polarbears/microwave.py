import numpy as np

from Malos import *
#2dsin(theta) = n * lambda
FREQUENCY = 10.5 * 10**9
WAVELENGTH = 3 * 10**8 / FREQUENCY
d = 0.04

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

    return np.array(angles), np.array(intensities), np.array(uncertainties)

def plot_2_polarizers(folder: str, save: bool = False) -> None:
    angles, intensities, uncertainties = data_from_folder(folder)
    intensities[27] *= 3
    intensities[28] *= 3
    intensities[29] *= 3

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
    if save:
        plt.savefig(f"{folder}{os.sep}2_polarizers_micro.png",)
    plt.show()



if __name__ == "__main__":
    plot_2_polarizers("bragg2")
    x = np.array([11, 2, 3, 4])
    y = np.where(x == 1)[0][0]
    print(y)
