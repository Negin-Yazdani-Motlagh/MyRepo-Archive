import json
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Load the JSON data
file_path = r'C:\Users\negin\soft_skills_analysis.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Step 1: Aggregate soft skill counts by date
soft_skills_trends = defaultdict(lambda: defaultdict(int))  # {soft_skill: {date: count}}

for period, details in data["YC"].items():
    try:
        # Parse the date (e.g., "April-2012") to a datetime object
        date = datetime.strptime(period, "%B-%Y")
        for skill, count in details.items():
            if skill != "numJobPost":  # Exclude "numJobPost" from skill counts
                soft_skills_trends[skill][date] += count
    except ValueError:
        print(f"Skipping invalid period format: {period}")

# Step 2: Create combined chart for all soft skills
combined_trend = defaultdict(int)

for skill, trends in soft_skills_trends.items():
    for date, count in trends.items():
        combined_trend[date] += count

# Sort combined data by date
sorted_combined_dates = sorted(combined_trend.keys())
sorted_combined_counts = [combined_trend[date] for date in sorted_combined_dates]

# Plot combined chart
plt.figure(figsize=(18, 9))
plt.plot(sorted_combined_dates, sorted_combined_counts, marker='o', linestyle='-', linewidth=2, color='skyblue', label="Total Soft Skills")
plt.title("Combined Trend of All Soft Skills Over Time", fontsize=16)
plt.xlabel("Date (Month and Year)", fontsize=12)
plt.ylabel("Total Mentions of Soft Skills", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45, fontsize=10)
plt.tight_layout()
plt.legend()
plt.savefig("combined_soft_skills_trend.png")
plt.show()

# Step 3: Create individual charts for each soft skill
for skill, trends in soft_skills_trends.items():
    # Sort data for each skill
    sorted_dates = sorted(trends.keys())
    sorted_counts = [trends[date] for date in sorted_dates]

    # Plot individual chart
    plt.figure(figsize=(18, 9))
    plt.plot(sorted_dates, sorted_counts, marker='o', linestyle='-', linewidth=2, label=f"{skill}")
    plt.title(f"Trend of '{skill}' Over Time", fontsize=16)
    plt.xlabel("Date (Month and Year)", fontsize=12)
    plt.ylabel(f"Mentions of {skill}", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"trend_{skill.replace(' ', '_')}.png")  # Save each chart with the skill name
    plt.show()
