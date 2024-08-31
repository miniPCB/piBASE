import csv
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Define the file name for the CSV output
csv_filename = r'C:\Repos\piBASE\31AUG2024adc.csv'

# Define the range for ADC values centered around 2.500 with deviations up to 1.000
ADC_CENTER = 2.500
ADC_DEVIATION = 1.000

# Number of simulated readings to display
NUM_READINGS = 100
SMOOTHING_WINDOW = 5  # Number of points for the moving average

# Initialize lists to store data for plotting (only keep last NUM_READINGS points)
indexes = []
q1_values = []
q2_values = []
q3_values = []
q4_values = []

# Deques for smoothing
q1_deque = deque(maxlen=SMOOTHING_WINDOW)
q2_deque = deque(maxlen=SMOOTHING_WINDOW)
q3_deque = deque(maxlen=SMOOTHING_WINDOW)
q4_deque = deque(maxlen=SMOOTHING_WINDOW)

# Function to generate a random ADC value centered around 2.500 with deviation up to 1.000
def generate_random_adc_value():
    return round(random.uniform(ADC_CENTER - ADC_DEVIATION, ADC_CENTER + ADC_DEVIATION), 3)

# Function to apply a simple moving average for smoothing
def smooth_signal(signal_deque):
    return round(sum(signal_deque) / len(signal_deque), 3) if signal_deque else None

# Function to update the plot
def update(frame):
    # Generate 1 new reading in each update (10 updates per second)
    # Generate current datetime
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate random ADC readings for each quadrant
    index = len(indexes) + 1 if len(indexes) == 0 else indexes[-1] + 1
    q1_raw = generate_random_adc_value()
    q2_raw = generate_random_adc_value()
    q3_raw = generate_random_adc_value()
    q4_raw = generate_random_adc_value()

    # Append raw data to deque for smoothing
    q1_deque.append(q1_raw)
    q2_deque.append(q2_raw)
    q3_deque.append(q3_raw)
    q4_deque.append(q4_raw)

    # Smooth the signals using the moving average
    q1_smooth = smooth_signal(q1_deque)
    q2_smooth = smooth_signal(q2_deque)
    q3_smooth = smooth_signal(q3_deque)
    q4_smooth = smooth_signal(q4_deque)

    # Append smoothed data to lists
    indexes.append(index)
    q1_values.append(q1_smooth)
    q2_values.append(q2_smooth)
    q3_values.append(q3_smooth)
    q4_values.append(q4_smooth)

    # Append data to CSV file
    with open(csv_filename, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([index, current_datetime, q1_smooth, q2_smooth, q3_smooth, q4_smooth])

    # Keep only the last NUM_READINGS points (in place modification)
    if len(indexes) > NUM_READINGS:
        del indexes[:-NUM_READINGS]
        del q1_values[:-NUM_READINGS]
        del q2_values[:-NUM_READINGS]
        del q3_values[:-NUM_READINGS]
        del q4_values[:-NUM_READINGS]

    # Clear previous plots
    plt.cla()

    # Plot the updated data
    plt.plot(indexes, q1_values, label='Q1 (smoothed)')
    plt.plot(indexes, q2_values, label='Q2 (smoothed)')
    plt.plot(indexes, q3_values, label='Q3 (smoothed)')
    plt.plot(indexes, q4_values, label='Q4 (smoothed)')

    # Add labels and legend
    plt.xlabel('Index')
    plt.ylabel('ADC Reading')
    plt.title('Real-Time Smoothed ADC Readings (Last 100 Readings)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)  # Fixed legend below the chart

# Create a CSV file and write the header
with open(csv_filename, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Index', 'Datetime', 'Q1', 'Q2', 'Q3', 'Q4'])

# Set up the figure and axis for the plot with increased width
plt.figure(figsize=(12, 6))  # Increased width from 10 to 12 inches

# Use FuncAnimation to update the plot in real-time every 100 ms (10 updates per second)
ani = FuncAnimation(plt.gcf(), update, interval=100, cache_frame_data=False)  # Update every 100 ms

# Adjust layout to make space for the legend
plt.subplots_adjust(bottom=0.2)

# Show the plot
plt.show()
