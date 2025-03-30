import json
import pandas as pd
import matplotlib.pyplot as plt

# Load data
json_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Soft_Skill_Occurrences_v9.1_Yearly_OncePerPost.json"
output_path = r"C:\Users\negin\YC-Job-Analytics\Result_YC\March 2025\Top3_Soft_Skills_v91_OncePerPost.png"

with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract and normalize
years = sorted(data.keys())
categories = list(data[years[0]]["soft_skill_counts"].keys())
normalized_counts = {category: [] for category in categories}

for year in years:
    total_posts = data[year]["total_job_posts"]
    for category in categories:
        count = data[year]["soft_skill_counts"].get(category, 0)
        percentage = (count / total_posts) * 100 if total_posts > 0 else 0
        normalized_counts[category].append(percentage)

# DataFrame
df_normalized = pd.DataFrame(normalized_counts, index=years)

# Top 3 skills by average
top_3 = df_normalized.mean().sort_values(ascending=False).head(3)

# Plot
plt.figure(figsize=(14, 8))
colors = ['#1f77b4', '#8c564b', '#17becf']  # Blue, brown, cyan

for i, category in enumerate(top_3.index):
    plt.plot(
        df_normalized.index,
        df_normalized[category],
        label=category,
        color=colors[i],
        marker='o',
        linewidth=2.5,
        markersize=6
    )

# Title
plt.text(
    0.5, 1.08,
    "Top Three Once-Per-Post Normalized Mentions of Soft Skills (v9.1) in AI Job Posts by Year",
    fontsize=15,
    fontweight='bold',
    color='navy',
    ha='center',
    transform=plt.gca().transAxes
)

# Axis labels & styling
plt.xlabel("Year", fontsize=13)
plt.ylabel("Percentage of Job Posts Mentioning Skill (%)", fontsize=13)
plt.xticks(rotation=45, fontsize=11)
plt.yticks(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# Legend
plt.legend(
    title="Top 3 Skill Categories",
    title_fontsize=11,
    fontsize=10,
    loc='upper right',
    bbox_to_anchor=(0.95, 0.95)
)

plt.tight_layout()

# Save the figure
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Figure saved to: {output_path}")
