from tkinter import ttk, Frame, Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from svgpath2mpl import parse_path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

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

        # Add a simple label to the Monitors tab
        label = Label(monitors_frame, text="Monitors Tab Content")
        label.pack(pady=10, padx=10, fill='x', expand=True)  # Make label span entire width

        # Add the Monitors tab to the notebook
        self.notebook.add(monitors_frame, text="Monitors")
