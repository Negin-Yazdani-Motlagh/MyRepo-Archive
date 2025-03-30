import json
import matplotlib.pyplot as plt

# File path for v9.1 JSON file
file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Soft_Skills_Occurrences_v9.1_Yearly_Once_Per_Post.json"
output_folder = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\AI_ML_LLM"

# Load the JSON data
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Prepare data for plotting
years = sorted(data.keys(), key=int)  # Sort years to ensure correct order
normalized_data = {}
for year in years:
    details = data[year]
    total_posts = details.get("total_job_posts", 1)  # To avoid division by zero

    for skill, count in details.get("soft_skill_counts", {}).items():
        if skill not in normalized_data:
            normalized_data[skill] = [0] * len(years)  # Initialize with zeros

        # Get the index of the current year and update the normalized value
        year_index = years.index(year)
        normalized_value = (count / total_posts) * 100
        normalized_data[skill][year_index] = normalized_value

# Plotting
plt.figure(figsize=(12, 8))
for skill, values in normalized_data.items():
    plt.plot(years, values, marker='o', label=skill)

plt.title("Normalized Soft Skills as a Percentage of Job Posts (v9.1)")
plt.xlabel("Year")
plt.ylabel("Percentage of Job Posts (%)")
plt.legend(title="Soft Skill Categories", loc='best')
plt.grid(True)

# Save the plot
output_file = f"{output_folder}\\Normalized_Soft_Skills_v9.1.png"
plt.savefig(output_file)
plt.show()

print(f"Figure saved to {output_file}")
