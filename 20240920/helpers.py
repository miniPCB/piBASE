import os
import json
from PIL import Image, ImageTk
import re

PARTS_LIST_FILE = "PartsList.json"
PART_CATALOG_FILE = "PartsCatalog.json"
PART_NUMBER_PATTERN = re.compile(r'^(?P<category>\d{2})(?P<subcategory>[A-Z])-?(?P<part>\d{2,3})$')

def set_window_icon(app, icon_path):
    icon = Image.open(icon_path)
    icon = icon.resize((32, 32), Image.Resampling.LANCZOS)
    app.iconphoto(False, ImageTk.PhotoImage(icon))

def load_parts():
    if not os.path.exists(PARTS_LIST_FILE):
        return []
    with open(PARTS_LIST_FILE, "r") as file:
        return json.load(file)

def load_part_catalog():
    try:
        with open("PartsCatalog.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Handle the case where the file is empty or corrupted
        print("Error: PartsCatalog.json is invalid or empty. Initializing with an empty catalog.")
        return {}
    except FileNotFoundError:
        # Handle the case where the file doesn't exist yet
        print("Error: PartsCatalog.json not found. Initializing with an empty catalog.")
        return {}

def save_parts(parts):
    parts.sort(key=lambda x: x['partnumber'])
    with open(PARTS_LIST_FILE, "w") as file:
        json.dump(parts, file, indent=4)
