import pandas as pd
import json
import os
from collections import defaultdict

# File paths
soft_skills_file = r'C:\Users\negin\Desktop\Dictionary of soft skills (1).xlsx'
job_posts_file = r'C:\Users\negin\Desktop\nested_Job_Posts.json'

# Load soft skills from the Excel file
def load_soft_skills(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Soft skills file not found: {file_path}")
    skills_df = pd.read_excel(file_path)
    skills = set()
    for column in skills_df.columns:
        skills.update(skills_df[column].dropna().str.strip())
    return skills

# Recursive function to extract job descriptions from nested JSON
def extract_descriptions(data):
    descriptions = []
    if isinstance(data, dict):
        for key, value in data.items():
            descriptions.extend(extract_descriptions(value))
    elif isinstance(data, list):
        for item in data:
            descriptions.extend(extract_descriptions(item))
    elif isinstance(data, str):
        descriptions.append(data)
    return descriptions

# Process job posts and count skill occurrences
def process_job_posts(file_path, skills):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Job posts file not found: {file_path}")
    skill_counts_by_month = defaultdict(lambda: defaultdict(int))

    with open(file_path, 'r', encoding='utf-8') as file:
        job_data = json.load(file)

        # Extract all descriptions from the nested structure
        for key, value in job_data.items():
            descriptions = extract_descriptions(value)
            for description in descriptions:
                description = description.lower()
                for skill in skills:
                    if skill.lower() in description:
                        skill_counts_by_month[key][skill] += 1
            skill_counts_by_month[key]['numJobPost'] = len(descriptions)

    # Sort each month's skills by their counts in descending order
    sorted_skill_counts = {}
    for month, counts in skill_counts_by_month.items():
        sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
        sorted_skill_counts[month] = sorted_counts

    return sorted_skill_counts

# Save the nested JSON structure to a file
def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Main execution
if __name__ == "__main__":
    try:
        # Load skills and process job posts
        soft_skills = load_soft_skills(soft_skills_file)
        skill_counts = process_job_posts(job_posts_file, soft_skills)

        # Save the JSON data
        yc_data = {"YC": skill_counts}
        output_file = r'C:\Users\negin\Desktop\YC_skill_counts.json'
        save_to_json(yc_data, output_file)

        print(f"Nested JSON file saved to {output_file}")
    except FileNotFoundError as e:
        print(e)
