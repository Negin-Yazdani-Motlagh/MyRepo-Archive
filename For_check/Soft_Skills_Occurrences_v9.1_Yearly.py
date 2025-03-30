import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

# File paths
dictionary_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Dictionary of soft skills (9.1).xlsx"
input_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Yearly.json"
output_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\AI_ML_LLM\Soft_Skills_Occurrences_v9.1_Yearly.json"

# Load the dictionary of soft skills from Excel
df = pd.read_excel(dictionary_path)

# Prepare the dictionary of skills and subcategories
soft_skills = defaultdict(list)
for _, row in df.iterrows():
    headcategory = str(row['Headcategory']).strip()
    subcategory = str(row['Subcategory']).strip()
    if headcategory and subcategory:
        soft_skills[headcategory].append(subcategory)

# Load the filtered yearly JSON file
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Prepare the output data structure
output_data = {}

# Iterate through each year and count soft skill occurrences
for year, details in tqdm(sorted(data.items()), desc="Processing Yearly Data"):
    total_job_posts = len(details.get("posts", []))  # Count total job posts for the year
    skill_counts = defaultdict(int)

    # Iterate through each post in the year
    for post in details.get("posts", []):
        # Check for each soft skill and its subcategories
        for headcategory, subcategories in soft_skills.items():
            # Check if headcategory or any subcategory appears in the post
            if any(sub.lower() in post.lower() for sub in subcategories) or headcategory.lower() in post.lower():
                skill_counts[headcategory] += 1

    # Save the counts for the year
    output_data[year] = {
        "total_job_posts": total_job_posts,
        "soft_skill_counts": dict(skill_counts)
    }

# Save the results to a new JSON file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(output_data, output_file, indent=4)

print(f"Soft skill occurrences saved to {output_file_path}")
