import json
import random
import os
from datetime import datetime

# Define the number of tests
NUM_TESTS = 10

# Define the output directory and file name
output_dir = "20240908"
output_filename = os.path.join(output_dir, "test_results.json")

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load existing results if the file already exists
if os.path.exists(output_filename):
    with open(output_filename, 'r') as json_file:
        all_sessions = json.load(json_file)
else:
    all_sessions = {}

# Generate a unique session name based on the current datetime
session_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
test_results = []

# Generate a list of new test results
for i in range(NUM_TESTS):
    test_number = i + 1
    description = f"Test {test_number}: Description of measurement"
    lower_limit = random.uniform(0.0, 50.0)
    upper_limit = random.uniform(50.0, 100.0)
    target_value = random.uniform(lower_limit, upper_limit)
    measured_value = round(random.uniform(lower_limit, upper_limit), 2)
    conclusion = "PASS" if lower_limit <= measured_value <= upper_limit else "FAIL"
    
    test_result = {
        "Test Number": test_number,
        "Description": description,
        "Lower Limit (LL)": round(lower_limit, 2),
        "Upper Limit (UL)": round(upper_limit, 2),
        "Target Value (TV)": round(target_value, 2),
        "Measured Value (MV)": measured_value,
        "Conclusion": conclusion
    }
    
    test_results.append(test_result)

# Add the new test session to the all_sessions dictionary
all_sessions[session_name] = test_results

# Write the updated sessions to the JSON file
with open(output_filename, 'w') as json_file:
    json.dump(all_sessions, json_file, indent=4)

print(f"Test results saved under session '{session_name}' to {output_filename}")
