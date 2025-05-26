import os
from typing import Tuple

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import use
DATA_SIZE = 2
AXIS_LABEL_SIZE = 13
TITLE_SIZE = 13
LEGEND_SIZE = 10
base_resistance = 20000
changing_plates_resistance = 4016
AXIS_LOC = (0.94, 0.84)
TITLE_LOC = 0.96

use('TkAgg')

def plot_config(x_label: str, y_label: str, title: str):
    plt.legend(fontsize=LEGEND_SIZE, bbox_to_anchor=(0.2, 0.9))
    plt.tight_layout()
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.plot((1), (0), '>k', transform=ax.transAxes)
    ax.plot((0), (1), '^k', transform=ax.transAxes)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel("$V_1 [V]$", fontsize=16, labelpad=10, x=AXIS_LOC[0])
    ax.set_ylabel("$V_2 [V]$", fontsize=16, labelpad=10, y=AXIS_LOC[1])
    ax.set_title(title, fontsize=TITLE_SIZE, y=TITLE_LOC)


def extract_voltages(file: str) -> Tuple[np.array, np.array, np.array]:
    df = pd.read_csv(file)
    times = df.iloc[:, 3].values
    v1 = df.iloc[:, 4].values
    v2 = df.iloc[:, 10].values
    return times, v1, v2

def plot_heshels(folder: str, save: bool=False):
    files = os.listdir(folder)
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for file in files:
        times, v1, v2 = extract_voltages(os.path.join(folder, file))
        plt.scatter(v1, v2, label=file[:-4] + '$\\Omega$', s=DATA_SIZE)
    plot_config('V1 [V]', 'V2 [V]', 'Heshel Loops Over Different Resistances')
    if save:
        plt.savefig(f"plots{os.sep}heshel_loops.png", dpi=300)
    plt.show()


def plot_heshel_plates(folder: str="heshel vs plates", save: bool=False):
    files = os.listdir(folder)
    for file in files:
        times, v1, v2 = extract_voltages(os.path.join(folder, file))
        plt.scatter(v1, v2, label=file[:-4], s=DATA_SIZE)
    plot_config('V1 [V]', 'V2 [V]', 'Heshel Loops Over Different Plates')
    plt.show()



if __name__ == "__main__":
    plot_heshels("heshel vs resistance", True)
    print(plot_heshel_plates())

