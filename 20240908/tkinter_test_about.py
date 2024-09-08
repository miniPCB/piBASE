import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Tabbed Window Example")
root.geometry("400x300")  # Set window size

# Create a notebook (tab control) for the main tabs
main_notebook = ttk.Notebook(root)

# Create the "Testing" tab
testing_tab = ttk.Frame(main_notebook)
main_notebook.add(testing_tab, text="Testing")

# Create a notebook (tab control) for the sub-tabs inside "Testing"
sub_notebook = ttk.Notebook(testing_tab)

# Create the "Test Controls" sub-tab
test_controls_tab = ttk.Frame(sub_notebook)
sub_notebook.add(test_controls_tab, text="Test Controls")

# Add content to the "Test Controls" sub-tab
test_controls_label = ttk.Label(test_controls_tab, text="This is the Test Controls sub-tab")
test_controls_label.pack(pady=20, padx=20)

# Create the "Test Reports" sub-tab
test_reports_tab = ttk.Frame(sub_notebook)
sub_notebook.add(test_reports_tab, text="Test Reports")

# Add content to the "Test Reports" sub-tab
test_reports_label = ttk.Label(test_reports_tab, text="This is the Test Reports sub-tab")
test_reports_label.pack(pady=20, padx=20)

# Pack the sub-notebook to make the sub-tabs visible
sub_notebook.pack(expand=True, fill="both")

# Create the "About" tab
about_tab = ttk.Frame(main_notebook)
main_notebook.add(about_tab, text="About")

# Add a label to the "About" tab
about_label = ttk.Label(about_tab, text="This is the About tab")
about_label.pack(pady=20, padx=20)

# Pack the main notebook to make the main tabs visible
main_notebook.pack(expand=True, fill="both")

# Start the main event loop
root.mainloop()
