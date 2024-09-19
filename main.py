import os
import sys
import subprocess

# Function to install GitPython dynamically based on the system type
def install_gitpython():
    try:
        print("GitPython not found. Attempting to install GitPython...")
        if sys.platform.startswith("linux"):  # Check if the system is Linux-based
            try:
                subprocess.check_call(["sudo", "apt-get", "update"])
                subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-git"])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install GitPython using apt: {e}")
                sys.exit(1)
        elif sys.platform == "win32":  # Windows-based system
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install GitPython using pip: {e}")
                sys.exit(1)
        else:
            print("Unsupported platform for automatic GitPython installation.")
            sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during GitPython installation: {e}")
        sys.exit(1)

# Check if gitpython is installed, and install it if not
try:
    import git
except ModuleNotFoundError:
    install_gitpython()
    import git  # Retry import after installation

# Detect OS and set repository path accordingly
if sys.platform.startswith("linux"):
    INSTALL_PATH = '/home/pi/piBASE'  # Path for Raspberry Pi
elif sys.platform == "win32":
    INSTALL_PATH = r'C:\Repos\piBASE'  # Path for Windows machine
else:
    print("Unsupported operating system.")
    sys.exit(1)

# GitHub repository URL
DATALOGGER_GITHUB = 'https://github.com/miniPCB/piBASE.git'

# Display program introduction
def print_intro():
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("miniPCB")
    print("piBASE: System Update")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# Display menu options
def print_menu():
    print("\n--- Select an Action ---")
    print("[1] Push System")
    print("[2] Pull System")
    print("[X] Exit")

# Function to pull the latest changes from the remote repository
def pull_from_github(repository, directory):
    try:
        # Check if the directory exists and is a Git repository
        if not os.path.exists(directory) or not os.path.exists(os.path.join(directory, '.git')):
            print(f"Cloning repository from {repository} to {directory}...")
            git.Repo.clone_from(repository, directory)
        else:
            # Pull the latest changes from the remote repository
            print("Pulling the latest changes from the remote repository...")
            repo = git.Repo(directory)
            origin = repo.remote(name='origin')
            origin.pull()

        print("Pull completed successfully!")
    except git.exc.GitError as e:
        print(f"Git error occurred while pulling: {e}")
        if 'invalid path' in str(e):
            print("It looks like there is an invalid path in the repository for Windows (such as a file with a colon ':'). Please rename the file in the remote repository to avoid this issue.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

# Function to push local changes to GitHub
def push_to_github(repository, directory, commit_message):
    try:
        # Check if the directory exists and is a Git repository
        if not os.path.exists(directory) or not os.path.exists(os.path.join(directory, '.git')):
            print(f"Cloning repository from {repository} to {directory}...")
            git.Repo.clone_from(repository, directory)
        else:
            print("Repository exists, pulling the latest changes...")
            repo = git.Repo(directory)
            origin = repo.remote(name='origin')
            origin.pull()  # Pull the latest changes before making new commits

        # Stage all changes
        print("Adding all changes to staging area...")
        repo.git.add('--all')

        # Commit the changes
        print(f"Committing changes with message: {commit_message}")
        repo.index.commit(commit_message)

        # Push the changes to GitHub
        print("Pushing changes to the remote repository...")
        origin.push()

        print("Push completed successfully!")
    except git.exc.GitError as e:
        print(f"Git error occurred: {e}")
        if 'invalid path' in str(e):
            print("It looks like there is an invalid path in the repository for Windows (such as a file with a colon ':'). Please rename the file in the remote repository to avoid this issue.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

# Wrapper function for the push action with user-provided commit message
def datalogger2git(commit_message):
    print("\nPreparing to push changes to GitHub...")
    push_to_github(DATALOGGER_GITHUB, INSTALL_PATH, commit_message)

# Main program loop
def main():
    print_intro()
    while True:
        print_menu()
        choice = input("\nEnter menu selection: ").strip().lower()

        if choice == '1':
            commit_message = ""
            while not commit_message:  # Ensure the user provides a valid commit message
                commit_message = input("\nEnter commit message: ").strip()
                if not commit_message:
                    print("Commit message cannot be empty. Please try again.")
            datalogger2git(commit_message)
            break

        elif choice == '2':
            print("\nPulling the latest changes from GitHub...")
            pull_from_github(DATALOGGER_GITHUB, INSTALL_PATH)
            break

        elif choice == 'x':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
