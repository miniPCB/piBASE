import os
import platform
import subprocess
import sys
import csv
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Determine the platform and set the correct file path
current_platform = platform.system()

if current_platform == "Windows":
    csv_filename = r'C:\Repos\piBASE\31AUG2024\adc.csv'
elif current_platform == "Linux":
    csv_filename = '/home/pi/piBASE/31AUG2024/adc.csv'
else:
    raise OSError(f"Unsupported platform: {current_platform}")

# Ensure the directory exists before trying to open the file
csv_dir = os.path.dirname(csv_filename)
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Create a CSV file and write the header
with open(csv_filename, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Index', 'Datetime', 'Q1', 'Q2', 'Q3', 'Q4'])

# Function to install packages if not present
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install Pandas
try:
    import pandas as pd
    print("Pandas is already installed.")
except ImportError:
    print("Pandas is not installed. Installing now...")
    install("pandas")
    try:
        import pandas as pd
        print("Pandas has been successfully installed.")
    except ImportError:
        print("Failed to install Pandas.")

# Check and install Matplotlib
try:
    import matplotlib
    print("Matplotlib is already installed.")
except ImportError:
    print("Matplotlib is not installed. Installing now...")
    install("matplotlib")
    try:
        import matplotlib
        print("Matplotlib has been successfully installed.")
    except ImportError:
        print("Failed to install Matplotlib.")

# ADC simulation and smoothing setup
ADC_CENTER = 2.500
ADC_DEVIATION = 1.000
NUM_READINGS = 100
SMOOTHING_WINDOW = 5

indexes = []
q1_values = []
q2_values = []
q3_values = []
q4_values = []

q1_deque = deque(maxlen=SMOOTHING_WINDOW)
q2_deque = deque(maxlen=SMOOTHING_WINDOW)
q3_deque = deque(maxlen=SMOOTHING_WINDOW)
q4_deque = deque(maxlen=SMOOTHING_WINDOW)

def generate_random_adc_value():
    return round(random.uniform(ADC_CENTER - ADC_DEVIATION, ADC_CENTER + ADC_DEVIATION), 3)

def smooth_signal(signal_deque):
    return round(sum(signal_deque) / len(signal_deque), 3) if signal_deque else None

def update(frame):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    index = len(indexes) + 1 if len(indexes) == 0 else indexes[-1] + 1

    q1_raw = generate_random_adc_value()
    q2_raw = generate_random_adc_value()
    q3_raw = generate_random_adc_value()
    q4_raw = generate_random_adc_value()

    q1_deque.append(q1_raw)
    q2_deque.append(q2_raw)
    q3_deque.append(q3_raw)
    q4_deque.append(q4_raw)

    q1_smooth = smooth_signal(q1_deque)
    q2_smooth = smooth_signal(q2_deque)
    q3_smooth = smooth_signal(q3_deque)
    q4_smooth = smooth_signal(q4_deque)

    indexes.append(index)
    q1_values.append(q1_smooth)
    q2_values.append(q2_smooth)
    q3_values.append(q3_smooth)
    q4_values.append(q4_smooth)

    with open(csv_filename, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([index, current_datetime, q1_smooth, q2_smooth, q3_smooth, q4_smooth])

    if len(indexes) > NUM_READINGS:
        del indexes[:-NUM_READINGS]
        del q1_values[:-NUM_READINGS]
        del q2_values[:-NUM_READINGS]
        del q3_values[:-NUM_READINGS]
        del q4_values[:-NUM_READINGS]

    plt.cla()

    plt.plot(indexes, q1_values, label='Q1 (smoothed)')
    plt.plot(indexes, q2_values, label='Q2 (smoothed)')
    plt.plot(indexes, q3_values, label='Q3 (smoothed)')
    plt.plot(indexes, q4_values, label='Q4 (smoothed)')

    plt.xlabel('Index')
    plt.ylabel('ADC Reading')
    plt.title('Real-Time Smoothed ADC Readings (Last 100 Readings)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4)

# Set up the figure and axis for the plot with increased width
fig = plt.figure(figsize=(12, 6))

# Use FuncAnimation to update the plot in real-time every 100 ms (10 updates per second)
ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)

# Adjust layout to make space for the legend
plt.subplots_adjust(bottom=0.2)

# Handle window close event to terminate the script
def handle_close(event):
    print("Window closed, stopping the script.")
    plt.close(fig)
    sys.exit()

fig.canvas.mpl_connect('close_event', handle_close)

# Show the plot
plt.show()
