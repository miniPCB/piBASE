import re
import os
import datetime
import getpass
import socket
import subprocess

# Define the directory where the files should be saved
save_directory = "/home/pi/piBASE/22AUG2024/redtags"

def parse_pcb_barcode(input_string):
    board_name_pattern = r"^(.*?)-"
    board_rev_pattern = r"^[^-]*-(.*?)-"
    board_var_pattern = r"(?:[^-]*-){2}([^-]*)-"
    board_sn_pattern = r"(?:[^-]*-){3}([^-\s]*)"

    board_name = re.match(board_name_pattern, input_string).group(1).lower() if re.match(board_name_pattern, input_string) else "unknown"
    board_rev = re.match(board_rev_pattern, input_string).group(1) if re.match(board_rev_pattern, input_string) else "unknown"
    board_var = re.search(board_var_pattern, input_string).group(1) if re.search(board_var_pattern, input_string) else "unknown"
    board_sn = re.search(board_sn_pattern, input_string).group(1) if re.search(board_sn_pattern, input_string) else "unknown"

    return board_name, board_rev, board_var, board_sn

def read_existing_issues(file_name):
    issues = []
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith("Message:"):
                    issues.append(line.strip())
    return issues

def prompt_user_for_action(board_name, board_rev, board_var, board_sn, existing_issues):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

        print("redTAG!")
        print("------------------------------------------------------------------------------------------------------------")
        print(f"|    \tBoard Name: {board_name}")
        print(f"| \tBoard Rev: {board_rev}")
        print(f"| \tBoard Variant: {board_var}")
        print(f"| \tBoard SN: {board_sn}")
        print("|")
        if existing_issues:
            for issue in existing_issues:
                print(f"| \t{issue}")
        else:
            print("| \tNo existing issues.")
        print("|")
        print("------------------------------------------------------------------------------------------------------------")
        print("redTAG!")
        print("\n\n\n  OPTIONS:")
        print("  [1] Enter new message.")
        print("  [x] Return to welcome screen.")
        
        user_input = input("\nChoose an option: ").strip().lower()
        
        if user_input == '1':
            issue_message = input("Enter the new message: ").strip()
            # Add the current datetime, username, and computer name to the beginning of the message
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_name = getpass.getuser()
            computer_name = socket.gethostname()
            issue_message = f"Message: {current_datetime} - {user_name}@{computer_name} - {issue_message}"
            return 'create', issue_message
        elif user_input == 'x':
            return 'welcome', None
        else:
            print("Invalid input. Please try again.")

def create_file_with_barcode_data(input_string):
    # Parse the barcode
    board_name, board_rev, board_var, board_sn = parse_pcb_barcode(input_string)

    # Create the full file path
    file_name = os.path.join(save_directory, f"{board_name}-{board_rev}-{board_var}-{board_sn}.txt")

    # Read existing issues from the file
    existing_issues = read_existing_issues(file_name)

    while True:
        # Prompt the user for action
        action, issue_message = prompt_user_for_action(board_name, board_rev, board_var, board_sn, existing_issues)

        if action == 'create':
            # Open the file in append mode if it exists, or create it if it doesn't
            with open(file_name, 'a+') as file:
                file.seek(0)
                content = file.read()
                if not content:  # If the file is empty (newly created), write headers
                    file.write(f"Board Name: {board_name}\n")
                    file.write(f"Board Revision: {board_rev}\n")
                    file.write(f"Board Variant: {board_var}\n")
                    file.write(f"Board Serial Number: {board_sn}\n")
                if issue_message:
                    file.write(f"{issue_message}\n")
            print(f"File '{file_name}' updated with new issue.")
            existing_issues.append(issue_message)  # Add the new issue to the list

            # Re-read the file to ensure all issues are included (in case of multiple updates)
            existing_issues = read_existing_issues(file_name)

        elif action == 'welcome':
            push_to_github(file_name)
            break  # Exit the loop to return to the welcome page

def push_to_github(file_name):
    try:
        # Stage the file for commit
        subprocess.run(['git', 'add', file_name], check=True)
        # Commit the file with a message
        commit_message = f"Update {file_name} with new issue"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        # Push the changes to the remote repository
        subprocess.run(['git', 'push'], check=True)
        print(f"Successfully pushed {file_name} to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pushing to GitHub: {e}")

def configure_git_remote():
    try:
        # Set the correct remote repository URL
        subprocess.run(['git', 'remote', 'set-url', 'origin', 'git@github.com:miniPCB/piBASE.git'], check=True)
        print("Configured the remote repository to git@github.com:miniPCB/piBASE.git.")
        
        # Verify the remote repository configuration
        result = subprocess.run(['git', 'remote', '-v'], check=True, text=True, capture_output=True)
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while configuring the remote repository: {e}")

def pull_from_github():
    try:
        configure_git_remote()
        
        # Fetch the latest changes from the remote repository
        fetch_result = subprocess.run(['git', 'fetch'], check=True, text=True, capture_output=True)
        print(fetch_result.stdout)
        
        # Pull the latest changes into the local branch
        pull_result = subprocess.run(['git', 'pull'], check=True, text=True, capture_output=True)
        print(pull_result.stdout)
        
        print("Successfully fetched and pulled the latest files from GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while fetching or pulling from GitHub: {e}")
        print(f"Error details: {e.stderr}")

def welcome_page():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

        print("-----------------------------------------------------------------")
        print("\n  Welcome to redTAG!\n  A simple system for collecting Red Tag messages.")
        print("\n  Scan a barcode,\n  See previous messages,\n  Enter new messages!")
        print("\n  Nolan Manteufel\n  Mesa Technologies\n  (C)2024")
        print("\n\n  [1] Pull latest files from GitHub")
        print("  [x] Exit program")
        print("\n-----------------------------------------------------------------")

        user_input = input("Press ENTER to scan a barcode, or choose an option: ").strip().lower()

        if user_input == 'x':
            print("Exiting program...")
            break
        elif user_input == '1':
            pull_from_github()
            input("\nPress ENTER to return to the welcome screen.")  # Pause before returning to the main menu
        elif user_input == '':
            return 'scan'
        else:
            print("Invalid input. Please try again.")

def read_barcode():
    while True:
        next_action = welcome_page()
        if next_action == 'scan':
            print("Scan a barcode:")
            barcode = input().strip()
            if barcode:
                create_file_with_barcode_data(barcode)
        else:
            break

if __name__ == "__main__":
    read_barcode()
