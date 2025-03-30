import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

# File paths
dictionary_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Dictionary of soft skills (11).xlsx"
input_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\AI_ML_LLM\Filtered_Job_Posts_AIML_Fixed.json"
output_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\AI_ML_LLM\Soft_Skills_Occurrences_v11_Yearly_Once_Per_Post.json"

# Load the dictionary of soft skills from Excel
df = pd.read_excel(dictionary_path)

# Prepare the dictionary of skills and subcategories
soft_skills = defaultdict(list)
for _, row in df.iterrows():
    headcategory = str(row['Headcategory']).strip()
    subcategory = str(row['Subcategory']).strip()
    if headcategory and subcategory:
        soft_skills[headcategory].append(subcategory)

# Load the filtered JSON file
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Prepare the output data structure
output_data = {}

# Iterate through each year and count soft skill occurrences (once per job post)
for year, details in tqdm(sorted(data.items()), desc="Processing Job Posts"):
    # Ignore 2025
    if year == "2025":
        continue

    total_job_posts = 0
    skill_counts = defaultdict(int)
    posts = details.get("posts", [])

    # Iterate over the list of posts directly
    for post in posts:
        total_job_posts += 1  # Count each job post

        # Track whether each headcategory has been counted for this post
        counted_headcategories = set()

        # Check for each soft skill and its subcategories
        for headcategory, subcategories in soft_skills.items():
            # Check if the headcategory or any of its subcategories appear in the post
            if (headcategory.lower() in post.lower() or 
                any(sub.lower() in post.lower() for sub in subcategories)):
                if headcategory not in counted_headcategories:
                    skill_counts[headcategory] += 1
                    counted_headcategories.add(headcategory)

    # Save the counts for the year
    output_data[year] = {
        "total_job_posts": total_job_posts,
        "soft_skill_counts": dict(skill_counts)
    }

# Save the results to a new JSON file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(output_data, output_file, indent=4)

print(f"Soft skill occurrences (once per job post) saved to {output_file_path}")
