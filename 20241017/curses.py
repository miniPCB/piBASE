import curses
import json
import os
from datetime import datetime

# Define the path for both task and tasker JSON files
tasker_json_file = 'tasker.json'
tasks_json_file = 'tasks.json'

# Task structure
tasks_template = []

# Load and save functions for JSON data
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

def load_tasks_data():
    """Load tasks.json data."""
    return load_json_data(tasks_json_file, tasks_template)

def save_tasks_data(data):
    """Save tasks data to tasks.json."""
    save_json_data(tasks_json_file, data)

def display_task(stdscr, task):
    """Display task details."""
    stdscr.clear()
    stdscr.addstr(0, 0, f"Task ID: {task['task_id']}")
    stdscr.addstr(1, 0, f"Title: {task['title']}")
    stdscr.addstr(2, 0, f"Description: {task['description']}")
    stdscr.addstr(3, 0, f"Originator: {task['originator']}")
    stdscr.addstr(4, 0, f"Assignees: {', '.join(task['assignees'])}")
    stdscr.addstr(5, 0, f"Created Date: {task['created_date']}")
    stdscr.addstr(6, 0, f"Completed Date: {task['completed_date']}")
    stdscr.addstr(8, 0, "Press any key to return...")
    stdscr.refresh()
    stdscr.getch()

def main_menu(stdscr):
    """Main menu for viewing and editing tasks."""
    curses.curs_set(0)  # Hide the cursor
    tasks = load_tasks_data()

    menu_options = ['View Tasks', 'Edit Tasks', 'Exit']
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Tasker Menu (use arrow keys to navigate, Enter to select)")

        for idx, option in enumerate(menu_options):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 2, 0, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 2, 0, option)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            if current_row == 0:
                view_tasks(stdscr, tasks)
            elif current_row == 1:
                edit_tasks(stdscr, tasks)
            elif current_row == 2:
                break

def view_tasks(stdscr, tasks):
    """View all tasks stored in tasks.json."""
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "View Tasks (use arrow keys to navigate, Enter to view, Q to quit)")
        
        for idx, task in enumerate(tasks):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 2, 0, f"{task['task_id']}: {task['title']}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 2, 0, f"{task['task_id']}: {task['title']}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tasks) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            display_task(stdscr, tasks[current_row])
        elif key in [ord('q'), ord('Q')]:
            break

def edit_tasks(stdscr, tasks):
    """Edit existing tasks."""
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Edit Tasks (use arrow keys to navigate, Enter to edit, Q to quit)")
        
        for idx, task in enumerate(tasks):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 2, 0, f"{task['task_id']}: {task['title']}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 2, 0, f"{task['task_id']}: {task['title']}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tasks) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            edit_task_fields(stdscr, tasks[current_row])
        elif key in [ord('q'), ord('Q')]:
            break

def edit_task_fields(stdscr, task):
    """Edit specific fields of a task."""
    stdscr.clear()
    stdscr.addstr(0, 0, "Editing Task Fields:")
    stdscr.addstr(1, 0, f"Title: {task['title']}")
    stdscr.addstr(2, 0, f"Description: {task['description']}")
    stdscr.addstr(3, 0, f"Originator: {task['originator']}")
    stdscr.addstr(4, 0, f"Assignees: {', '.join(task['assignees'])}")
    stdscr.addstr(6, 0, "Press any key to go back...")
    stdscr.refresh()
    stdscr.getch()

def curses_main(stdscr):
    """Initialize colors and start the curses interface."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Highlight color
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(curses_main)
