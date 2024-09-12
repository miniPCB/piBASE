import os
import csv
import json
from tkinter import ttk, Frame, Label, Button, Entry, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch
from svgpath2mpl import parse_path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

        # Add the Sensors tab
        self.add_sensors_tab()

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

        # Construct the path to the JSON file relative to the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(script_dir, "monitors.json")

        # Load monitor data from JSON file
        with open(json_file_path, "r") as file:
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

    def add_sensors_tab(self):
        # Create the Sensors tab with sub-tabs
        sensors_frame = Frame(self.notebook)
        sensors_frame.pack(fill='both', expand=True)

        sensors_notebook = ttk.Notebook(sensors_frame)
        sensors_notebook.pack(expand=True, fill='both')

        # Create sub-tabs for Sensor 1, Sensor 2, Sensor 3, and Sensor 4
        for i in range(1, 5):
            sensor_frame = Frame(sensors_notebook)
            sensor_frame.pack(fill='both', expand=True)

            # Create a StringVar to hold the tab name
            tab_name_var = StringVar(value=f"Sensor {i}")

            # Create a frame to hold the form field and button
            form_frame = Frame(sensor_frame)
            form_frame.pack(fill='x', pady=10, padx=10, anchor="w")

            # Create an entry field and a button to change the tab name
            entry = Entry(form_frame, textvariable=tab_name_var, font=("Helvetica", 12))
            entry.pack(side="left", padx=(0, 10))

            def change_tab_name(tab_index=i, var=tab_name_var):
                sensors_notebook.tab(tab_index-1, text=var.get())

            button = Button(form_frame, text="Change Name", command=change_tab_name, font=("Helvetica", 12))
            button.pack(side="left")

            # Horizontal line separator
            separator = ttk.Separator(sensor_frame, orient='horizontal')
            separator.pack(fill='x', pady=10)

            # Create a frame to hold the chart
            chart_frame = Frame(sensor_frame)
            chart_frame.pack(fill='both', expand=True)

            # Create a Matplotlib figure for the chart
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

            # Initialize the plot lines for four channels
            lines = [ax.plot([], [], label=f'Channel {j}')[0] for j in range(1, 5)]

            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Voltage (V)")
            ax.set_title(f"Sensor {i} - Voltage Over Time")
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)

            # Embed the Matplotlib figure into the Tkinter canvas
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)

            # Function to update the plot with new data
            def update_chart(frame, lines=lines):
                try:
                    # Read the latest data from the CSV file
                    with open(f"sensor_data_{i}.csv", "r") as csvfile:
                        reader = csv.reader(csvfile)
                        times, channels = [], [[] for _ in range(4)]
                        for row in reader:
                            times.append(float(row[0]))
                            for j in range(4):
                                channels[j].append(float(row[j + 1]))

                    # Update the data for each line
                    for j, line in enumerate(lines):
                        line.set_data(times, channels[j])

                    # Rescale the x and y axis to fit the new data
                    ax.relim()
                    ax.autoscale_view()
                except Exception as e:
                    print(f"Error updating chart for Sensor {i}: {e}")

            # Animate the plot with data from the CSV file
            anim = FuncAnimation(fig, update_chart, interval=100, cache_frame_data=False)

            # Add the sensor tab to the sensors notebook
            sensors_notebook.add(sensor_frame, text=f"Sensor {i}")

        # Add the Sensors tab to the main notebook
        self.notebook.add(sensors_frame, text="Sensors")
