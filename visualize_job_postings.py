import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load the JSON data
file_path = r'C:\Users\negin\soft_skills_analysis.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract data for the chart
dates = []
job_post_counts = []

for period, details in data["YC"].items():
    try:
        # Parse the date (e.g., "April-2012") to a datetime object
        date = datetime.strptime(period, "%B-%Y")
        num_posts = details.get("numJobPost", 0)
        dates.append(date)
        job_post_counts.append(num_posts)
    except ValueError:
        print(f"Skipping invalid period format: {period}")

# Sort data by date
sorted_dates, sorted_counts = zip(*sorted(zip(dates, job_post_counts)))

# Create the line chart
plt.figure(figsize=(24, 10))  # Increase figure size for more space
plt.plot(sorted_dates, sorted_counts, marker='o', linestyle='-', linewidth=2, color='skyblue', label="Job Postings")
plt.title("Total Job Postings by Month and Year", fontsize=20)
plt.xlabel("Date (Month and Year)", fontsize=14)
plt.ylabel("Number of Job Postings", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Add detailed x-axis labels (include all months) and rotate them
x_labels = [date.strftime("%b %Y") for date in sorted_dates]  # Format as "Mon Year" (e.g., "Apr 2012")
plt.xticks(sorted_dates, x_labels, rotation=90, fontsize=10)  # Rotate at 90 degrees for better readability

# Add legend and layout adjustments
plt.tight_layout()
plt.legend()

# Save and show the chart
plt.savefig("job_postings_all_months_years.png")
plt.show()
