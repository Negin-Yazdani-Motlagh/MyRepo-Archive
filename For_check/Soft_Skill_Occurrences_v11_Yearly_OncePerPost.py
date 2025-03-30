import pandas as pd
import json
from collections import defaultdict
from tqdm import tqdm

# File paths (update if needed)
excel_path_v11 = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Dictionary of soft skills (11).xlsx'
json_input_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Yearly.json'
output_json_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Soft_Skill_Occurrences_v11_Yearly_OncePerPost.json'

# Load v11 dictionary
dict_df = pd.read_excel(excel_path_v11, sheet_name='Sheet1')

# Extract headcategories and build keyword mapping
categories = dict_df['Headcategory'].dropna().unique()
keywords_dict = defaultdict(list)

for category in categories:
    keywords = dict_df[dict_df['Headcategory'] == category]['Subcategory'].dropna().str.lower().tolist()
    keywords_dict[category] = keywords

# Load job posts JSON
with open(json_input_path, 'r', encoding='utf-8') as file:
    job_posts_yearly = json.load(file)

# Count once-per-post occurrences
results = {}

for year in tqdm(sorted(job_posts_yearly.keys()), desc="Counting Soft Skills Once Per Post (v11)"):
    posts = job_posts_yearly[year]['posts']
    year_counts = defaultdict(int)

    for description in posts:
        description_lower = description.lower()
        for category, keywords in keywords_dict.items():
            if any(keyword in description_lower for keyword in keywords):
                year_counts[category] += 1  # count once per post per category

    results[year] = {
        'total_job_posts': len(posts),
        'soft_skill_counts': dict(year_counts)
    }

# Save the results
with open(output_json_path, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, indent=4)

print(f"Once-per-post occurrences saved to: {output_json_path}")
