import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import json
import os
import socket
import getpass

# Define the number of tests
NUM_TESTS = 10

# Define the output directory and file name
output_dir = "20240908"
output_filename = os.path.join(output_dir, "test_results.json")

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get the computer ID and username
computer_id = socket.gethostname()
username = getpass.getuser()

# Define a function to generate test results
def generate_test_result(test_number):
    description = f"Test {test_number}: Description of measurement"
    lower_limit = random.uniform(0.0, 50.0)
    upper_limit = random.uniform(50.0, 100.0)
    target_value = random.uniform(lower_limit, upper_limit)
    measured_value = round(random.uniform(lower_limit, upper_limit), 2)
    conclusion = "PASS" if lower_limit <= measured_value <= upper_limit else "FAIL"
    
    return {
        "Test Number": test_number,
        "Description": description,
        "Lower Limit (LL)": round(lower_limit, 2),
        "Upper Limit (UL)": round(upper_limit, 2),
        "Target Value (TV)": round(target_value, 2),
        "Measured Value (MV)": measured_value,
        "Conclusion": conclusion
    }

# Define a function to load test results from the JSON file
def load_test_results():
    if os.path.exists(output_filename):
        with open(output_filename, 'r') as json_file:
            return json.load(json_file)
    return {"configuration": {}, "comments": [], "sessions": {}}  # Ensure structure with "configuration", "comments", and "sessions" keys

# Define a function to save test results to the JSON file
def save_test_results(data):
    with open(output_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Define a function to delete a test session with confirmation
def delete_test_results(session_name, tab_index):
    # Show a confirmation dialog
    if messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete the test results for '{session_name}'?"):
        # Load existing results
        data = load_test_results()
        
        # Remove the selected session
        if session_name in data["sessions"]:
            del data["sessions"][session_name]
        
        # Save the updated results back to the file
        save_test_results(data)
        
        # Remove the tab from the notebook
        testing_notebook.forget(tab_index)
        
        print(f"Test results for session '{session_name}' deleted.")

# Define a function to display test results in a new sub-tab under "Testing"
def display_test_results(session_name, test_results):
    frame = ttk.Frame(testing_notebook)
    testing_notebook.add(frame, text=session_name)

    # Add a treeview to display the test results
    tree = ttk.Treeview(frame, columns=("Description", "LL", "UL", "TV", "MV", "Conclusion"), show='headings')
    tree.heading("Description", text="Description")
    tree.heading("LL", text="Lower Limit")
    tree.heading("UL", text="Upper Limit")
    tree.heading("TV", text="Target Value")
    tree.heading("MV", text="Measured Value")
    tree.heading("Conclusion", text="Conclusion")
    tree.pack(expand=True, fill='both')

    # Insert test results into the treeview
    for result in test_results:
        tree.insert("", "end", values=(
            result["Description"],
            result["Lower Limit (LL)"],
            result["Upper Limit (UL)"],
            result["Target Value (TV)"],
            result["Measured Value (MV)"],
            result["Conclusion"]
        ))

    # Add a "Delete Results" button
    delete_button = ttk.Button(frame, text="Delete Results", 
                               command=lambda: delete_test_results(session_name, testing_notebook.index(frame)))
    delete_button.pack(pady=10)

# Define a function to run selected tests and display the results
def run_tests():
    selected_tests = [i+1 for i, var in enumerate(test_vars) if var.get()]
    
    if not selected_tests:
        print("No tests selected.")
        return
    
    # Load existing results
    data = load_test_results()

    # Generate a unique session name based on the current datetime
    session_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_results = []

    # Run the selected tests
    for test_number in selected_tests:
        test_result = generate_test_result(test_number)
        test_results.append(test_result)
    
    # Add the new test session to the sessions dictionary
    data["sessions"][session_name] = test_results

    # Save the updated results
    save_test_results(data)

    print(f"Test results saved under session '{session_name}' to {output_filename}")

    # Display the new test results in a new sub-tab under "Testing"
    display_test_results(session_name, test_results)

# Define a function to add a comment
def add_comment():
    comment_text = comment_entry.get().strip()
    if comment_text:
        # Get the current datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create the comment entry
        comment_entry_data = {
            "timestamp": timestamp,
            "computer_id": computer_id,
            "username": username,
            "comment": comment_text
        }
        
        # Load existing data
        data = load_test_results()
        
        # Add the new comment
        data["comments"].append(comment_entry_data)
        
        # Save the updated data
        save_test_results(data)
        
        # Clear the comment entry field
        comment_entry.delete(0, tk.END)
        
        # Update the comments display
        display_comments()

# Define a function to display comments
def display_comments():
    data = load_test_results()
    comments_text.delete(1.0, tk.END)  # Clear the text widget
    for comment in data["comments"]:
        comments_text.insert(tk.END, f"{comment['timestamp']} - {comment['computer_id']} ({comment['username']}):\n{comment['comment']}\n\n")

# Define a function to save configuration data
def save_configuration():
    data = load_test_results()
    data["configuration"] = {
        "board_name": board_name_entry.get().strip(),
        "board_variant": board_variant_entry.get().strip(),
        "board_revision": board_revision_entry.get().strip(),
        "board_serial_number": board_serial_number_entry.get().strip(),
    }
    save_test_results(data)
    update_welcome_tab()  # Update the welcome tab with the new information
    print("Configuration saved.")

# Define a function to load configuration data into the UI
def load_configuration():
    data = load_test_results()
    config = data.get("configuration", {})
    board_name_entry.insert(0, config.get("board_name", ""))
    board_variant_entry.insert(0, config.get("board_variant", ""))
    board_revision_entry.insert(0, config.get("board_revision", ""))
    board_serial_number_entry.insert(0, config.get("board_serial_number", ""))
    update_welcome_tab()  # Update the welcome tab with the loaded information

# Define a function to update the welcome tab with the board information
def update_welcome_tab():
    data = load_test_results()
    config = data.get("configuration", {})
    board_name = config.get("board_name", "N/A")
    board_variant = config.get("board_variant", "N/A")
    board_revision = config.get("board_revision", "N/A")
    board_serial_number = config.get("board_serial_number", "N/A")

    # Update the welcome text
    welcome_text.set(f"Board Name: {board_name}\n"
                     f"Board Variant: {board_variant}\n"
                     f"Board Revision: {board_revision}\n"
                     f"Board SN: {board_serial_number}")

# Create the main application window
root = tk.Tk()
root.title("Test Manager")

# Create a major tab control
major_notebook = ttk.Notebook(root)
major_notebook.pack(expand=True, fill='both')

# Create a "Welcome" major tab
welcome_frame = ttk.Frame(major_notebook)
major_notebook.add(welcome_frame, text="Welcome")

# Variable to hold the welcome text
welcome_text = tk.StringVar()
welcome_label = tk.Label(welcome_frame, textvariable=welcome_text, font=("Helvetica", 12), justify="left")
welcome_label.pack(pady=20, padx=20, anchor="w")

# Create a notebook inside the "Welcome" tab for sub-tabs (Board Information, Comments, Testing)
welcome_notebook = ttk.Notebook(welcome_frame)
welcome_notebook.pack(expand=True, fill='both')

# Create the "Board Information" sub-tab under "Welcome"
board_info_frame = ttk.Frame(welcome_notebook)
welcome_notebook.add(board_info_frame, text="Board Information")

# Add board information input fields
ttk.Label(board_info_frame, text="Board Name:").pack(pady=5, anchor='w')
board_name_entry = ttk.Entry(board_info_frame, width=40)
board_name_entry.pack(pady=5, padx=10, anchor='w')

ttk.Label(board_info_frame, text="Board Variant:").pack(pady=5, anchor='w')
board_variant_entry = ttk.Entry(board_info_frame, width=40)
board_variant_entry.pack(pady=5, padx=10, anchor='w')

ttk.Label(board_info_frame, text="Board Revision:").pack(pady=5, anchor='w')
board_revision_entry = ttk.Entry(board_info_frame, width=40)
board_revision_entry.pack(pady=5, padx=10, anchor='w')

ttk.Label(board_info_frame, text="Board Serial Number:").pack(pady=5, anchor='w')
board_serial_number_entry = ttk.Entry(board_info_frame, width=40)
board_serial_number_entry.pack(pady=5, padx=10, anchor='w')

# Add a button to save the board information
save_config_button = ttk.Button(board_info_frame, text="Save Board Information", command=save_configuration)
save_config_button.pack(pady=10)

# Load existing board information data into the UI
load_configuration()

# Create the "Comments" sub-tab under "Welcome"
comments_frame = ttk.Frame(welcome_notebook)
welcome_notebook.add(comments_frame, text="Comments")

# Create the comment input form
comment_entry = ttk.Entry(comments_frame, width=80)
comment_entry.pack(pady=10, padx=10)

# Create a button to add the comment
add_comment_button = ttk.Button(comments_frame, text="Add Comment", command=add_comment)
add_comment_button.pack(pady=5)

# Create a text widget to display comments
comments_text = tk.Text(comments_frame, wrap='word', height=15)
comments_text.pack(expand=True, fill='both', padx=10, pady=10)

# Display existing comments
display_comments()

# Create the "Testing" sub-tab under "Welcome"
testing_frame = ttk.Frame(welcome_notebook)
welcome_notebook.add(testing_frame, text="Testing")

# Create a notebook inside the "Testing" sub-tab for Test Controls and results
testing_notebook = ttk.Notebook(testing_frame)
testing_notebook.pack(expand=True, fill='both')

# Create the "Test Controls" sub-tab under "Testing"
controls_frame = ttk.Frame(testing_notebook)
testing_notebook.add(controls_frame, text="Test Controls")

# Create a list to hold the variables for the checkboxes
test_vars = []

# Create checkboxes for each test
for i in range(NUM_TESTS):
    var = tk.IntVar()
    checkbox = ttk.Checkbutton(controls_frame, text=f"Test {i+1}: Description of measurement", variable=var)
    checkbox.pack(anchor='w')
    test_vars.append(var)

# Create the "Run Tests" button
run_button = ttk.Button(controls_frame, text="Run Tests", command=run_tests)
run_button.pack(pady=10)

# Load and display all previous test sessions after adding the "Test Controls" sub-tab
data = load_test_results()
for session_name, test_results in data["sessions"].items():
    display_test_results(session_name, test_results)

# Create the "About" major tab
about_frame = ttk.Frame(major_notebook)
major_notebook.add(about_frame, text="About")

# Add content to the "About" tab
about_label = tk.Label(about_frame, text="Test Manager Application\nVersion 1.0\n\nThis application allows users to run and manage tests, view results, and add comments.", justify="center", padx=10, pady=10)
about_label.pack(expand=True)

# Start the main event loop
root.mainloop()
