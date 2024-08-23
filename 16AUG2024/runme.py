import time
from generate_colors import generate_random_color
from update_svg_script import update_svg_colors  # Assuming the original script is in update_svg_script.py
import csv
from xml.etree import ElementTree as ET

# File paths
svg_file = '/home/pi/Documents/16AUG2024/10.svg'
csv_file = '/home/pi/Documents/16AUG2024/colors.csv'
output_file = '/home/pi/Documents/16AUG2024/output.svg'

while True:
    update_svg_colors(svg_file, csv_file, output_file)
    generate_random_color(csv_file)  # Call the function to generate random colors
    print(f"SVG file '{output_file}' updated.")
    time.sleep(2)
