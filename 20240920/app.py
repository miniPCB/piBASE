import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import json
import os
import re
from catalog import CatalogManager
from form_handler import FormHandler
from helpers import set_window_icon, load_parts, load_part_catalog, save_parts
from image_handler import load_and_resize_image
from config import *

class PartsManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up window
        set_window_icon(self, ICON)
        self.title(APPLICATION_TITLE)
        self.geometry(DEFAULT_WINDOW_SIZE)

        # Define the catalog file path as a class attribute
        self.PART_CATALOG_FILE = PART_CATALOG_FILE

        # Initialize parts list and catalog
        self.parts = load_parts()
        self.part_catalog = load_part_catalog()
        self.current_part_number = None
        self.current_category_and_subcategory = (None, None)

        # Initialize form fields dictionary
        self.form_fields = {}

        # Create CatalogManager and FormHandler
        self.catalog_manager = CatalogManager(self)
        self.form_handler = FormHandler(self)

        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create the View Catalog, Edit Catalog (combined), Part, and Read Catalog tabs
        self.view_catalog_tab = ttk.Frame(self.notebook)
        self.edit_catalog_tab = ttk.Frame(self.notebook)  # Combined tab for Category and Subcategory
        self.part_tab = ttk.Frame(self.notebook)
        self.read_catalog_tab = ttk.Frame(self.notebook)

        # Add the tabs to the notebook
        self.notebook.add(self.view_catalog_tab, text="View Catalog")
        self.notebook.add(self.edit_catalog_tab, text="Edit Catalog")
        self.notebook.add(self.part_tab, text="Edit Part")
        self.notebook.add(self.read_catalog_tab, text="Read Catalog")

        # Create the widgets for each tab
        from widgets import create_view_catalog_widgets, create_catalog_widgets, create_part_widgets, create_read_catalog_widgets
        
        create_view_catalog_widgets(self)
        create_catalog_widgets(self)  # Combined category and subcategory widgets
        create_part_widgets(self)
        create_read_catalog_widgets(self)

        # Initial population of the catalog listbox
        self.catalog_manager.update_catalog_listbox()

    def load_part_into_form(self, part_number):
        """Load the selected part into the form fields for editing."""
        self.current_part_number = part_number
        part = next((p for p in self.parts if p['partnumber'] == part_number), None)
        if part:
            self.form_fields["part number"].delete(0, tk.END)
            self.form_fields["part number"].insert(0, part['partnumber'])

            self.form_fields["name"].delete(0, tk.END)
            self.form_fields["name"].insert(0, part['name'])

            self.form_fields["description"].delete(1.0, tk.END)
            self.form_fields["description"].insert(1.0, part['description'])

            self.form_fields["revision"].delete(0, tk.END)
            self.form_fields["revision"].insert(0, part['revision'])

            # Display the associated image for the part
            self.display_part_image(part_number)

    def create_form(self):
        """Create the form fields for the Edit Part tab."""
        large_font = tkFont.Font(size=14)
        labels = ["Part Number", "Name", "Description", "Revision"]

        # Use a container for the form fields (frame)
        self.form_frame = tk.Frame(self.part_tab)
        self.form_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)

        for idx, label_text in enumerate(labels):
            label = tk.Label(self.form_frame, text=label_text, font=large_font)
            label.grid(row=idx, column=0, sticky=tk.W, pady=5)

            if label_text == "Description":
                description_text = tk.Text(self.form_frame, font=large_font, height=5, width=80)
                description_text.grid(row=idx, column=1, sticky=tk.EW, padx=5, pady=5)
                self.form_fields[label_text.lower()] = description_text
            else:
                entry = tk.Entry(self.form_frame, font=large_font)
                entry.grid(row=idx, column=1, sticky=tk.EW, padx=5, pady=5)
                self.form_fields[label_text.lower()] = entry

    def create_buttons(self, parent_tab, save_command, delete_command):
        """Create buttons for saving and deleting forms."""
        small_font = tkFont.Font(size=12)

        # Create a frame for the buttons at the bottom of the parent_tab
        button_frame = tk.Frame(parent_tab)
        button_frame.pack(side=tk.BOTTOM, pady=10)  # Ensure buttons are always at the bottom

        # Create Save and Delete buttons
        button_labels = ["Save", "Delete"]
        button_commands = [save_command, delete_command]

        # Loop through button labels and commands to create buttons
        for idx, (label, command) in enumerate(zip(button_labels, button_commands)):
            button = tk.Button(button_frame, text=label, command=command, width=10, height=2, font=small_font)
            button.grid(row=0, column=idx, padx=5)  # Ensure the buttons appear in a row

    def display_full_catalog(self):
        """Display the full catalog in the Read Catalog tab."""
        self.read_catalog_text.delete(1.0, tk.END)  # Clear existing text
        for category_code, category_info in self.part_catalog.items():
            self.read_catalog_text.insert(tk.END, f"{category_code}: {category_info['name']}\n")
            for subcategory_code, subcategory_name in category_info['subcategories'].items():
                self.read_catalog_text.insert(tk.END, f"\t{subcategory_code}: {subcategory_name}\n")
                filtered_parts = [part for part in self.parts if part['partnumber'].startswith(f"{category_code}{subcategory_code}-")]
                for part in filtered_parts:
                    self.read_catalog_text.insert(tk.END, f"\t\t{part['partnumber']}: {part['name']}\n")
            self.read_catalog_text.insert(tk.END, "\n")

    def clear_part_form(self):
        """Clear the form fields for adding a new part."""
        for field in self.form_fields.values():
            if isinstance(field, tk.Entry):
                field.delete(0, tk.END)  # Clear text from Entry widgets
            elif isinstance(field, tk.Text):
                field.delete(1.0, tk.END)  # Clear text from Text widgets

    def display_part_image(self, part_number):
        """Load and display the part's image in PNG format or a default image if not available."""
        png_file = f"images/{part_number}.png"  # Path to the part-specific PNG file
        default_png_file = "images/No_Image_Available.png"  # Path to the default PNG file

        # Try loading the part-specific image, fall back to the default image if not found
        photo = load_and_resize_image(png_file, 1000, 400) or load_and_resize_image(default_png_file, 1000, 400)

        # Check if the image label has been created, if not, create it
        if not hasattr(self, 'image_label'):
            self.image_label = tk.Label(self.part_tab)
            self.image_label.pack(side=tk.TOP, pady=10)

        # Set the image
        self.image_label.config(image=photo, text="")  # Clear any text if an image exists
        self.image_label.image = photo  # Keep reference to avoid garbage collection

if __name__ == "__main__":
    try:
        app = PartsManagerApp()
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
