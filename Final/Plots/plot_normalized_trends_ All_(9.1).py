import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import os

def safe_str(value):
    if pd.isna(value):
        return ""
    return str(value).lower()

def count_yearly_occurrences():
    # Set up correct file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (9.1).xlsx")
    json_path = os.path.join(workspace_dir, "JSON", "Yearly_Job_Posts.json")
    
    print("Loading Excel file...")
    df = pd.read_excel(excel_path)
    
    print("Loading JSON file...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize yearly counts dictionary
    yearly_counts = {}
    total_posts_by_year = {}
    
    # Convert subcategories to lowercase for case-insensitive matching
    subcategories = df['Subcategory'].apply(safe_str).values
    headcategories = df['Headcategory'].unique()
    
    # Initialize counts for each headcategory and year
    for year in data['YC']:
        yearly_counts[year] = {headcategory: 0 for headcategory in headcategories}
        total_posts_by_year[year] = len(data['YC'][year]['comments'])
    
    # Process each year's comments
    for year in data['YC']:
        print(f"\nProcessing year {year}...")
        comments = data['YC'][year]['comments']
        
        # Process in batches
        batch_size = 1000
        for i in tqdm(range(0, len(comments), batch_size)):
            batch = comments[i:i + batch_size]
            batch = [comment.lower() for comment in batch]
            
            # Count occurrences for each subcategory
            for j, subcategory in enumerate(subcategories):
                if subcategory and subcategory not in ["responsible", "motivated"]:  # Skip these subcategories
                    headcategory = df.iloc[j]['Headcategory']
                    matches = [subcategory in comment for comment in batch]
                    yearly_counts[year][headcategory] += np.sum(matches)
    
    return yearly_counts, total_posts_by_year

def create_smooth_plot(yearly_counts, total_posts_by_year):
    # Convert to DataFrame for easier plotting
    years = sorted(yearly_counts.keys())
    headcategories = list(yearly_counts[years[0]].keys())
    
    # Create DataFrame with normalized percentages
    plot_data = []
    for year in years:
        total_posts = total_posts_by_year[year]
        for headcategory in headcategories:
            count = yearly_counts[year][headcategory]
            percentage = (count / total_posts) * 100
            plot_data.append({
                'Year': int(year),
                'Headcategory': headcategory,
                'Percentage': percentage
            })
    
    df_plot = pd.DataFrame(plot_data)
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Set style
    sns.set_style("whitegrid")
    
    # Plot each headcategory
    for headcategory in headcategories:
        category_data = df_plot[df_plot['Headcategory'] == headcategory]
        
        # Create smooth line using rolling average
        smooth_data = category_data.sort_values('Year')
        smooth_data['Smooth_Percentage'] = smooth_data['Percentage'].rolling(window=2, min_periods=1).mean()
        
        # Plot both original points and smooth line
        plt.plot(smooth_data['Year'], smooth_data['Smooth_Percentage'], 
                label=headcategory, linewidth=2)
        plt.scatter(smooth_data['Year'], smooth_data['Percentage'], 
                   alpha=0.3, s=30)
    
    # Customize plot
    plt.title('Normalized Skill Category Trends Over Time', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Percentage of Job Posts', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Format y-axis as percentage
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}%'))
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "skills_trends_normalized.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as: {output_path}")
    
    # Print analysis results
    print("\nAnalysis Results:")
    print("================")
    for headcategory in headcategories:
        total_occurrences = sum(yearly_counts[year][headcategory] for year in years)
        print(f"\n{headcategory}:")
        print(f"Total occurrences: {total_occurrences}")
        for year in years:
            percentage = (yearly_counts[year][headcategory] / total_posts_by_year[year]) * 100
            print(f"  {year}: {percentage:.1f}%")

if __name__ == "__main__":
    yearly_counts, total_posts_by_year = count_yearly_occurrences()
    create_smooth_plot(yearly_counts, total_posts_by_year) 
