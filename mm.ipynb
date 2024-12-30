import re
import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the webpage content
url = "https://news.ycombinator.com/item?id=42297424"  # Hacker News job thread URL
response = requests.get(url)

if response.status_code == 200:
    print("Successfully fetched the webpage.")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    exit()

# Step 2: Parse the webpage using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Extract all text
all_text = soup.get_text(separator='\n')  # Get all text from the page

# Step 4: Define enhanced regex to match job posts and their details
# This regex captures job posts that follow the "Company | Location | Role | Format" format
job_pattern = re.compile(
    r'^(.*? \| .*? \| .*?(?:Full-Time|Contract|Remote|Onsite).*? \| .*?)$',
    re.MULTILINE
)

# Find all matching job posts
job_posts = job_pattern.findall(all_text)

# Step 5: Collect detailed job descriptions by matching blocks after job posts
detailed_jobs = []
lines = all_text.split('\n')  # Split text into lines for processing

for idx, line in enumerate(lines):
    if job_pattern.match(line):
        # Found a job post, start collecting details
        job_post = line.strip()
        description = []

        # Collect subsequent lines (descriptions) until the next job post or blank line
        for next_line in lines[idx + 1:]:
            if next_line.strip() == "" or job_pattern.match(next_line):
                break
            description.append(next_line.strip())

        # Combine the job post and its description
        detailed_jobs.append((job_post, " ".join(description)))

# Step 6: Display detailed job posts
if detailed_jobs:
    print(f"Found {len(detailed_jobs)} detailed job posts:\n")
    for i, (job, desc) in enumerate(detailed_jobs, 1):
        print(f"Job {i}:\n{job}\nDescription: {desc}\n{'-'*40}\n")
else:
    print("No detailed job posts found.")
import re
import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the webpage content
url = "https://news.ycombinator.com/item?id=42297424"  # Hacker News job thread URL
response = requests.get(url)

if response.status_code == 200:
    print("Successfully fetched the webpage.")
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    exit()

# Step 2: Parse the webpage using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Extract all text
all_text = soup.get_text(separator='\n')  # Get all text from the page

# Step 4: Define enhanced regex to match job posts and their details
# This regex captures job posts that follow the "Company | Location | Role | Format" format
job_pattern = re.compile(
    r'^(.*? \| .*? \| .*?(?:Full-Time|Contract|Remote|Onsite).*? \| .*?)$',
    re.MULTILINE
)

# Find all matching job posts
job_posts = job_pattern.findall(all_text)

# Step 5: Collect detailed job descriptions by matching blocks after job posts
detailed_jobs = []
lines = all_text.split('\n')  # Split text into lines for processing

for idx, line in enumerate(lines):
    if job_pattern.match(line):
        # Found a job post, start collecting details
        job_post = line.strip()
        description = []

        # Collect subsequent lines (descriptions) until the next job post or blank line
        for next_line in lines[idx + 1:]:
            if next_line.strip() == "" or job_pattern.match(next_line):
                break
            description.append(next_line.strip())

        # Combine the job post and its description
        detailed_jobs.append((job_post, " ".join(description)))

# Step 6: Display detailed job posts
if detailed_jobs:
    print(f"Found {len(detailed_jobs)} detailed job posts:\n")
    for i, (job, desc) in enumerate(detailed_jobs, 1):
        print(f"Job {i}:\n{job}\nDescription: {desc}\n{'-'*40}\n")
else:
    print("No detailed job posts found.")
