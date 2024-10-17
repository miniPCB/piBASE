import curses
import json
from datetime import datetime

# Define the path for tasks JSON file
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

def display_task(stdscr, task):
    """Display task details and allow editing."""
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Task ID: {task['task_id']}")
        stdscr.addstr(1, 0, f"Title: {task['title']}")
        stdscr.addstr(2, 0, f"Description: {task['description']}")
        stdscr.addstr(3, 0, f"Originator: {task['originator']}")
        stdscr.addstr(4, 0, f"Assignees: {', '.join(task['assignees'])}")
        stdscr.addstr(6, 0, "Press 'E' to edit this task, 'Q' to go back.")
        stdscr.refresh()

        key = stdscr.getch()

        if key in [ord('q'), ord('Q')]:
            break
        elif key in [ord('e'), ord('E')]:
            edit_task(stdscr, task)

def edit_task(stdscr, task):
    """Edit specific fields of the selected task."""
    curses.echo()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Editing Task Fields:")
        stdscr.addstr(1, 0, f"[1] Title: {task['title']}")
        stdscr.addstr(2, 0, f"[2] Description: {task['description']}")
        stdscr.addstr(3, 0, f"[3] Originator: {task['originator']}")
        stdscr.addstr(4, 0, f"[4] Assignees: {', '.join(task['assignees'])}")
        stdscr.addstr(6, 0, "Enter the number of the field to edit (or 'Q' to quit):")
        stdscr.refresh()

        key = stdscr.getch()

        if key in [ord('q'), ord('Q')]:
            break
        elif key == ord('1'):
            stdscr.addstr(7, 0, "Enter new title: ")
            task['title'] = stdscr.getstr(7, 17).decode("utf-8").strip()
        elif key == ord('2'):
            stdscr.addstr(7, 0, "Enter new description: ")
            task['description'] = stdscr.getstr(7, 24).decode("utf-8").strip()
        elif key == ord('3'):
            stdscr.addstr(7, 0, "Enter new originator: ")
            task['originator'] = stdscr.getstr(7, 21).decode("utf-8").strip()
        elif key == ord('4'):
            stdscr.addstr(7, 0, "Enter new assignees (comma-separated): ")
            new_assignees = stdscr.getstr(7, 41).decode("utf-8").split(',')
            task['assignees'] = [assignee.strip() for assignee in new_assignees]

        # Save changes
        save_tasks_data(load_tasks_data())
        stdscr.addstr(9, 0, "Task updated successfully! Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        break

    curses.noecho()

def view_tasks(stdscr):
    """View all tasks stored in tasks.json."""
    tasks = load_tasks_data()
    current_row = 0

    if not tasks:
        stdscr.addstr(0, 0, "No tasks available. Press any key to return.")
        stdscr.getch()
        return

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

def add_task(stdscr):
    """Add a new task to tasks.json."""
    tasks = load_tasks_data()

    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter task title: ")
    title = stdscr.getstr(0, 18).decode("utf-8")

    stdscr.addstr(1, 0, "Enter task description: ")
    description = stdscr.getstr(1, 24).decode("utf-8")

    stdscr.addstr(2, 0, "Enter originator name: ")
    originator = stdscr.getstr(2, 20).decode("utf-8")

    stdscr.addstr(3, 0, "Enter assignees (comma-separated): ")
    assignees = stdscr.getstr(3, 34).decode("utf-8").split(',')

    curses.noecho()

    task_id = len(tasks) + 1
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_task = {
        "task_id": task_id,
        "title": title.strip(),
        "description": description.strip(),
        "originator": originator.strip(),
        "assignees": [assignee.strip() for assignee in assignees],
        "created_date": created_date,
        "completed_date": ""
    }

    tasks.append(new_task)
    save_tasks_data(tasks)
    
    stdscr.addstr(5, 0, "\nTask added successfully! Press any key to return...")
    stdscr.refresh()
    stdscr.getch()

def main_menu(stdscr):
    """Main menu for viewing, adding, and editing tasks."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.refresh()

    menu = ['View Tasks', 'Add Task', 'Exit']
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Tasker Menu (use arrow keys to navigate, Enter to select)")

        for idx, row in enumerate(menu):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 2, 0, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 2, 0, row)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                view_tasks(stdscr)
            elif current_row == 1:
                add_task(stdscr)
            elif current_row == 2:
                break

def curses_main(stdscr):
    """Initialize colors and start the curses interface."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Highlight color
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(curses_main)
