import json
from collections import defaultdict

# Load the dataset (Nested JSON format)
with open(r'C:\Users\negin\Neginn\AI&Education\nested_Job_Posts.json', 'r') as f:
    data = json.load(f)

# Load the dictionary of soft skills
import pandas as pd
soft_skills_df = pd.read_excel(r'C:\Users\negin\Neginn\AI&Education\Excell\Dictionary of soft skills.xlsx')
soft_skills = set(soft_skills_df.stack().str.lower().dropna().tolist())  # Flatten and convert to lowercase

# Initialize the output structure
result = {"YC": defaultdict(dict)}

# Iterate through the nested JSON structure
for key, value in data["YC"].items():
    year_month = "-".join(key.split()[-2:])  # Extract year and month (e.g., "April 2011" -> "2011-4")
    if "comments" in value:
        comments = value["comments"]
        num_posts = value.get("numJobPost", len(comments))

        # Count occurrences of each soft skill in all comments
        skill_counts = {skill: 0 for skill in soft_skills}
        for comment in comments:
            comment_lower = comment.lower()
            for skill in soft_skills:
                skill_counts[skill] += comment_lower.count(skill)

        # Filter out skills with zero occurrences
        filtered_skill_counts = {skill: count for skill, count in skill_counts.items() if count > 0}

        # Save the results if there are any skills with occurrences
        if filtered_skill_counts:
            result["YC"][year_month] = {**filtered_skill_counts, "numJobPost": num_posts}

# Save the result to a JSON file
with open('soft_skills_analysis.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Analysis complete. Results saved to 'soft_skills_analysis.json'.")
