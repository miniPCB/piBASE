import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to automatically install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import the 'requests' package and install it if it's missing
try:
    import requests
except ModuleNotFoundError:
    print("Module 'requests' not found, installing it...")
    install_package('requests')
    import requests  # Import again after installation

# Try to import the 'BeautifulSoup' package from 'bs4' and install it if it's missing
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Module 'bs4' not found, installing it...")
    install_package('bs4')
    from bs4 import BeautifulSoup  # Import again after installation

# Custom headers to simulate a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to ensure a URL has a scheme (http or https)
def ensure_scheme(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url  # Default to https
    return url

# List of keywords to filter course names (add more if needed)
keywords = ['Electronics', 'Engineering', 'Technology', 'Computer', 'Power']

# Regex pattern for common course ID formats (you can adjust this pattern as needed)
course_id_pattern = re.compile(r'\b[A-Z]{2,4}\d{2,4}\b')  # Example: EE101, CS205, MATH300

# Function to search for course names and course IDs, with retry logic
def search_course_info(website_url, retries=3, delay=5):
    website_url = ensure_scheme(website_url)  # Ensure the URL is valid with a scheme
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(website_url, headers=headers, timeout=10)  # Use custom headers and a timeout
            if response.status_code == 200:
                # Parse the website's content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Focus on specific tags that typically contain course info
                course_blocks = soup.find_all(['h2', 'h3', 'li', 'span', 'td'])  # Limit to tags likely to contain course info

                for block in course_blocks:
                    block_text = block.get_text(" ", strip=True)  # Get the text from the block

                    # Try to find a match for the course ID in the block
                    course_id_match = course_id_pattern.search(block_text)
                    if course_id_match:
                        course_id = course_id_match.group()  # Extract the matched course ID
                        course_name = block_text.replace(course_id, "").strip()  # Remove the ID to get the course name

                        # Check if the course name contains at least one keyword
                        if any(keyword.lower() in course_name.lower() for keyword in keywords):
                            print(f"Website: {website_url}\nCourse Name: {course_name}\nCourse ID: {course_id}\n")

                            # Save the results (optional: append to a file)
                            with open('found_course_info.txt', 'a') as output_file:
                                output_file.write(f"Website: {website_url}\nCourse Name: {course_name}\nCourse ID: {course_id}\n\n")

                return  # Exit function if successful

            else:
                print(f"Failed to access {website_url}, status code: {response.status_code}")
                return  # No need to retry if the server returned a non-200 status code

        except requests.exceptions.RequestException as e:
            print(f"Error accessing {website_url}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying... ({attempt}/{retries})")
                time.sleep(delay)  # Wait before retrying
            else:
                print(f"Failed to access {website_url} after {retries} attempts.")
                return  # Exit if maximum retries have been reached

# Function to parallelize the website processing
def process_websites_parallel(websites, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks for each website
        futures = [executor.submit(search_course_info, website) for website in websites]
        
        # As the tasks complete, process the results
        for future in as_completed(futures):
            try:
                future.result()  # Get the result (or catch exceptions)
            except Exception as e:
                print(f"An error occurred: {e}")

# Read the list of websites from the file and process them in parallel
with open('unique.txt', 'r') as infile:
    websites = [line.strip() for line in infile]  # List of websites
    
# Parallelize the processing with a maximum of 5 threads (you can adjust this)
process_websites_parallel(websites, max_workers=5)
