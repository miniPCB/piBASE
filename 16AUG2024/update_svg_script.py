import csv
from xml.etree import ElementTree as ET

# Function to update the stroke colors in the SVG
def update_svg_colors(svg_file, csv_file, output_file):
    # Parse the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Handle namespaces if they exist
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Load the colors from the CSV file
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if present
        colors = list(csv_reader)
    
    # Define the quadrants to update (circle sets)
    quadrant_ids = ['q1c', 'q2c', 'q3c', 'q4c']
    
    # Process each row and update the SVG
    for row_idx, row in enumerate(colors):
        print(f"Processing row {row_idx} with colors: {row[1:]}")
        for quadrant_idx, color in enumerate(row[1:]):  # Skip the row identifier
            # Construct the circle ID (e.g., q1c1, q2c1, q3c1, q4c1)
            circle_id = f'q{quadrant_idx + 1}c{row_idx + 1}'
            circle = root.find(f".//svg:circle[@id='{circle_id}']", namespaces)
            if circle is not None:
                print(f"Updating circle {circle_id} to color {color}")
                circle.set('stroke', color.strip("'"))  # Remove any surrounding quotes
            else:
                print(f"Circle with ID {circle_id} not found.")
    
    # Write the updated SVG to a file
    tree.write(output_file)