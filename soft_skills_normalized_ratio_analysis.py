import json
import matplotlib.pyplot as plt
from datetime import datetime

# File paths
input_file = r'C:\Users\negin\soft_skills_analysis.json'
output_chart_file = r'C:\Users\negin\soft_skills_normalized_ratio.png'

# Load the processed JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize data structures
dates = []
ratios = []

# Iterate through each month-year in the data
for month_year, details in data["YC"].items():
    try:
        # Skip specific invalid entries
        if month_year in ["help-refugees", "who is hiring now"]:
            continue

        # Convert "Month-Year" format to "YYYY-MM"
        date = datetime.strptime(month_year, "%B-%Y")
        
        # Total job posts
        total_job_posts = details.get("numJobPost", 0)
        
        # Count of job posts mentioning at least one soft skill
        job_posts_with_soft_skills = sum(1 for skill, count in details.items() if skill != "numJobPost" and count > 0)
        
        # Calculate the ratio
        if total_job_posts > 0:
            ratio = job_posts_with_soft_skills / total_job_posts
            dates.append(date)
            ratios.append(ratio)

    except Exception as e:
        print(f"Skipping invalid entry for '{month_year}': {e}")

# Ensure there is data to plot
if dates and ratios:
    # Sort the data by date
    sorted_dates, sorted_ratios = zip(*sorted(zip(dates, ratios)))

    # Plot the new ratio over time
    plt.figure(figsize=(18, 9))
    plt.plot(sorted_dates, sorted_ratios, marker='o', linestyle='-', linewidth=2, color='skyblue')
    plt.title("Proportion of Job Posts Mentioning at Least One Soft Skill Over Time", fontsize=16)
    plt.xlabel("Date (Month and Year)", fontsize=14)
    plt.ylabel("Normalized Ratio (Job Posts with Soft Skills / Total Job Posts)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(sorted_dates, [date.strftime("%b %Y") for date in sorted_dates], rotation=90, fontsize=10)
    plt.tight_layout()

    # Save the chart
    plt.savefig(output_chart_file, bbox_inches="tight")
    plt.show()

    print(f"Chart saved to {output_chart_file}")
else:
    print("No valid data available to plot.")
