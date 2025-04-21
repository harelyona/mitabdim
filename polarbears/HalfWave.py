import os

from Malos import *

# Plot constants
DATA_COLOR = ["blue", "green", "red"]
LABELS = ["No Angle", "30° Angle", "50° Angle"]


def cos2_fit_func(x, a, b, c):
    return a * np.cos(np.deg2rad(x) - b)**2 + c


def plot_intensity_and_polar(intensities_by_type: list[list[float]]):
    angles_deg_all = [np.linspace(0, 180, len(intensities)) for intensities in intensities_by_type]
    angles_rad_all = [np.deg2rad(angles) for angles in angles_deg_all]

    # Create the figure and both axes separately
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, projection='polar')

    # Regular plot
    for i, (angles_deg, intensities) in enumerate(zip(angles_deg_all, intensities_by_type)):
        ax1.plot(angles_deg, intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])
    ax1.set_xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    ax1.set_ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    ax1.legend()
    ax1.set_title("Intensity vs Angle", fontsize=GRAPH_TITLE_SIZE)

    # Polar plot
    for i, (angles_rad, intensities) in enumerate(zip(angles_rad_all, intensities_by_type)):
        ax2.plot(angles_rad, intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])
    ax2.set_title("Polar Plot", fontsize=GRAPH_TITLE_SIZE)
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

def plot_regular_with_fit(intensities_by_type: list[list[float]]):
    plt.figure(figsize=FIGURE_SIZE)

    angles_deg_list = [
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # No Angle
        [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220],  # 30°

      #  [0, 10, 20, 30, 40, 120, 110, 100, 180, 190, 200, 210, 220],  # 50° (disabled)
    ]

    for i in range(2):  # Only No Angle and 30°
        angles_deg = angles_deg_list[i]
        intensities = intensities_by_type[i]
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

        plt.scatter(angles_deg, intensities, label=f"{label} Data", color=color)
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

    for i, intensities in enumerate(intensities_by_type):
        if LABELS[i] == "50° Angle":
            continue

        angles_deg = np.linspace(0, 180, len(intensities))
        angles_rad = np.deg2rad(angles_deg)

        # Mirror the data for 180°–360°
        mirrored_angles = angles_rad + np.pi
        full_angles = np.concatenate([angles_rad, mirrored_angles])
        full_intensities = np.concatenate([intensities, intensities])

        ax.plot(full_angles, full_intensities, 'o-', label=LABELS[i], color=DATA_COLOR[i])

    ax.set_title("Polar Plot (0–360°)", fontsize=GRAPH_TITLE_SIZE)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

#plot_polar(intensities[:2])
#######################################33

def plot_single_fit(intensities: list[float], angles_deg: list[float], label: str):
    plt.figure(figsize=FIGURE_SIZE)

    def cos2_fit_func(x, a, center, offset):
        return a * np.cos(np.deg2rad(x - center))**2 + offset

    initial_guess = [0.001, 90, 0]  # Try amplitude ~0.001, center at 90°, no offset
    bounds = ([0, 0, -1], [1, 180, 1])  # Amplitude between 0 and 1, center 0–180°

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
        return

    fine_x = np.linspace(min(angles_deg), max(angles_deg), 500)
    fitted_vals = cos2_fit_func(fine_x, *popt)

    plt.scatter(angles_deg, intensities, label=f"{label} Data", color='blue')
    plt.plot(fine_x, fitted_vals, label=f"{label} Fit", color='red')

    a, b, c = popt
    print(f"{label} Fit Params:\n  a = {a:.6f}\n  center = {b:.2f}°\n  offset = {c:.6f}")

    plt.xlabel(DEG_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.ylabel(INTENSITY_LABEL, fontsize=AXIS_LABEL_SIZE)
    plt.title(f"{label} - Cos² Fit", fontsize=GRAPH_TITLE_SIZE)
    plt.legend()
    plt.tight_layout()
    plt.show()


folder_names = [f"half wave{os.sep}no angle", f"half wave{os.sep}30 angle", f"half wave{os.sep}50 angle"]
intensities = [extract_averages_from_folder(name) for name in folder_names]

plot_regular_with_fit(intensities)
angles_30 = [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220]
intensities_30 = intensities[1]
initial_guess_30 = [-0.01, 0.617, 0.001]
bounds_30 = ([-1, -np.pi, -np.inf], [-0.0001, np.pi, np.inf])

angles_30 = [0, 10, 20, 30, 40, 100, 110, 120, 180, 190, 200, 210, 220]
intensities_30 = intensities[1]

plot_single_fit(intensities_30, angles_30, "30° Angle")

