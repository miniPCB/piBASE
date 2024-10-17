import subprocess
import sys
import json
import os
from datetime import datetime

# Check if PyInquirer is installed, if not, install it
try:
    from PyInquirer import prompt, Separator
except ImportError:
    print("PyInquirer not found. Installing it...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInquirer"])

    # Retry importing after installation
    from PyInquirer import prompt, Separator

# Define the path for both task and tasker JSON files
tasker_json_file = 'tasker.json'
tasks_json_file = 'tasks.json'

# Template structure for tasker.json
tasker_template = {
    "assignees": [],
    "unique_titles": [],
    "completion_counts": {},
    "duration_counters": {}
}

# Task structure
tasks_template = []

def load_json_data(file, template):
    """Load JSON data or create it if not present."""
    if not os.path.exists(file):
        return template
    with open(file, 'r') as f:
        return json.load(f)

def save_json_data(file, data):
    """Save data to JSON file."""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def load_tasker_data():
    """Load tasker.json data."""
    return load_json_data(tasker_json_file, tasker_template)

def load_tasks_data():
    """Load tasks.json data."""
    return load_json_data(tasks_json_file, tasks_template)

def save_tasker_data(data):
    """Save data to tasker.json."""
    save_json_data(tasker_json_file, data)

def save_tasks_data(data):
    """Save tasks data to tasks.json."""
    save_json_data(tasks_json_file, data)

def view_tasks():
    """View all tasks stored in tasks.json."""
    tasks = load_tasks_data()
    
    if not tasks:
        print("\nNo tasks available.")
        return

    questions = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Select a task to view:',
            'choices': [f"{task['task_id']}: {task['title']}" for task in tasks]
        }
    ]
    
    answer = prompt(questions)
    selected_task_id = int(answer['task'].split(':')[0])
    selected_task = next(task for task in tasks if task['task_id'] == selected_task_id)

    display_task(selected_task)

def display_task(task):
    """Display a single task."""
    print(f"\nTask ID: {task['task_id']}")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Originator: {task['originator']}")
    print(f"Assignees: {', '.join(task['assignees'])}")
    print(f"Created Date: {task['created_date']}")
    print(f"Completed Date: {task['completed_date']}")
    print()

def edit_task():
    """Edit an existing task."""
    tasks = load_tasks_data()

    if not tasks:
        print("\nNo tasks available to edit.")
        return

    # Select task to edit
    questions = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Select a task to edit:',
            'choices': [f"{task['task_id']}: {task['title']}" for task in tasks]
        }
    ]
    
    answer = prompt(questions)
    task_id = int(answer['task'].split(':')[0])
    task = next(t for t in tasks if t['task_id'] == task_id)

    # Fields to edit
    edit_questions = [
        {
            'type': 'list',
            'name': 'field',
            'message': 'Which field would you like to edit?',
            'choices': [
                'Title',
                'Description',
                'Originator',
                'Assignees',
                'Cancel'
            ]
        }
    ]

    field_answer = prompt(edit_questions)
    field_choice = field_answer['field'].lower()

    if field_choice == 'title':
        new_title = input("Enter new title: ").strip()
        task['title'] = new_title
    elif field_choice == 'description':
        new_description = input("Enter new description: ").strip()
        task['description'] = new_description
    elif field_choice == 'originator':
        new_originator = input("Enter new originator: ").strip()
        task['originator'] = new_originator
    elif field_choice == 'assignees':
        new_assignees = input("Enter new assignees (comma-separated): ").strip().split(',')
        task['assignees'] = [assignee.strip() for assignee in new_assignees]
    elif field_choice == 'cancel':
        print("Editing canceled.")
        return

    save_tasks_data(tasks)
    print("\nTask updated successfully!")

def main_menu():
    """Main menu for managing tasks and tasker.json."""
    questions = [
        {
            'type': 'list',
            'name': 'menu',
            'message': 'Select an option:',
            'choices': [
                'View tasks',
                'Edit task',
                'Exit'
            ]
        }
    ]

    while True:
        answer = prompt(questions)
        choice = answer['menu']

        if choice == 'View tasks':
            view_tasks()
        elif choice == 'Edit task':
            edit_task()
        elif choice == 'Exit':
            print("Exiting...")
            break

if __name__ == "__main__":
    main_menu()
