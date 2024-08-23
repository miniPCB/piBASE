import random
import csv

def generate_random_color(csv_file):
    colors = []
    for _ in range(20):  # Assuming you need 20 random colors
        color = "#{:06x}".format(random.randint(0, 0xFFFFFFFF))  # Generate a random hex color
        colors.append(color)
    
    # Writing to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['ID', 'Q1', 'Q2', 'Q3', 'Q4'])  # Assuming a header
        for i in range(20):
            csv_writer.writerow([f'row{i+1}', colors[i], colors[i], colors[i], colors[i]])  # Assuming the same color in each quadrant