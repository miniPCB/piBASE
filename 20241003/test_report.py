import subprocess
import sys
from colorama import Fore, Back, Style, init

# Function to install colorama if not available
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import colorama, and install if it is not installed
try:
    from colorama import Fore, Back, Style, init
except ImportError:
    print("colorama not found. Installing...")
    install("colorama")
    from colorama import Fore, Back, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Sample test data
test_results = [
    {"Test No.": 1, "Description": "Voltage Test", "Target": 5.0, "Lower Limit": 4.8, "Upper Limit": 5.2, "Measured": 5.1},
    {"Test No.": 2, "Description": "Current Test", "Target": 2.0, "Lower Limit": 1.8, "Upper Limit": 2.2, "Measured": 2.3},
    {"Test No.": 3, "Description": "Resistance Test", "Target": 100.0, "Lower Limit": 95.0, "Upper Limit": 105.0, "Measured": 100.5},
    {"Test No.": 4, "Description": "Temperature Test", "Target": 25.0, "Lower Limit": 20.0, "Upper Limit": 30.0, "Measured": 18.0},
    {"Test No.": 5, "Description": "Frequency Test", "Target": 50.0, "Lower Limit": 48.0, "Upper Limit": 52.0, "Measured": 51.0}
]

# Function to determine pass or fail based on measured value
def get_conclusion(lower, upper, measured):
    if lower <= measured <= upper:
        return "Pass"
    else:
        return "Fail"

# Display header
print(f"{'Test No.':<10} {'Description':<20} {'Target':<10} {'Lower Limit':<15} {'Upper Limit':<15} {'Measured':<12} {'Conclusion':<10}")
print('-' * 90)

# Iterate over test results and print them with color-coded conclusions
for test in test_results:
    conclusion = get_conclusion(test["Lower Limit"], test["Upper Limit"], test["Measured"])
    
    # Determine color based on pass or fail
    if conclusion == "Pass":
        conclusion_str = Back.GREEN + "Pass" + Style.RESET_ALL
    else:
        conclusion_str = Back.RED + "Fail" + Style.RESET_ALL
    
    # Print the test result in a formatted row
    print(f"{test['Test No.']:<10} {test['Description']:<20} {test['Target']:<10} {test['Lower Limit']:<15} {test['Upper Limit']:<15} {test['Measured']:<12} {conclusion_str:<10}")
