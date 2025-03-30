import json
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# File paths
grouped_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Grouped_Yearly_Updated.json"

# Load the grouped JSON file
with open(grouped_json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Prepare data for plotting
years = []
ai_percentages = []
ml_percentages = []
llm_percentages = []

# Calculate normalized occurrences
for year, details in tqdm(sorted(data.items()), desc="Processing Yearly Data"):
    if year == "2025":
        continue

    total_job_posts = details.get("total_job_posts", 0)
    ai_count = details.get("AI", {}).get("total_occurrences", 0)
    ml_count = details.get("ML", {}).get("total_occurrences", 0)
    llm_count = details.get("LLM", {}).get("total_occurrences", 0)

    # Normalization formula: (occurrences / total_job_posts) * 100
    ai_percentage = (ai_count / total_job_posts) * 100 if total_job_posts > 0 else 0
    ml_percentage = (ml_count / total_job_posts) * 100 if total_job_posts > 0 else 0
    llm_percentage = (llm_count / total_job_posts) * 100 if total_job_posts > 0 else 0

    years.append(year)
    ai_percentages.append(ai_percentage)
    ml_percentages.append(ml_percentage)
    llm_percentages.append(llm_percentage)

# Plotting the normalized occurrences
plt.figure(figsize=(10, 6))

plt.plot(years, ai_percentages, marker='o', label='AI', color='blue')
plt.plot(years, ml_percentages, marker='o', label='ML', color='orange')
plt.plot(years, llm_percentages, marker='o', label='LLM', color='green')

plt.title('Normalized AI/ML/LLM Occurrences as a Percentage of Job Posts (Yearly)')
plt.xlabel('Year')
plt.ylabel('Percentage of Job Posts (%)')
plt.grid(True)
plt.legend(title='Group')

# Save and show the plot
plt.savefig(r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Normalized_Occurrences_AIML_Yearly.png")
plt.show()

print("Figure saved successfully!")
