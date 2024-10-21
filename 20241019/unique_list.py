def get_unique_items(input_file, output_file):
    # Create an empty set to store unique items
    unique_items = set()

    # Open the input file and read lines
    with open(input_file, 'r') as infile:
        for line in infile:
            # Strip any extra whitespace and add each line to the set
            unique_items.add(line.strip())

    # Write the unique items to the output file
    with open(output_file, 'w') as outfile:
        for item in sorted(unique_items):
            outfile.write(item + '\n')

    print(f"Unique items have been written to {output_file}")

# Specify the input and output file names
input_file = 'websites.txt'
output_file = 'unique.txt'

# Call the function to process the files
get_unique_items(input_file, output_file)
