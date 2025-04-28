import matplotlib.pyplot as plt

from Malos import *




if __name__ == "__main__":
    angles = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 25, 20, 15, 10])
    brewster_angles = np.array([55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 50, 51, 52, 53, 54, 55])
    vertical_intensities = extract_averages_from_folder(f"refraction{os.sep}vertical")
    horizontal_intensities = extract_averages_from_folder(f"refraction{os.sep}horizontal")
    brewster_intensities = extract_averages_from_folder(f"refraction{os.sep}brewster")
    vertical_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}vertical")
    horizontal_uncertainties = extract_uncertainties_from_folder(f"refraction{os.sep}horizontal")
    plt.scatter(angles, vertical_intensities, color="b", label="Vertical Intensities")
    plt.scatter(angles, horizontal_intensities, color="r", label="Horizontal Intensities")
    plt.scatter(brewster_angles, brewster_intensities, color="g", label="Brewster Intensities")
    plt.legend()
    plt.show()
    print(len(brewster_angles))