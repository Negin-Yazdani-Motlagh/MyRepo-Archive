import json
import re
from collections import defaultdict
from tqdm import tqdm

# File paths
input_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Yearly_Job_Posts.json"
output_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Grouped_Yearly.json"

# Keywords to search for (grouped)
keyword_groups = {
    "AI": [r"\bAI\b", r"\bArtificial Intelligence\b"],
    "ML": [r"\bML\b", r"\bMachine Learning\b"],
    "LLM": [r"\bLLM\b", r"\bLarge Language Model\b"]
}

# Initialize a dictionary to store results
filtered_data = defaultdict(lambda: {
    "total_occurrences": 0,
    "AI": [],
    "ML": [],
    "LLM": []
})

# Load the nested JSON file
with open(input_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Iterate through each year and count occurrences
for year, details in tqdm(data.get("YC", {}).items(), desc="Processing Job Posts"):
    job_posts = details.get("comments", [])

    for post in job_posts:
        found = False
        for group, keywords in keyword_groups.items():
            # Check for keyword occurrences using regex
            if any(re.search(keyword, post, re.IGNORECASE) for keyword in keywords):
                filtered_data[year][group].append(post)
                filtered_data[year]["total_occurrences"] += 1
                found = True
                break  # Stop checking other groups once matched

# Save the filtered data to a new JSON file
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(filtered_data, output_file, indent=4)

print(f"Filtered job posts saved to {output_file_path}")
