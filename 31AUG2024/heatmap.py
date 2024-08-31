import csv
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from matplotlib.colors import LinearSegmentedColormap

# File paths
csv_filename = r'C:\Repos\piBASE\31AUG2024\adc.csv'
floorplan_image_path = r'C:\Repos\piBASE\31AUG2024\floorplan.png'

# Custom blue-green-red gradient colors
colors = [
    (0.0, "#0000FF"),  # Blue at 0%
    (0.25, "#00FF00"),  # Green at 25%
    (0.75, "#00FF00"),  # Green at 75%
    (1.0, "#FF0000")   # Red at 100%
]

# Create a custom colormap with more weight on the green region
custom_cmap = LinearSegmentedColormap.from_list("blue_green_red_gradient", colors, N=256)

# Generate random ADC values (for simulation purposes)
def generate_random_adc_value():
    return round(random.uniform(2.500 - 1.000, 2.500 + 1.000), 3)

# Function to read the latest values from the CSV
def read_latest_values_from_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        rows = list(reader)
        latest_row = rows[-1]  # Get the last row
        q1, q2, q3, q4 = map(float, latest_row[2:6])
    return q1, q2, q3, q4

# Read the latest values from the CSV
q1, q2, q3, q4 = read_latest_values_from_csv(csv_filename)

# Create a 2x2 grid for heatmap values
heatmap_data = np.array([[q1, q2],
                         [q3, q4]])

# Load the floorplan image
img = mpimg.imread(floorplan_image_path)

# Plotting the floorplan
plt.imshow(img, extent=[0, 2, 0, 2])  # Adjust extent to match your floorplan's coordinates

# Overlay the heatmap with the custom blue-green-red gradient
plt.imshow(heatmap_data, cmap=custom_cmap, alpha=0.6, extent=[0, 2, 0, 2])  # Adjust extent to match the floorplan

# Add color bar
plt.colorbar(label='ADC Value')

# Labels and title
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Heatmap of ADC Values on Floorplan (Custom Blue-Green-Red Gradient)')

# Display the heatmap
plt.show()
