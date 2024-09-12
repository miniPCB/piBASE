import os
import csv
from tkinter import ttk, Frame, Label, Button, Entry, StringVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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

        # Add the Devices tab
        self.add_devices_tab()

    def add_floorplan_tab(self):
        # Create a new frame for the Floorplan tab
        floorplan_frame = Frame(self.notebook)
        floorplan_frame.pack(fill='both', expand=True)

        # Create a Matplotlib figure
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Add a simple plot or SVG if needed
        ax.plot([0, 1, 2], [0, 1, 0])

        # Embed the Matplotlib figure into the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=floorplan_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Add the Floorplan tab to the notebook
        self.notebook.add(floorplan_frame, text="Floorplan")

    def add_devices_tab(self):
        # Create the Devices tab with sub-tabs
        devices_frame = Frame(self.notebook)
        devices_frame.pack(fill='both', expand=True)

        devices_notebook = ttk.Notebook(devices_frame)
        devices_notebook.pack(expand=True, fill='both')

        # Create sub-tabs for Device 1, Device 2, Device 3, and Device 4
        for i in range(1, 5):
            device_frame = Frame(devices_notebook)
            device_frame.pack(fill='both', expand=True)

            # Create a StringVar to hold the tab name
            tab_name_var = StringVar(value=f"Device {i}")

            # Create a frame to hold the form field and button
            form_frame = Frame(device_frame)
            form_frame.pack(fill='x', pady=10, padx=10, anchor="w")

            # Create an entry field and a button to change the tab name
            entry = Entry(form_frame, textvariable=tab_name_var, font=("Helvetica", 12))
            entry.pack(side="left", padx=(0, 10))

            def change_tab_name(tab_index=i, var=tab_name_var):
                devices_notebook.tab(tab_index-1, text=var.get())

            button = Button(form_frame, text="Change Name", command=change_tab_name, font=("Helvetica", 12))
            button.pack(side="left")

            # Horizontal line separator
            separator = ttk.Separator(device_frame, orient='horizontal')
            separator.pack(fill='x', pady=10)

            # Create a frame to hold the chart
            chart_frame = Frame(device_frame)
            chart_frame.pack(fill='both', expand=True)

            # Create a Matplotlib figure for the chart
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

            # Initialize the plot lines for four channels
            lines = [ax.plot([], [], label=f'Channel {j}')[0] for j in range(1, 5)]

            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Voltage (V)")
            ax.set_title(f"Device {i} - Voltage Over Time")
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)

            # Embed the Matplotlib figure into the Tkinter canvas
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.get_tk_widget().pack(fill='both', expand=True)

            # Function to update the plot with new data
            def update_chart(frame, lines=lines):
                try:
                    # Read the latest data from the CSV file
                    with open(f"device_data_{i}.csv", "r") as csvfile:
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
                    print(f"Error updating chart for Device {i}: {e}")

            # Animate the plot with data from the CSV file
            anim = FuncAnimation(fig, update_chart, interval=100, cache_frame_data=False)

            # Add the device tab to the devices notebook
            devices_notebook.add(device_frame, text=f"Device {i}")

        # Add the Devices tab to the main notebook
        self.notebook.add(devices_frame, text="Devices")
