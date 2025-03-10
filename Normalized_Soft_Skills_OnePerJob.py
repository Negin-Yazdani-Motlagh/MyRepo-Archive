import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# File paths
json_file_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Headcategory_Counts_OnePerJob_V10.json"
output_image_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\February 2025\Normalized_Soft_Skills_OnePerJob.png"

# Load JSON data
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

monthly_data = data["HeadcategoryCountsByDate"]

# Extract headcategories dynamically
categories = set()
for month in monthly_data.values():
    categories.update(month.keys())
categories.discard("numJobPost")  # Remove total job posts from the list

# Normalize data into percentages
records = []
for month_key, counts in monthly_data.items():
    total_posts = counts.get("numJobPost", 1)  # Avoid division by zero
    date_str = month_key.lower().replace("ask hn who is hiring ", "").title()
    
    try:
        date_obj = pd.to_datetime(date_str, format="%B %Y")
    except ValueError:
        continue

    record = {"Date": date_obj}
    for category in categories:
        record[category] = (counts.get(category, 0) / total_posts) * 100

    records.append(record)

# Convert records to DataFrame and sort by Date
df = pd.DataFrame(records).sort_values("Date")

# Plotting
plt.figure(figsize=(14, 8))
for category in categories:
    plt.plot(df["Date"], df[category], label=category)

plt.xlabel('Year')
plt.ylabel('Percentage (%)')
plt.title('Normalized Soft Skill Categories (One Per Job) as a Percentage of Job Postings (2011-2025)')
plt.grid(True, linestyle='--', alpha=0.6)

# Format x-axis with monthly ticks
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)

# Move legend outside the plot area
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))A

plt.tight_layout()

# Save the plot image
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Plot saved successfully at: {output_image_path}")
