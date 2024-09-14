import os
from tkinter import ttk, Frame, Canvas
from cairosvg import svg2png
from PIL import Image, ImageTk

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

        # Convert SVG to PNG for displaying on the Canvas
        svg_file = "floorplan.svg"
        png_file = "floorplan.png"

        # Convert SVG to PNG
        svg2png(url=svg_file, write_to=png_file)

        # Load the PNG image and display it on the Canvas
        image = Image.open(png_file)
        photo = ImageTk.PhotoImage(image)

        canvas = Canvas(floorplan_frame, width=image.width, height=image.height)
        canvas.pack(fill='both', expand=True)
        canvas.create_image(0, 0, image=photo, anchor='nw')

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

            # Add the device tab to the devices notebook
            devices_notebook.add(device_frame, text=f"Device {i}")

        # Add the Devices tab to the main notebook
        self.notebook.add(devices_frame, text="Devices")
