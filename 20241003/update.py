import os
import subprocess

def is_git_repo(folder):
    """Check if the folder is a Git repository."""
    return os.path.exists(os.path.join(folder, '.git'))

def fetch_and_pull(repo_path):
    """Fetch and pull the latest changes from the 'origin main' branch."""
    print(f"Updating repository: {repo_path}")
    
    # Change to the repo directory
    os.chdir(repo_path)
    
    # Run git fetch
    subprocess.run(["git", "fetch"], check=True)
    
    # Run git pull origin main
    subprocess.run(["git", "pull", "origin", "main"], check=True)

def scan_and_update_repos(start_dir):
    """Scan directories for Git repositories and update them."""
    for root, dirs, files in os.walk(start_dir):
        if is_git_repo(root):
            try:
                fetch_and_pull(root)
            except subprocess.CalledProcessError as e:
                print(f"Failed to update {root}: {e}")
            print('-' * 60)

if __name__ == "__main__":
    # Start directory (current directory)
    start_directory = os.getcwd()
    
    # Scan and update repositories
    scan_and_update_repos(start_directory)
