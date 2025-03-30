import json
from tqdm import tqdm

# File paths
yearly_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Yearly_Job_Posts.json"
grouped_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Grouped_Yearly_Fixed.json"
output_json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Filtered_Job_Posts_AIML_Grouped_Yearly_Updated.json"

# Load the yearly JSON file with total job posts
with open(yearly_json_path, "r", encoding="utf-8") as file:
    yearly_data = json.load(file)

# Load the grouped JSON to update
with open(grouped_json_path, "r", encoding="utf-8") as file:
    grouped_data = json.load(file)

# Update the grouped JSON with the total job posts from the yearly JSON
for year, details in tqdm(grouped_data.items(), desc="Updating Total Job Posts"):
    if year == "2025":
        continue

    # Get the total job posts from the yearly JSON
    total_job_posts = yearly_data.get("YC", {}).get(year, {}).get("total_job_posts", 0)
    grouped_data[year]["total_job_posts"] = total_job_posts

# Save the updated JSON
with open(output_json_path, "w", encoding="utf-8") as output_file:
    json.dump(grouped_data, output_file, indent=4)

print(f"Updated JSON saved to {output_json_path}")
