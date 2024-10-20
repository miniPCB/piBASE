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

def save_tasks_data(tasks):
    """Save tasks data to tasks.json."""
    save_json_data(tasks_json_file, tasks)

def draw_menu_bar(stdscr, menu_items, current_item, fields_len):
    """Draw the bottom menu bar."""
    height, width = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(2))  # Green background for the menu
    stdscr.addstr(height - 2, 0, " " * width)
    stdscr.attroff(curses.color_pair(2))

    for idx, item in enumerate(menu_items):
        if idx + fields_len == current_item:  # Match index with current_item
            stdscr.attron(curses.color_pair(1))  # Highlighted item
            stdscr.addstr(height - 2, idx * 15, f"[{item}]")
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(height - 2, idx * 15, f"[{item}]")

def display_task(stdscr, task, tasks, task_idx):
    """Display task details and allow editing."""
    fields = ["Task ID", "Title", "Description", "Originator", "Assignees"]
    field_data = [task['task_id'], task['title'], task['description'], task['originator'], ', '.join(task['assignees'])]
    menu_items = ['Back', 'Edit Task', 'Exit']
    total_items = len(fields) + len(menu_items)
    current_item = 0

    while True:
        stdscr.clear()
        for idx, field in enumerate(fields):
            if idx == current_item:
                stdscr.attron(curses.color_pair(2))  # Green background for selected field
            stdscr.addstr(idx, 0, f"{field}: {field_data[idx]}")
            stdscr.attroff(curses.color_pair(2))

        # Draw the bottom menu bar
        draw_menu_bar(stdscr, menu_items, current_item, len(fields))
        
        stdscr.refresh()

        key = stdscr.getch()

        # Navigation between fields and menu bar
        if key == curses.KEY_UP and current_item > 0:
            current_item -= 1
        elif key == curses.KEY_DOWN and current_item < total_items - 1:
            current_item += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_item == len(fields):  # Back
                break
            elif current_item == len(fields) + 1:  # Edit Task
                edit_task(stdscr, task, tasks, task_idx)
            elif current_item == len(fields) + 2:  # Exit
                return 'exit'

def edit_task(stdscr, task, tasks, task_idx):
    """Edit specific fields of the selected task."""
    fields = ["Title", "Description", "Originator", "Assignees"]
    menu_items = ['Save', 'Cancel']
    total_items = len(fields) + len(menu_items)
    current_item = 0
    
    curses.echo()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Editing Task Fields:")
        
        # Display the fields with proper highlighting
        for idx, field in enumerate(fields):
            if idx == current_item:
                stdscr.attron(curses.color_pair(2))  # Green background for selected field
            stdscr.addstr(idx + 1, 0, f"[{idx + 1}] {field}: {task[field.lower()]}")
            stdscr.attroff(curses.color_pair(2))
        
        # Draw the bottom menu bar
        draw_menu_bar(stdscr, menu_items, current_item, len(fields))
        stdscr.refresh()

        key = stdscr.getch()

        # Unified navigation between fields and menu
        if key == curses.KEY_UP and current_item > 0:
            current_item -= 1
        elif key == curses.KEY_DOWN and current_item < total_items - 1:
            current_item += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_item < len(fields):
                edit_field(stdscr, task, fields[current_item])
            elif current_item == len(fields):  # Save
                tasks[task_idx] = task
                save_tasks_data(tasks)
                stdscr.addstr(7, 0, "Task saved successfully! Press any key to continue...")
                stdscr.refresh()
                stdscr.getch()
                break
            elif current_item == len(fields) + 1:  # Cancel
                break

def edit_field(stdscr, task, field):
    """Edit a specific field of the task."""
    curses.echo()
    stdscr.clear()

    # Highlight the current field in red when being edited
    stdscr.attron(curses.color_pair(1))  # Red background for edit mode
    stdscr.addstr(0, 0, f"Editing {field}: {task[field.lower()]}")
    stdscr.attroff(curses.color_pair(1))
    
    stdscr.addstr(1, 0, f"Enter new {field}: ")
    new_value = stdscr.getstr(1, len(f"Enter new {field}: ") + 1).decode("utf-8").strip()

    task[field.lower()] = new_value if field != "Assignees" else [x.strip() for x in new_value.split(',')]
    stdscr.addstr(2, 0, f"{field} updated successfully! Press any key to return...")
    stdscr.refresh()
    stdscr.getch()
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
                stdscr.attron(curses.color_pair(2))  # Green background for selected task
                stdscr.addstr(idx + 2, 0, f"{task['task_id']}: {task['title']}")
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(idx + 2, 0, f"{task['task_id']}: {task['title']}")

        # Draw the bottom menu bar (fields_len is 0 since there are no fields here)
        draw_menu_bar(stdscr, ['View Task', 'Edit Task', 'Exit'], 0, len(tasks))

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(tasks) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            action = display_task(stdscr, tasks[current_row], tasks, current_row)
            if action == 'exit':
                return 'exit'  # Exit from the view
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
                stdscr.attron(curses.color_pair(2))  # Green background for selected task
                stdscr.addstr(idx + 2, 0, row)
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(idx + 2, 0, row)

        # Draw the bottom menu bar (fields_len is 0 for the main menu)
        draw_menu_bar(stdscr, ['View Task', 'Edit Task', 'Exit'], current_row, 0)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                action = view_tasks(stdscr)
                if action == 'exit':
                    break  # Exit from the view
            elif current_row == 1:
                add_task(stdscr)
            elif current_row == 2:
                break

def curses_main(stdscr):
    """Initialize colors and start the curses interface."""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)   # Red background for editing
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN) # Green background for selected item
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(curses_main)
