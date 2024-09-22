import json
import tkinter as tk
from tkinter import messagebox
from helpers import PART_NUMBER_PATTERN, save_parts

class FormHandler:
    def __init__(self, app):
        self.app = app

    def save_catalog_entry(self):
        """Save or update category and subcategory entries in the catalog."""
        category_code = self.app.category_entry.get().strip()
        category_name = self.app.category_name_entry.get().strip()
        subcategory_code = self.app.subcategory_entry.get().strip()
        subcategory_name = self.app.subcategory_name_entry.get().strip()

        if category_code and category_name:
            if category_code not in self.app.part_catalog:
                # Create new category if it doesn't exist
                self.app.part_catalog[category_code] = {'name': category_name, 'subcategories': {}}
            else:
                # Update the category name if it exists
                self.app.part_catalog[category_code]['name'] = category_name

            # Add or update subcategory if both fields are filled
            if subcategory_code and subcategory_name:
                self.app.part_catalog[category_code]['subcategories'][subcategory_code] = subcategory_name

            # **Sort the catalog by category and subcategory before saving**
            sorted_catalog = {cat_code: {'name': cat['name'], 'subcategories': dict(sorted(cat['subcategories'].items()))}
                              for cat_code, cat in sorted(self.app.part_catalog.items())}

            # **Save the updated catalog to the JSON file**
            try:
                with open(self.app.PART_CATALOG_FILE, "w") as file:
                    json.dump(sorted_catalog, file, indent=4)
                # Update the internal catalog and UI
                self.app.part_catalog = sorted_catalog
                self.app.catalog_manager.update_catalog_listbox()
                self.app.display_full_catalog()
                messagebox.showinfo("Success", "Catalog entry saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save catalog: {e}")
        else:
            messagebox.showerror("Error", "Category code and name are required.")

    def delete_catalog_entry(self):
        """Delete category or subcategory from the catalog."""
        category_code = self.app.category_entry.get().strip()
        subcategory_code = self.app.subcategory_entry.get().strip()

        if category_code in self.app.part_catalog:
            # If a subcategory is selected, delete it
            if subcategory_code and subcategory_code in self.app.part_catalog[category_code]['subcategories']:
                del self.app.part_catalog[category_code]['subcategories'][subcategory_code]
                messagebox.showinfo("Success", "Subcategory deleted successfully.")
            else:
                # Otherwise, delete the category
                del self.app.part_catalog[category_code]
                messagebox.showinfo("Success", "Category deleted successfully.")

            # **Sort the catalog by category and subcategory before saving**
            sorted_catalog = {cat_code: {'name': cat['name'], 'subcategories': dict(sorted(cat['subcategories'].items()))}
                              for cat_code, cat in sorted(self.app.part_catalog.items())}

            # **Save the updated catalog to the JSON file**
            try:
                with open(self.app.PART_CATALOG_FILE, "w") as file:
                    json.dump(sorted_catalog, file, indent=4)
                # Update the internal catalog and UI
                self.app.part_catalog = sorted_catalog
                self.app.catalog_manager.update_catalog_listbox()
                self.app.display_full_catalog()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save catalog: {e}")

            # Clear form fields after deletion
            self.app.category_entry.delete(0, 'end')
            self.app.category_name_entry.delete(0, 'end')
            self.app.subcategory_entry.delete(0, 'end')
            self.app.subcategory_name_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Category or Subcategory not found.")

    def save_part(self):
        """Save or update a part in the parts list."""
        part_number = self.app.form_fields["part number"].get().upper()
        name = self.app.form_fields["name"].get().upper()
        description = self.app.form_fields["description"].get(1.0, 'end').strip().upper()
        revision = self.app.form_fields["revision"].get().upper()

        if not PART_NUMBER_PATTERN.match(part_number):
            messagebox.showerror("Invalid Part Number", "The part number must follow the format: CCX-PPP.")
            return

        part = next((p for p in self.app.parts if p['partnumber'] == part_number), None)
        if part:
            # Update existing part
            part['name'] = name
            part['description'] = description
            part['revision'] = revision
        else:
            # Add new part
            self.app.parts.append({
                'partnumber': part_number,
                'name': name,
                'description': description,
                'revision': revision
            })

        # Save updated parts list to file
        save_parts(self.app.parts)

        # Refresh the parts listbox
        category_code, subcategory_code = self.app.current_category_and_subcategory
        self.app.catalog_manager.update_parts_listbox(category_code, subcategory_code)
        self.app.display_full_catalog()

        messagebox.showinfo("Success", "Part saved successfully.")

    def delete_part(self):
        """Delete a part from the parts list."""
        if self.app.current_part_number:
            part = next((p for p in self.app.parts if p['partnumber'] == self.app.current_part_number), None)
            if part:
                self.app.parts.remove(part)
                save_parts(self.app.parts)
                self.app.catalog_manager.update_parts_listbox(*self.app.current_category_and_subcategory)
                self.app.display_full_catalog()
                messagebox.showinfo("Success", "Part deleted successfully.")
                self.add_new_part()

    def add_new_part(self):
        """Clear form fields to add a new part."""
        self.app.current_part_number = None
        for field in self.app.form_fields.values():
            if isinstance(field, tk.Entry):
                field.delete(0, 'end')
            elif isinstance(field, tk.Text):
                field.delete(1.0, 'end')
