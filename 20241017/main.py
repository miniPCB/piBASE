import os
import subprocess
import sys

def list_scripts():
    """List all Python scripts in the current directory."""
    scripts = [f for f in os.listdir() if f.endswith('.py') and f != os.path.basename(__file__)]
    return sorted(scripts)

def display_menu(scripts):
    """Display the script list menu."""
    print("Available Python scripts:")
    for i, script in enumerate(scripts, start=1):
        print(f"[{i}] {script}")
    print("[X] Exit")

def run_script(script):
    """Run the selected script."""
    python_executable = sys.executable  # Use the current Python executable
    try:
        subprocess.run([python_executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script}: {e}")

def clear_screen():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # Linux/Unix/Mac

def main():
    while True:
        clear_screen()  # Clear screen before displaying the menu
        scripts = list_scripts()
        if not scripts:
            print("No Python scripts found in the current directory.")
            break

        display_menu(scripts)
        choice = input("\nSelect a script to run by entering the corresponding number, or 'X' to exit: ").strip()

        if choice.lower() == 'x':
            print("Exiting program.")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(scripts):
            selected_script = scripts[int(choice) - 1]
            print(f"\nRunning {selected_script}...\n")
            run_script(selected_script)
            input("\nPress Enter to return to the menu...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
