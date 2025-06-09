import glob
import os
import numpy as np
from matplotlib import pyplot as plt, rc, use
from skimage import io, color, filters
use('TkAgg')

v1 = np.concatenate((np.arange(0, 5.5, 0.2), np.arange(5.2, -0.1, -0.2), np.arange(-0.2, -5.5, -0.2), np.arange(-5.2, 0.1, 0.2)))
v2 = np.concatenate((np.arange(0, 5.1, 0.2), np.arange(4.8, -0.1, -0.2), np.arange(-0.2, -5.1, -0.2), np.arange(-4.8, 0.1, 0.2)))
img1_numbers = np.array([f"{1238 + i}" for i in range(len(v1))])
img2_numbers = np.array([f"{1349 + i}" for i in range(len(v2))])
step = 0.2
v1 = np.round(v1 / step) * step
v2 = np.round(v2 / step) * step
image_directory = fr'domains{os.sep}2'  # Your specified path
def main():
    # Set the font family to 'serif'
    rc('font', family='serif')

    # Directory containing the images (using raw string for Windows path)


    # List to store the data
    area_data = []

    # Loop through all images with the specified naming pattern (handling both single and double digit numbers)
    for num in range(len(img1_numbers)):
        # Create the file name pattern, without zero-padding the number, and check for both .png and .bmp extensions
        png_filename = os.path.join(image_directory, f'grant_*_v_mes_{num}.jpg')
        # grant_5_v_mes_1.png
        # Find the files that match the pattern
        image_files = glob.glob(png_filename)

        # If there's at least one matching file
        if image_files:
            image_file = image_files[0]  # In case there are multiple, take the first one

            # Extract only the filename from the full path
            base_filename = os.path.basename(image_file)  # Extracts 'grant_*_v_mes_{num}.png' or .bmp

            # Extract the value of * from the filename
            try:
                filename_parts = base_filename.split('_')  # Split the filename by '_'
                star_value = filename_parts[1]  # Extract the part corresponding to '*'

                # Load and process the image
                image = io.imread(image_file)
                grayscale_image = color.rgb2gray(image)  # Convert to grayscale

                # Apply a threshold (Otsu's method)
                threshold = filters.threshold_otsu(grayscale_image)
                binary_image = grayscale_image > threshold  # Bright areas are True, dark areas are False

                # Calculate areas
                dark_area = np.sum(~binary_image)  # Count dark pixels (False)
                bright_area = np.sum(binary_image)  # Count bright pixels (True)

                # Calculate the percentage of bright area out of total area
                total_area = dark_area + bright_area
                bright_percentage = (bright_area / total_area) * 100

                # Normalize the percentage (shift it so that 50% becomes 0)
                normalized_bright_percentage = bright_percentage

                # Store the result in the list
                area_data.append({
                    'star_value': float(star_value),  # Convert to float to handle numeric values properly
                    'normalized_bright_percentage': normalized_bright_percentage
                })
            except Exception as e:
                print(f"Failed to process {image_file}: {e}")
        else:
            print(f"No file found for: {png_filename}")

    # Extract the data for plotting
    star_values = [data['star_value'] for data in area_data]
    normalized_bright_percentages = np.array([data['normalized_bright_percentage'] for data in area_data])
    normalized_bright_percentages += 100 - np.max(normalized_bright_percentages)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(star_values, normalized_bright_percentages, marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.xlabel('H (a.u)', fontsize=14, fontfamily='serif')
    plt.ylabel('Precentage of Bright Area (%)', fontsize=14, fontfamily='serif')

    # Show the plot
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()