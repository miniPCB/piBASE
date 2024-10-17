import json
import os
from datetime import datetime

# Define the path for tasker.json
tasker_json_file = 'tasker.json'

# Template structure for tasker.json
tasker_template = {
    "assignees": [],
    "unique_titles": [],
    "completion_counts": {},
    "duration_counters": {}
}

def load_tasker_data():
    """Load tasker.json data or create it if not present."""
    if not os.path.exists(tasker_json_file):
        return tasker_template
    
    with open(tasker_json_file, 'r') as file:
        return json.load(file)

def save_tasker_data(data):
    """Save data to tasker.json."""
    with open(tasker_json_file, 'w') as file:
        json.dump(data, file, indent=4)

def add_assignee(assignee):
    """Add a new assignee to tasker.json if they don't exist."""
    data = load_tasker_data()
    
    if assignee not in data['assignees']:
        data['assignees'].append(assignee)
        data['completion_counts'][assignee] = {}
        print(f"Added new assignee: {assignee}")
    
    save_tasker_data(data)

def add_unique_title(title):
    """Add a unique title to tasker.json if it doesn't exist."""
    data = load_tasker_data()
    
    if title not in data['unique_titles']:
        data['unique_titles'].append(title)
        data['duration_counters'][title] = {}
        print(f"Added new task title: {title}")
    
    save_tasker_data(data)

def update_completion_count(assignee, title):
    """Update the completion count for an assignee and task title."""
    data = load_tasker_data()
    
    if assignee not in data['completion_counts']:
        add_assignee(assignee)
    
    if title not in data['completion_counts'][assignee]:
        data['completion_counts'][assignee][title] = 0
    
    data['completion_counts'][assignee][title] += 1
    print(f"Updated completion count: {assignee} completed '{title}' {data['completion_counts'][assignee][title]} times")
    
    save_tasker_data(data)

def add_duration(assignee, title, duration):
    """Add a task duration for a specific assignee and task title."""
    data = load_tasker_data()

    if title not in data['duration_counters']:
        add_unique_title(title)

    if assignee not in data['duration_counters'][title]:
        data['duration_counters'][title][assignee] = []
    
    data['duration_counters'][title][assignee].append(duration)
    print(f"Added duration of {duration} hours for {assignee} on '{title}'")
    
    save_tasker_data(data)

def display_tasker_data():
    """Display the content of tasker.json."""
    data = load_tasker_data()
    print(json.dumps(data, indent=4))

def main_menu():
    """Main menu for managing tasker.json."""
    while True:
        print("\nTasker Automation Menu:")
        print("[1] View tasker data")
        print("[2] Add assignee")
        print("[3] Add unique task title")
        print("[4] Update completion count")
        print("[5] Add task duration")
        print("[6] Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            display_tasker_data()
        elif choice == '2':
            assignee = input("Enter assignee name: ").strip()
            add_assignee(assignee)
        elif choice == '3':
            title = input("Enter task title: ").strip()
            add_unique_title(title)
        elif choice == '4':
            assignee = input("Enter assignee name: ").strip()
            title = input("Enter task title: ").strip()
            update_completion_count(assignee, title)
        elif choice == '5':
            assignee = input("Enter assignee name: ").strip()
            title = input("Enter task title: ").strip()
            duration = float(input("Enter duration in hours: ").strip())
            add_duration(assignee, title, duration)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
