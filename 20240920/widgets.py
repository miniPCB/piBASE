import tkinter as tk
import tkinter.font as tkFont

def create_view_catalog_widgets(app):
    # Create a frame to contain the entire section
    app.catalog_frame = tk.Frame(app.view_catalog_tab)
    app.catalog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Categories Section
    app.catalog_label = tk.Label(app.catalog_frame, text="Categories", font=tkFont.Font(size=14, weight="bold"))
    app.catalog_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(0, 5))

    app.catalog_listbox = tk.Listbox(app.catalog_frame, width=30, height=15, font=tkFont.Font(size=12))
    app.catalog_listbox.grid(row=1, column=0, sticky="nsew", padx=10)
    app.catalog_listbox.bind("<<ListboxSelect>>", app.catalog_manager.on_catalog_select)
    app.catalog_listbox.bind("<Double-Button-1>", app.catalog_manager.on_category_double_click)  # Double-click for category

    # Subcategories Section
    app.subcategory_label = tk.Label(app.catalog_frame, text="Subcategories", font=tkFont.Font(size=14, weight="bold"))
    app.subcategory_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=(0, 5))

    app.subcategory_listbox = tk.Listbox(app.catalog_frame, width=30, height=15, font=tkFont.Font(size=12))
    app.subcategory_listbox.grid(row=1, column=1, sticky="nsew", padx=10)
    app.subcategory_listbox.bind("<<ListboxSelect>>", app.catalog_manager.on_subcategory_select)
    app.subcategory_listbox.bind("<Double-Button-1>", app.catalog_manager.on_subcategory_double_click)  # Double-click for subcategory

    # Parts Section
    app.parts_label = tk.Label(app.catalog_frame, text="Parts", font=tkFont.Font(size=14, weight="bold"))
    app.parts_label.grid(row=0, column=2, sticky=tk.W, padx=10, pady=(0, 5))  # Positioned at row 0, column 2

    app.parts_listbox = tk.Listbox(app.catalog_frame, width=30, height=15, font=tkFont.Font(size=12))
    app.parts_listbox.grid(row=1, column=2, sticky="nsew", padx=10)  # Positioned at row 1, column 2
    app.parts_listbox.bind("<Double-Button-1>", app.catalog_manager.on_part_double_click)

    # Make sure the grid expands properly
    app.catalog_frame.grid_columnconfigure(0, weight=1)  # Allow the category column to expand
    app.catalog_frame.grid_columnconfigure(1, weight=1)  # Allow the subcategory column to expand
    app.catalog_frame.grid_columnconfigure(2, weight=1)  # Allow the parts column to expand
    app.catalog_frame.grid_rowconfigure(1, weight=1)     # Allow the row with listboxes to expand

def create_catalog_widgets(app):
    """Create the form for editing categories and subcategories in the Edit Catalog tab."""

    # Create the frame for the Edit Catalog tab
    app.catalog_frame = tk.Frame(app.edit_catalog_tab)
    app.catalog_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

    # --- Category Form Section ---
    app.category_label = tk.Label(app.catalog_frame, text="Category Code", font=tkFont.Font(size=14))
    app.category_label.grid(row=0, column=0, sticky=tk.W, pady=5)

    app.category_entry = tk.Entry(app.catalog_frame, font=tkFont.Font(size=14), width=40)
    app.category_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

    app.category_name_label = tk.Label(app.catalog_frame, text="Category Name", font=tkFont.Font(size=14))
    app.category_name_label.grid(row=1, column=0, sticky=tk.W, pady=5)

    app.category_name_entry = tk.Entry(app.catalog_frame, font=tkFont.Font(size=14), width=40)
    app.category_name_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

    # --- Subcategory Form Section ---
    app.subcategory_label = tk.Label(app.catalog_frame, text="Subcategory Code", font=tkFont.Font(size=14))
    app.subcategory_label.grid(row=3, column=0, sticky=tk.W, pady=5)

    app.subcategory_entry = tk.Entry(app.catalog_frame, font=tkFont.Font(size=14), width=40)
    app.subcategory_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

    app.subcategory_name_label = tk.Label(app.catalog_frame, text="Subcategory Name", font=tkFont.Font(size=14))
    app.subcategory_name_label.grid(row=4, column=0, sticky=tk.W, pady=5)

    app.subcategory_name_entry = tk.Entry(app.catalog_frame, font=tkFont.Font(size=14), width=40)
    app.subcategory_name_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

    # Make rows flexible
    app.catalog_frame.grid_rowconfigure(5, weight=1)

    # --- Buttons at the Bottom of the Edit Catalog form ---
    button_frame = tk.Frame(app.catalog_frame)
    button_frame.grid(row=6, columnspan=2, pady=10, sticky="ew")

    save_button = tk.Button(button_frame, text="Save", command=app.form_handler.save_catalog_entry, width=10, height=2)
    save_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_frame, text="Delete", command=app.form_handler.delete_catalog_entry, width=10, height=2)
    delete_button.pack(side=tk.LEFT, padx=5)

def create_part_widgets(app):
    """Create the form for editing parts."""
    
    # Create the frame for the part form inside the Edit Part tab
    app.form_frame = tk.Frame(app.part_tab)
    app.form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create the form fields by calling the create_form() method
    app.create_form()

    # --- Buttons at the Bottom of the Edit Part form ---
    button_frame = tk.Frame(app.part_tab)
    button_frame.pack(side=tk.BOTTOM, pady=10)

    save_button = tk.Button(button_frame, text="Save", command=app.form_handler.save_part, width=10, height=2)
    save_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_frame, text="Delete", command=app.form_handler.delete_part, width=10, height=2)
    delete_button.pack(side=tk.LEFT, padx=5)

def create_read_catalog_widgets(app):
    """Creates the Read Catalog pane that displays the entire catalog."""
    
    app.read_catalog_text = tk.Text(app.read_catalog_tab, wrap=tk.WORD, font=tkFont.Font(size=12))
    app.read_catalog_text.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

    # Populates the catalog in the read-only text box
    app.display_full_catalog()
