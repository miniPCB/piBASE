import csv
import random

# Define the input and output file paths
input_csv_filename = r'C:\Repos\piBASE\31AUG2024_02\input_test_data.csv'
output_csv_filename = r'C:\Repos\piBASE\31AUG2024_02\test_report.csv'

# Function to generate a random measured value within a range
def generate_measured_value(target_value, deviation=0.1):
    # Generate a random value within the target value ± deviation
    return round(random.uniform(target_value - deviation, target_value + deviation), 2)

# Function to generate the test report
def generate_test_report(input_csv, output_csv):
    # Open the input CSV file and read its contents
    with open(input_csv, mode='r') as infile:
        csv_reader = csv.DictReader(infile)
        
        # Open the output CSV file for writing
        with open(output_csv, mode='w', newline='') as outfile:
            fieldnames = ['Test ID', 'Measurement', 'Lower Limit', 'Target Value', 'Upper Limit', 'Measured Value', 'Conclusion']
            csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            
            # Loop through each row in the input CSV file
            for row in csv_reader:
                test_id = row['Test ID']
                measurement = row['Measurement']
                lower_limit = float(row['Lower Limit'])
                target_value = float(row['Target Value'])
                upper_limit = float(row['Upper Limit'])
                
                # Generate a random measured value around the target value
                measured_value = generate_measured_value(target_value)
                
                # Determine if the test passed or failed
                if lower_limit <= measured_value <= upper_limit:
                    conclusion = 'Pass'
                else:
                    conclusion = 'Fail'
                
                # Write the test result to the output CSV file
                csv_writer.writerow({
                    'Test ID': test_id,
                    'Measurement': measurement,
                    'Lower Limit': lower_limit,
                    'Target Value': target_value,
                    'Upper Limit': upper_limit,
                    'Measured Value': measured_value,
                    'Conclusion': conclusion
                })

    print(f"Test report generated: {output_csv}")

# Example usage
generate_test_report(input_csv_filename, output_csv_filename)
