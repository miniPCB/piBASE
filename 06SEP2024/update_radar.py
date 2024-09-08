import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the directions (categories) for the radar chart
categories = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
num_vars = len(categories)

# Function to calculate the angle for each category
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# Initialize the flux field values (for demonstration, random values will be used)
flux_field_values = np.random.rand(num_vars).tolist()
flux_field_values += flux_field_values[:1]  # to close the radar chart

# Function to generate random flux field values (simulate your flux field calculation)
def calculate_flux_field():
    return np.random.rand(num_vars).tolist()

# Function to update the radar chart
def update(frame):
    # Calculate new flux field values
    new_flux_field_values = calculate_flux_field()
    new_flux_field_values += new_flux_field_values[:1]  # Close the radar chart

    # Clear the previous plot
    ax.clear()

    # Draw the radar chart with updated values
    ax.fill(angles, new_flux_field_values, color='blue', alpha=0.25)
    ax.plot(angles, new_flux_field_values, color='blue', linewidth=2)

    # Draw the category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Set the range for the radar chart
    ax.set_ylim(0, 1)

# Create the radar chart figure
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Function to create an animated radar chart
ani = FuncAnimation(fig, update, interval=1000)  # Update every second

plt.show()
