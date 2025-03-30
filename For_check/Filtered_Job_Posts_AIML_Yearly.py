import json
import re
from collections import defaultdict
from tqdm import tqdm

# File paths
input_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Yearly_Job_Posts.json"
output_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Yearly.json"

# Keywords to search for (regex patterns to match exact words only)
keywords = [
    r"\bAI\b",                          # AI as a standalone word
    r"\bML\b",                          # ML as a standalone word
    r"\bLLM\b",                         # LLM as a standalone word
    r"\bLarge Language Model\b",         # Large Language Model phrase
    r"\bArtificial Intelligence\b",      # Artificial Intelligence phrase
    r"\bMachine Learning\b"              # Machine Learning phrase
]

# Initialize a dictionary to store results
filtered_data = {}

# Load the nested JSON file
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Iterate through each year and count occurrences
for year, details in tqdm(data.get("YC", {}).items(), desc="Processing Job Posts"):
    year_posts = []
    total_occurrences = 0

    job_posts = details.get("comments", [])
    for post in job_posts:
        # Check for keyword occurrences using regex
        if any(re.search(keyword, post, re.IGNORECASE) for keyword in keywords):
            year_posts.append(post)
            total_occurrences += 1

    # Store results if there are any matched posts
    if total_occurrences > 0:
        filtered_data[year] = {
            "total_occurrences": total_occurrences,
            "posts": year_posts
        }

# Save the filtered data to a new JSON file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(filtered_data, output_file, indent=4)

print(f"Filtered job posts saved to {output_file_path}")
