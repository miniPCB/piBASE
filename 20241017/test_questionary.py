import subprocess
import sys

# Try to import questionary, if not available, install it
try:
    import questionary
except ImportError:
    print("questionary not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "questionary"])
    import questionary

import json
from datetime import datetime

# Define the path for both task and tasker JSON files
tasker_json_file = 'tasker.json'
tasks_json_file = 'tasks.json'

# Template structure for tasks.json
tasks_template = []

def load_json_data(file, template):
    """Load JSON data or create it if not present."""
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return template

def save_json_data(file, data):
    """Save data to JSON file."""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def load_tasks_data():
    """Load tasks.json data."""
    return load_json_data(tasks_json_file, tasks_template)

def save_tasks_data(data):
    """Save tasks data to tasks.json."""
    save_json_data(tasks_json_file, data)

def display_task(task):
    """Display task details."""
    print(f"\nTask ID: {task['task_id']}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Originator: {task['originator']}")
    print(f"Assignees: {', '.join(task['assignees'])}")
    print(f"Created Date: {task['created_date']}")
    print(f"Completed Date: {task['completed_date']}")
    print()

def view_tasks():
    """View all tasks stored in tasks.json."""
    tasks = load_tasks_data()
    
    if not tasks:
        print("\nNo tasks available.")
        return

    choices = [f"{task['task_id']}: {task['title']}" for task in tasks]
    selected_task = questionary.select(
        "Select a task to view:",
        choices=choices
    ).ask()

    if selected_task:
        task_id = int(selected_task.split(":")[0])
        task = next(task for task in tasks if task['task_id'] == task_id)
        display_task(task)

def add_task():
    """Add a new task to tasks.json."""
    tasks = load_tasks_data()
    task_id = len(tasks) + 1
    title = questionary.text("Enter task title:").ask()
    description = questionary.text("Enter task description:").ask()
    originator = questionary.text("Enter originator name:").ask()
    assignees = questionary.text("Enter assignees (comma-separated):").ask().split(',')

    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    task = {
        "task_id": task_id,
        "title": title,
        "description": description,
        "originator": originator,
        "assignees": [assignee.strip() for assignee in assignees],
        "created_date": created_date,
        "completed_date": ""
    }

    tasks.append(task)
    save_tasks_data(tasks)
    print("\nTask added successfully!")

def main_menu():
    """Main menu for managing tasks."""
    while True:
        answer = questionary.select(
            "Select an option:",
            choices=[
                "View tasks",
                "Add task",
                "Exit"
            ]
        ).ask()

        if answer == "View tasks":
            view_tasks()
        elif answer == "Add task":
            add_task()
        elif answer == "Exit":
            print("Exiting...")
            break

if __name__ == "__main__":
    main_menu()
