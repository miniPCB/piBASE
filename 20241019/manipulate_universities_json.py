import requests
from bs4 import BeautifulSoup
import json
import os

# Load the JSON file from the same directory as the script
input_filename = 'universities.json'
output_filename = 'universities_with_names.json'

# Check if the file exists
if not os.path.exists(input_filename):
    print(f"File {input_filename} not found!")
    exit()

def scrape_university_name(url):
    """Scrape the university name from the website."""
    try:
        response = requests.get(url)
        
        # Ensure we got a valid response
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return "Unknown University"
        
        # Parse the HTML of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Attempt to find the university name in the <title> tag
        if soup.title:
            title_text = soup.title.string.strip()
            print(f"Found title for {url}: {title_text}")
            return title_text

        # Attempt to find the university name in <meta> tags (name or description)
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description and 'content' in meta_description.attrs:
            meta_text = meta_description.attrs['content'].strip()
            print(f"Found meta description for {url}: {meta_text}")
            return meta_text

        # Fallback if no title or meta description found
        print(f"No title or meta description found for {url}")
        return "Unknown University"
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return "Unknown University"

# Read the universities.json file
with open(input_filename, 'r') as file:
    data = json.load(file)

# Scrape the university names
for university in data["universities"]:
    url = university["url"]
    print(f"Scraping {url}...")
    university["name"] = scrape_university_name(url)

# Save the updated data to universities_with_names.json
with open(output_filename, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Updated university data saved to {output_filename}")
