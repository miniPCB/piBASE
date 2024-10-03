import subprocess
import sys
import json

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import the wordcloud package, if it fails, install it
try:
    from wordcloud import WordCloud
except ImportError:
    print("wordcloud package not found. Installing...")
    install("wordcloud")
    from wordcloud import WordCloud

import matplotlib.pyplot as plt

# Sample JSON array as a string (replace this with your actual JSON data)
json_data = '''
[
    "Electrical Engineering", 
    "Hardware Design", 
    "Altium", 
    "Microcontrollers", 
    "Signal Processing", 
    "PCB Layout", 
    "Embedded Systems", 
    "Circuit Simulation", 
    "Data Logging", 
    "Python", 
    "Testing", 
    "Prototyping"
]
'''

# Parse the JSON array
words = json.loads(json_data)

# Join the words/phrases into a single string
word_string = ' '.join(words)

# Create a word cloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(word_string)

# Display the generated word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off axis
plt.show()
