import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')

# Function to load a CSV file into a DataFrame
def load_csv_to_dataframe(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None

# Function to extract metadata and data from a CSV file
def extract_data(file_path):
    # Example usage
    data = load_csv_to_dataframe(file_path)

    # Splitting the original data into two sections for each channel
    channel_1 = data.iloc[:, :5]  # First 6 columns for Channel 1
    channel_2 = data.iloc[:, 6:11]  # Last 6 columns for Channel 2

    # Renaming columns for better readability
    channel_1.columns = ['metadata_name', 'metadata_value', 'metadata_units', 'T', 'V']
    channel_2.columns = ['metadata_name', 'metadata_value', 'metadata_units', 'T', 'V']

    # Extracting metadata and data for each channel
    channel_1_metadata = channel_1[['metadata_name', 'metadata_value', 'metadata_units']].transpose()
    channel_1_metadata.columns = channel_1_metadata.iloc[0]
    channel_1_metadata = channel_1_metadata[1:]

    channel_2_metadata = channel_2[['metadata_name', 'metadata_value', 'metadata_units']].transpose()
    channel_2_metadata.columns = channel_2_metadata.iloc[0]
    channel_2_metadata = channel_2_metadata[1:]

    channel_1 = channel_1[['T', 'V']]
    channel_2 = channel_2[['T', 'V']]

    return channel_1, channel_2

def create_list_of_all_loops():
    num_of_materials = np.arange(1, 5)
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    for material in num_of_materials:
        file_path = f"../data/2.2_material{material}.csv"
        ch1_voltage, ch2_voltage = extract_data(file_path)
        ax1.scatter(ch1_voltage, ch2_voltage, label=f"Material {material}", s=10)

    plt.xlabel("H (V)")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.axhline(0, color='black', linewidth=1.5)  # Bold horizontal line at y=0
    plt.axvline(0, color='black', linewidth=1.5)  # Bold vertical line at x=0
    plt.ylabel("$\Phi_B$ (V)")
    plt.title("Hysteresis Loops of Different Materials")
    plt.legend()
    plt.show()

create_list_of_all_loops()
