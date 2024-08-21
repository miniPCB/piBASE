import os
import sys
import subprocess

# Function to install GitPython using apt
def install_gitpython():
    try:
        print("Installing GitPython using apt...")
        subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-git"])
        print("GitPython installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install GitPython: {e}")
        sys.exit(1)

# Check if gitpython is installed, and install it if not
try:
    import git
except ModuleNotFoundError:
    print("GitPython is not installed.")
    install_gitpython()
    import git  # Try importing again after installation

# Your existing script continues here

INSTAL_PATH = '/home/pi/piBASE'
DATALOGGER_GITHUB = 'https://github.com/miniPCB/piBASE.git'

def print_intro():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("miniPCB")
    print("piBASE: System Update")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def print_menu():
    print("\n--- Select a Test ---")
    print("[1] Push System")
    print("[X] Exit")

def push_to_github(repository, directory, commit_message):
    try:
        # Check if the directory exists and contains a .git folder
        if not os.path.exists(directory) or not os.path.exists(os.path.join(directory, '.git')):
            print(f"Cloning repository from {repository} to {directory}...")
            git.Repo.clone_from(repository, directory)

        # Initialize the repository
        repo = git.Repo(directory)

        # Add all changes to the staging area
        print("Adding all changes to staging...")
        repo.git.add('--all')

        # Commit the changes
        print(f"Committing changes with message: {commit_message}")
        repo.index.commit(commit_message)

        # Push the changes to the remote repository
        print("Pushing changes to the remote repository...")
        origin = repo.remote(name='origin')
        origin.push()

        print("Push completed successfully!")
    except git.exc.GitError as e:
        print(f"An error occurred while pushing to GitHub: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def datalogger2git(commit_message):
    print("\nPushing to GitHub...")
    push_to_github(DATALOGGER_GITHUB, INSTAL_PATH, commit_message)

def main():
    print_intro()
    while True:
        print_menu()
        choice = input("\nEnter menu selection: ").strip().lower()
        if choice == '1':
            commit_message = input("\nEnter commit message: ").strip()
            if commit_message:  # Ensure the commit message isn't empty
                datalogger2git(commit_message)
            else:
                print("Commit message cannot be empty.")
            break
        elif choice == 'x':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
