import json
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Load the JSON data
file_path = r'C:\Users\negin\soft_skills_analysis.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize data structures
dates = []
ratios = []

# Step 1: Calculate the total number of soft skill mentions and the ratio for each period
for period, details in data["YC"].items():
    try:
        # Parse the date (e.g., "April-2012") to a datetime object
        date = datetime.strptime(period, "%B-%Y")
        
        # Total job posts
        total_job_posts = details.get("numJobPost", 0)
        
        # Total mentions of soft skills
        total_soft_skill_mentions = sum(count for skill, count in details.items() if skill != "numJobPost")
        
        # Calculate ratio (avoid division by zero)
        if total_job_posts > 0:
            ratio = total_soft_skill_mentions / total_job_posts
            dates.append(date)
            ratios.append(ratio)
    except ValueError:
        print(f"Skipping invalid period format: {period}")

# Step 2: Sort data by date
if dates and ratios:
    sorted_dates, sorted_ratios = zip(*sorted(zip(dates, ratios)))

    # Step 3: Plot the ratio over time
    plt.figure(figsize=(24, 10))  # Increase figure size for better readability
    plt.plot(sorted_dates, sorted_ratios, marker='o', linestyle='-', linewidth=2, color='skyblue')
    plt.title("Ratio of Job Posts Mentioning Soft Skills to Total Job Posts Over Time", fontsize=20)
    plt.xlabel("Date (Month and Year)", fontsize=14)
    plt.ylabel("Ratio (Soft Skills / Total Job Posts)", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Add all months and years to the x-axis
    x_labels = [date.strftime("%b %Y") for date in sorted_dates]  # Format as "Mon Year" (e.g., "Apr 2012")
    plt.xticks(sorted_dates, x_labels, rotation=90, fontsize=10)  # Rotate labels at 90 degrees for better readability

    # Save the chart
    output_file = r'C:\Users\negin\soft_skills_ratio_trend_all_months.png'
    plt.savefig(output_file, bbox_inches="tight")  # Save with bounding box to fit all content

    # Show the chart
    plt.show()

    print(f"The chart has been saved to: {output_file}")
else:
    print("No data available to plot.")
