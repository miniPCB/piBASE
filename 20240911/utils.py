import csv
import time
import random

def generate_csv_files():
    # Define the number of CSV files and their respective names
    num_sensors = 4
    csv_files = [f"sensor_data_{i}.csv" for i in range(1, num_sensors + 1)]
    
    # Initialize the CSV files with headers
    for file in csv_files:
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Channel1', 'Channel2', 'Channel3', 'Channel4'])
    
    start_time = time.time()
    
    try:
        while True:
            # Calculate the elapsed time since start
            elapsed_time = time.time() - start_time

            for file in csv_files:
                with open(file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Generate random voltages for the 4 channels
                    voltages = [round(random.uniform(3.0, 3.6), 2) for _ in range(4)]

                    # Write the time and voltages to the CSV file
                    writer.writerow([round(elapsed_time, 2)] + voltages)
            
            # Sleep for 0.1 seconds to simulate 10 updates per second
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("CSV generation stopped.")

# If this script is run directly, start generating the CSV files
if __name__ == "__main__":
    generate_csv_files()
