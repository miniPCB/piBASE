# Define the file name for the text output
log_filename = r'C:\Repos\piBASE\31AUG2024_02\test_results.txt'

# Function to log test results
def log_test_result(test_id, measurement, lower_limit, target_value, upper_limit, measured_value):
    # Determine the conclusion based on the measured value
    if lower_limit <= measured_value <= upper_limit:
        conclusion = 'Pass'
    else:
        conclusion = 'Fail'

    # Append data to text file with tabs between the data
    with open(log_filename, mode='a') as file:
        file.write(f"{test_id}\t\t\t{measurement}\t\t\t\t\t{lower_limit}\t\t{target_value}\t\t{upper_limit}\t\t{measured_value}\t\t{conclusion}\n")

    print(f"Test result logged: {test_id}, {measurement}, {lower_limit}, {target_value}, {upper_limit}, {measured_value}, {conclusion}")

# Function to initialize the text file with headers
def initialize_log():
    with open(log_filename, mode='w') as file:
        file.write("Test\t\tMeasurement\t\t\t\t\tLower Limit\t\tTarget Value\t\tUpper Limit\t\tMeasured Value\t\tConclusion\n")

# Initialize the text file
initialize_log()

# Example usage
log_test_result('001', 'Voltage between TP2 and TP1.', 4.75, 5.00, 5.25, 4.95)
log_test_result('002', 'Current through R1', 9.5, 10.0, 10.5, 10.1)
log_test_result('003', 'Resistance between TP1 and TP2', 99.0, 100.0, 101.0, 102.5)
