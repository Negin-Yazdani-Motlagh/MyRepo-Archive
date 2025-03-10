import json
import pandas as pd
import re
from collections import defaultdict
from tqdm import tqdm

# Define file paths
dictionary_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Dictionary of soft skills (10).xlsx"
job_posts_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Feb_Nested_Job_Posts.json"
output_file = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Headcategory_Counts_OnePerJob_V10.json"

# Load the soft skills dictionary (V10)
df = pd.read_excel(dictionary_file)

# Convert dictionary to a lookup format (Subcategory → Headcategory)
subcategory_to_headcategory = {}
for _, row in df.iterrows():
    headcategory = str(row['Headcategory']).strip() if pd.notna(row['Headcategory']) else "Unknown"
    subcategory = str(row['Subcategory']).strip().lower() if pd.notna(row['Subcategory']) else None
    if subcategory:
        subcategory_to_headcategory[subcategory] = headcategory

# Precompile regex patterns for subcategories
compiled_patterns = {subcategory: re.compile(rf'\b{re.escape(subcategory)}\b', re.IGNORECASE) for subcategory in subcategory_to_headcategory}

# Load the job postings JSON file
with open(job_posts_file, "r", encoding="utf-8") as f:
    job_posts = json.load(f)

# Dictionary to store counts per month
date_wise_counts = defaultdict(lambda: defaultdict(int))

# Function to extract **all matching headcategories** per job post
def assign_headcategories(text):
    text_lower = text.lower()
    matched_headcategories = set()
    for subcategory, pattern in compiled_patterns.items():
        if pattern.search(text_lower):
            matched_headcategories.add(subcategory_to_headcategory[subcategory])
    return list(matched_headcategories)  # Return all matched headcategories

# Process job posts
for date, data in tqdm(job_posts["YC"].items(), desc="Processing Job Posts"):
    if "comments" not in data:
        continue
    
    # Track unique job posts per headcategory
    for job_text in data["comments"]:
        headcategories = assign_headcategories(job_text)  # Get all matched headcategories
        for headcategory in headcategories:
            date_wise_counts[date][headcategory] += 1  # Increment count for each headcategory
    
    # Store total job posts per month
    date_wise_counts[date]["numJobPost"] = data.get("numJobPost", 0)

# Convert results to JSON format
result_json = {"HeadcategoryCountsByDate": dict(date_wise_counts)}

# Save the results
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_json, f, indent=4)

print(f"Results saved to {output_file}")
