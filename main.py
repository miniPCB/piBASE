import git
import os

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

def push_to_github(repository,directory,commit_message):
    repo_url = repository
    local_dir = directory

    # Clone the repository if it doesn't exist locally
    if not os.path.exists(local_dir):
        git.Repo.clone_from(repo_url, local_dir)

    # Initialize the repository
    repo = git.Repo(local_dir)

    # Add all changes to the staging area
    repo.git.add('--all')

    # Commit the changes
    #commit_message = input("\nEnter commit message: ")
    repo.index.commit(commit_message)

    # Push the changes to the remote repository
    origin = repo.remote(name='origin')
    origin.push()

def datalogger2git(commit_message):
    print("\nPushing to Github")
    push_to_github(DATALOGGER_GITHUB,INSTAL_PATH,commit_message)

def main():
    print_intro()
    while True:
        print_menu()
        choice = input("\nEnter menu selection: ")
        choice=choice.strip().lower()
        if choice == '1':
            commit_message = input("\nEnter commit message: ")
            commit_message=commit_message.strip().lower()
            datalogger2git(commit_message)
            break
        elif choice == 'x':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()