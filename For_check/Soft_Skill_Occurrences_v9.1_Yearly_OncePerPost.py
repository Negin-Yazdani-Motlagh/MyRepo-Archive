import pandas as pd
import json
from collections import defaultdict
from tqdm import tqdm

# Explicit file paths
excel_path_v91 = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Dictionary of soft skills (9.1).xlsx'
json_input_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Yearly.json'
output_json_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Soft_Skill_Occurrences_v9.1_Yearly_OncePerPost.json'

# Load Excel dictionary (v9.1)
dict_df = pd.read_excel(excel_path_v91, sheet_name='Sheet1')

# Prepare keywords explicitly from Excel dictionary
categories = dict_df['Headcategory'].dropna().unique()
keywords_dict = defaultdict(list)
for category in categories:
    keywords = dict_df[dict_df['Headcategory'] == category]['Subcategory'].dropna().str.lower().tolist()
    keywords_dict[category] = keywords

# Load yearly JSON explicitly
with open(json_input_path, 'r', encoding='utf-8') as file:
    job_posts_yearly = json.load(file)

# Count explicitly (once per post)
results = {}

for year in tqdm(sorted(job_posts_yearly.keys()), desc="Counting Soft Skills Once Per Post (v9.1)"):
    posts = job_posts_yearly[year]['posts']
    year_counts = defaultdict(int)

    for description in posts:
        description_lower = description.lower()
        for category, keywords in keywords_dict.items():
            if any(keyword in description_lower for keyword in keywords):
                year_counts[category] += 1  # counted once per post explicitly

    results[year] = {
        'total_job_posts': len(posts),
        'soft_skill_counts': dict(year_counts)
    }

# Save explicitly
with open(output_json_path, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, indent=4)

print(f"Once-per-post occurrences explicitly saved to {output_json_path}")
