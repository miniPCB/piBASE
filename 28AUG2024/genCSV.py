import csv
import random

# Define the file name for the CSV output
csv_file = '/home/pi/piBASE/28AUG2024/adc.csv'

# Define the range for ADC values (e.g., 0 to 1023 for a 10-bit ADC)
ADC_MIN = 0
ADC_MAX = 1023

# Number of simulated readings
NUM_READINGS = 100

# Function to generate a random ADC value within the range
def generate_random_adc_value():
    return random.randint(ADC_MIN, ADC_MAX)

# Create and write to the CSV file
with open(csv_filename, mode='w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write the header row
    csv_writer.writerow(['Q1', 'Q2', 'Q3', 'Q4'])
    
    # Generate and write simulated ADC readings
    for _ in range(NUM_READINGS):
        # Generate random ADC readings for each quadrant
        q1 = generate_random_adc_value()
        q2 = generate_random_adc_value()
        q3 = generate_random_adc_value()
        q4 = generate_random_adc_value()
        
        # Write the row to the CSV file
        csv_writer.writerow([q1, q2, q3, q4])

print(f"Simulated ADC readings saved to {csv_filename}")
