import csv
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Define the file name for the CSV output
csv_filename = '/home/pi/piBASE/28AUG2024/adc.csv'

# Define the range for ADC values centered around 2.500 with deviations up to 1.000
ADC_CENTER = 2.500
ADC_DEVIATION = 1.000

# Number of simulated readings
NUM_READINGS = 100

# Function to generate a random ADC value centered around 2.500 with deviation up to 1.000
def generate_random_adc_value():
    return round(random.uniform(ADC_CENTER - ADC_DEVIATION, ADC_CENTER + ADC_DEVIATION), 3)

# Create and write to the CSV file
with open(csv_filename, mode='w', newline='') as file:
    # Create a CSV writer object
    csv_writer = csv.writer(file)
    
    # Write the header row
    csv_writer.writerow(['Index', 'Datetime', 'Q1', 'Q2', 'Q3', 'Q4'])
    
    # Generate and write simulated ADC readings
    for index in range(1, NUM_READINGS + 1):
        # Generate current datetime
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Generate random ADC readings for each quadrant
        q1 = generate_random_adc_value()
        q2 = generate_random_adc_value()
        q3 = generate_random_adc_value()
        q4 = generate_random_adc_value()
        
        # Write the row to the CSV file
        csv_writer.writerow([index, current_datetime, q1, q2, q3, q4])

print(f"Simulated ADC readings saved to {csv_filename}")

# Read the CSV data using pandas
df = pd.read_csv(csv_filename)

# Plot ADC readings for each quadrant over time
plt.figure(figsize=(10, 6))
plt.plot(df['Index'], df['Q1'], label='Q1')
plt.plot(df['Index'], df['Q2'], label='Q2')
plt.plot(df['Index'], df['Q3'], label='Q3')
plt.plot(df['Index'], df['Q4'], label='Q4')

# Add labels and legend
plt.xlabel('Index')
plt.ylabel('ADC Reading')
plt.title('Simulated ADC Readings Over Time')
plt.legend()

# Show the plot
plt.show()
