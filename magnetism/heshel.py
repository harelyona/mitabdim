import os
from typing import Tuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import use
DATA_SIZE = 2
AXIS_LABEL_SIZE = 20
TITLE_SIZE = 20
LEGEND_SIZE = 10
base_resistance = 20000
changing_plates_resistance = 4016

use('TkAgg')

def plot_config(x_label: str, y_label: str, title: str):
    # plt.xlabel(x_label, fontsize=AXIS_LABEL_SIZE)
    # plt.ylabel(y_label, fontsize=AXIS_LABEL_SIZE)
    # plt.title(title, fontsize=TITLE_SIZE)
    plt.legend(fontsize=LEGEND_SIZE)
    plt.tight_layout()
    # Add axes at the center (x=0, y=0)
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add arrows to axes
    ax.plot((1), (0), '>k', transform=ax.transAxes)
    ax.plot((0), (1), '^k', transform=ax.transAxes)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)


def extract_voltages(file: str) -> Tuple[np.array, np.array, np.array]:
    df = pd.read_csv(file)
    times = df.iloc[:, 3].values
    v1 = df.iloc[:, 4].values
    v2 = df.iloc[:, 10].values
    return times, v1, v2

def plot_heshels(folder: str):
    files = os.listdir(folder)
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for file in files:
        times, v1, v2 = extract_voltages(os.path.join(folder, file))
        plt.scatter(v1, v2, label=file[:-4] + '$\\Omega$', s=DATA_SIZE)
    plot_config('V1 [V]', 'V2 [V]', 'Heshel Loops Over Different Resistances')
    plt.show()



if __name__ == "__main__":
    plot_heshels("heshel vs resistance")

