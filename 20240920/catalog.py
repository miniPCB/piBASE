import tkinter as tk
from tkinter import messagebox
import re

class CatalogManager:
    def __init__(self, app):
        self.app = app

    def on_catalog_select(self, event):
        """Update subcategory and parts listboxes when a category is selected."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_text = event.widget.get(index)
            match = re.match(r'^(\d{2}):', selected_text)
            if match:
                category_code = match.group(1)
                self.app.current_category_and_subcategory = (category_code, None)
                self.update_subcategory_listbox(category_code)
                self.app.parts_listbox.delete(0, tk.END)

    def on_subcategory_select(self, event):
        """Update parts listbox when a subcategory is selected."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_text = event.widget.get(index)
            match = re.match(r'^([A-Z]):', selected_text)
            if match:
                subcategory_code = match.group(1)
                category_code, _ = self.app.current_category_and_subcategory
                self.app.current_category_and_subcategory = (category_code, subcategory_code)
                self.update_parts_listbox(category_code, subcategory_code)

    def update_catalog_listbox(self):
        """Update the listbox in the View Catalog tab with categories."""
        
        self.app.catalog_listbox.delete(0, tk.END)

        print("Updating catalog listbox...")
        print("Catalog data:", self.app.part_catalog)

        for category_code, category_info in self.app.part_catalog.items():
            display_text = f"{category_code}: {category_info['name']}"
            self.app.catalog_listbox.insert(tk.END, display_text)
            print(f"Inserted category: {display_text}")

    def update_subcategory_listbox(self, category_code):
        """Update the subcategory listbox based on the selected category."""
        print(f"Updating subcategories for category {category_code}")  # Debugging
        self.app.subcategory_listbox.delete(0, tk.END)
        subcategories = self.app.part_catalog.get(category_code, {}).get("subcategories", {})
        print(f"Subcategories: {subcategories}")  # Debugging
        if not subcategories:
            self.app.subcategory_listbox.insert(tk.END, "No Subcategories Available")
        else:
            for subcategory_code, subcategory_name in subcategories.items():
                display_text = f"{subcategory_code}: {subcategory_name}"
                self.app.subcategory_listbox.insert(tk.END, display_text)

    def update_parts_listbox(self, category_code, subcategory_code):
        """Update the parts listbox based on the selected category and subcategory."""
        self.app.parts_listbox.delete(0, tk.END)  # Clear existing entries
        filtered_parts = [
            part for part in self.app.parts
            if part['partnumber'].startswith(f"{category_code}{subcategory_code}-")
        ]
        if not filtered_parts:
            self.app.parts_listbox.insert(tk.END, "No Parts Available")
        else:
            for part in filtered_parts:
                display_text = f"{part['partnumber']}, {part['name']}"
                self.app.parts_listbox.insert(tk.END, display_text)

    def on_part_double_click(self, event):
        """Handle the event when a part is double-clicked and load it into the form or open the form blank."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_text = event.widget.get(index)
            print(f"Double-clicked Part: {selected_text}")  # Debugging

            # If "No Parts Available" is clicked, open the form with blank fields
            if selected_text == "No Parts Available":
                self.app.clear_part_form()  # Clear the form fields
                self.app.notebook.select(self.app.part_tab)  # Switch to the Edit Part tab
                return

            # Otherwise, load the selected part into the form
            match = re.match(r'^(\d{2}[A-Z]-\d{2,3}), (.*)$', selected_text)
            if match:
                part_number = match.group(1)
                self.app.load_part_into_form(part_number)  # Load the selected part
                self.app.notebook.select(self.app.part_tab)  # Switch to the Edit Part tab

    def on_category_double_click(self, event):
        """Handle double-click on a category to open the Edit Catalog tab with the category populated."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_category = event.widget.get(index)
            category_code = selected_category.split(":")[0].strip()

            # Populate the Category fields in the Edit Catalog tab
            self.app.category_entry.delete(0, tk.END)
            self.app.category_entry.insert(0, category_code)

            category_name = self.app.part_catalog[category_code]['name']
            self.app.category_name_entry.delete(0, tk.END)
            self.app.category_name_entry.insert(0, category_name)

            # Clear subcategory fields
            self.app.subcategory_entry.delete(0, tk.END)
            self.app.subcategory_name_entry.delete(0, tk.END)

            # Switch to the Edit Catalog tab
            self.app.notebook.select(self.app.edit_catalog_tab)

    def on_subcategory_double_click(self, event):
        """Handle double-click on a subcategory to open the Edit Catalog tab with both category and subcategory populated."""
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_subcategory = event.widget.get(index)
            subcategory_code = selected_subcategory.split(":")[0].strip()

            # Retrieve the selected category from the internal state
            category_code, _ = self.app.current_category_and_subcategory

            if not category_code:
                print("Error: No category selected.")
                messagebox.showerror("Error", "Please select a category first.")
                return

            print(f"Updating subcategories for category {category_code}")
            subcategories = self.app.part_catalog[category_code]['subcategories']
            print(f"Subcategories: {subcategories}")

            # Populate the Category fields if not already populated (preserve them otherwise)
            if not self.app.category_entry.get():
                self.app.category_entry.delete(0, tk.END)
                self.app.category_entry.insert(0, category_code)

            category_name = self.app.part_catalog[category_code]['name']
            if not self.app.category_name_entry.get():
                self.app.category_name_entry.delete(0, tk.END)
                self.app.category_name_entry.insert(0, category_name)

            # Populate the Subcategory fields
            if subcategory_code in subcategories:
                self.app.subcategory_entry.delete(0, tk.END)
                self.app.subcategory_entry.insert(0, subcategory_code)

                subcategory_name = subcategories[subcategory_code]
                self.app.subcategory_name_entry.delete(0, tk.END)
                self.app.subcategory_name_entry.insert(0, subcategory_name)

                # Preserve the current category and subcategory for further interactions
                self.app.current_category_and_subcategory = (category_code, subcategory_code)

                # Switch to the Edit Catalog tab
                self.app.notebook.select(self.app.edit_catalog_tab)
            else:
                print("Error: Subcategory not found.")
                messagebox.showerror("Error", "Subcategory not found.")