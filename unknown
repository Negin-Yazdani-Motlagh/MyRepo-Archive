import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File path to the JSON data
input_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\v8\categorized_soft_skills_by_headcategory.json'
output_plot_file = r'C:\Users\negin\YC-Job-Analytics\Result_YC\normalized_headcategories_trends.png'

# Load the JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare data for analysis
time_series_data = []
total_job_posts_per_year = {}

# Extract job posts per year
for year, months in data.items():
    if year.isdigit():  # Only process numeric years
        # Sum numJobPost across all months
        total_job_posts_per_year[int(year)] = sum(
            month_data.get("numJobPost", 0) for month_data in months.values() if isinstance(month_data, dict)
        )

        # Extract headcategory mentions
        for month, categories in months.items():
            if isinstance(categories, dict):  # Ensure it's a valid dictionary
                for headcategory, count in categories.items():
                    if headcategory != "numJobPost":  # Exclude job post count
                        time_series_data.append({
                            "Year": int(year),
                            "Headcategory": headcategory,
                            "Count": count
                        })

# Convert extracted data into a DataFrame
df = pd.DataFrame(time_series_data)

# Aggregate mentions of each headcategory per year
agg_df = df.groupby(['Year', 'Headcategory']).agg({'Count': 'sum'}).reset_index()

# Convert total job posts per year to a DataFrame
job_post_counts = pd.DataFrame(list(total_job_posts_per_year.items()), columns=["Year", "TotalJobPosts"])

# Merge with the aggregated dataset
agg_df = pd.merge(agg_df, job_post_counts, on='Year', how="left")

# Ensure no division by zero
agg_df['TotalJobPosts'] = agg_df['TotalJobPosts'].replace(0, 1)  

# Normalize counts (Convert to percentage)
agg_df['NormalizedCount'] = (agg_df['Count'] / agg_df['TotalJobPosts']) * 100  # Fixed scaling

# Debugging: Check data before plotting
print("Total Job Posts Per Year:", total_job_posts_per_year)
print(agg_df.head())

# Plot normalized trends
plt.figure(figsize=(16, 10))
sns.lineplot(data=agg_df, x='Year', y='NormalizedCount', hue='Headcategory', palette='tab10')

# Configure the plot
plt.title("Normalized Trends of Headcategories Over Years", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Percentage of Mentions (%)", fontsize=12)  # Fixed y-axis label
plt.legend(title="Headcategories", fontsize=10, title_fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig(output_plot_file)
plt.show()

print(f"Plot saved to: {output_plot_file}")
