from tkinter import ttk, Frame, Label, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from svgpath2mpl import parse_path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import json

class setup_tabs:
    def __init__(self, master):
        self.master = master
        self.master.title("Static Monitor")  # Set window title
        self.master.geometry("1280x720")  # Set window size

        # Create the main notebook (tab control)
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both')

        # Add the Floorplan tab
        self.add_floorplan_tab()

        # Add the Monitors tab
        self.add_monitors_tab()

    def add_floorplan_tab(self):
        # Create a new frame for the Floorplan tab
        floorplan_frame = Frame(self.notebook)
        floorplan_frame.pack(fill='both', expand=True)

        # Create a Matplotlib figure
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Example of parsing an SVG path (replace with your own SVG paths)
        svg_path = "M10 10 H 90 V 90 H 10 L 10 10"
        path = parse_path(svg_path)

        # Create a patch from the SVG path and add it to the plot
        patch = PathPatch(path, facecolor='none', edgecolor='black')
        ax.add_patch(patch)

        # Adjust the plot limits
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Remove axes for a cleaner look
        ax.axis('off')

        # Embed the Matplotlib figure into the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=floorplan_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add the Floorplan tab to the notebook
        self.notebook.add(floorplan_frame, text="Floorplan")

    def add_monitors_tab(self):
        # Create a new frame for the Monitors tab
        monitors_frame = Frame(self.notebook)
        monitors_frame.pack(fill='both', expand=True)

        # Load monitor data from JSON file
        with open("monitors.json", "r") as file:
            monitors = json.load(file)

        # Determine the grid size
        rows = 2
        columns = 2
        for index, monitor in enumerate(monitors):
            row = index // columns
            column = index % columns

            status_color = "green" if monitor["Status"] == "Running" else "red"
            button_text = f"Name: {monitor['Name']}\nSN: {monitor['SN']}\nStatus: {monitor['Status']}"

            button = Button(
                monitors_frame, text=button_text, bg=status_color, fg="white",
                font=("Helvetica", 12), width=20, height=5
            )
            button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Configure grid weights to make buttons expand to fill space
        for i in range(rows):
            monitors_frame.grid_rowconfigure(i, weight=1)
        for j in range(columns):
            monitors_frame.grid_columnconfigure(j, weight=1)

        # Add the Monitors tab to the notebook
        self.notebook.add(monitors_frame, text="Monitors")
