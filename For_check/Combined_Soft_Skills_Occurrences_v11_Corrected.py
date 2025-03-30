import pandas as pd
import json
from tqdm import tqdm

# File paths
excel_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Dictionary of soft skills (11).xlsx'
json_input_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Yearly.json'
json_output_path = r'C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Combined_Soft_Skills_Occurrences_v11_Corrected.json'

# Load Excel Dictionary (v11)
dict_df = pd.read_excel(excel_path, sheet_name='Sheet1')

# Corrected category filtering explicitly:
categories = ['Personal Effectiveness & Growth',
              'Interpersonal & Leadership Skills',
              'Conceptual/thinking skills']

keywords_dict = {
    category: dict_df[dict_df['Headcategory'].str.lower().str.strip() == category.lower().strip()]['Subcategory']
             .dropna().str.lower().tolist()
    for category in categories
}

# Load JSON Job Posts Data
with open(json_input_path, 'r', encoding='utf-8') as file:
    job_posts_yearly = json.load(file)

# Counting for each year and category
combined_results = {}

for year in tqdm(sorted(job_posts_yearly.keys()), desc="Counting Skills per Year"):
    posts = job_posts_yearly[year]['posts']
    total_posts = len(posts)

    year_counts = {
        'total_job_posts': total_posts,
        'soft_skill_counts': {}
    }

    for cat, keywords in keywords_dict.items():
        skill_count = 0
        for description in posts:
            description_lower = description.lower()
            for keyword in keywords:
                skill_count += description_lower.count(keyword)
        year_counts['soft_skill_counts'][cat] = skill_count

    combined_results[year] = year_counts

# Save results explicitly to JSON
with open(json_output_path, 'w', encoding='utf-8') as outfile:
    json.dump(combined_results, outfile, indent=4)

print(f"Corrected combined JSON saved explicitly to {json_output_path}")
