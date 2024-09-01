import csv

# Define the file name for the CSV output
csv_filename = r'C:\Repos\piBASE\31AUG2024_02\test_results.csv'

# Function to log test results
def log_test_result(test_id, measurement, lower_limit, target_value, upper_limit, measured_value):
    # Determine the conclusion based on the measured value
    if lower_limit <= measured_value <= upper_limit:
        conclusion = 'Pass'
    else:
        conclusion = 'Fail'

    # Append data to CSV file
    with open(csv_filename, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([test_id, measurement, lower_limit, target_value, upper_limit, measured_value, conclusion])

    print(f"Test result logged: {test_id}, {measurement}, {lower_limit}, {target_value}, {upper_limit}, {measured_value}, {conclusion}")

# Function to initialize the CSV file with headers
def initialize_csv():
    with open(csv_filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Test ID', 'Measurement', 'Lower Limit', 'Target Value', 'Upper Limit', 'Measured Value', 'Conclusion'])

# Initialize the CSV file
initialize_csv()

# Example usage
log_test_result('001', 'Voltage between TP1 and TP2', 4.75, 5.00, 5.25, 4.95)
log_test_result('002', 'Current into TP3', 9.5, 10.0, 10.5, 10.1)
log_test_result('003', 'Resistance between TP4 and TP5', 99.0, 100.0, 101.0, 102.5)
