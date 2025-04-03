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
    excel_path = os.path.join(script_dir, "count_11_filtered.xlsx")
    json_path = os.path.join(workspace_dir, "JSON", "Filtered_Job_Posts.json")
    
    print("Loading Excel file...")
    df = pd.read_excel(excel_path)
    
    # Filter out 'motivated' and 'responsibility' subcategories
    df['Subcategory_lower'] = df['Subcategory'].apply(safe_str)
    df = df[~df['Subcategory_lower'].isin(['motivated', 'responsibility'])]
    
    print("Loading JSON file...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize yearly counts dictionary
    yearly_counts = {}
    total_posts_by_year = {}
    
    # Convert subcategories to lowercase for case-insensitive matching
    subcategories = df['Subcategory'].apply(safe_str).values
    headcategories = df['Headcategory'].unique()
    
    print(f"Found {len(headcategories)} headcategories: {headcategories}")
    
    # Initialize counts for each headcategory and year
    for year in data['YC']:
        year_int = int(year)
        if year_int in [2011, 2025]:  # Skip 2011 and 2025
            continue
        yearly_counts[year_int] = {headcategory: 0 for headcategory in headcategories}
        total_posts_by_year[year_int] = len(data['YC'][year]['comments'])
    
    print(f"\nProcessing years: {sorted(yearly_counts.keys())}")
    
    # Process each year's comments
    for year in data['YC']:
        year_int = int(year)
        if year_int in [2011, 2025]:  # Skip 2011 and 2025
            continue
        print(f"\nProcessing year {year}...")
        comments = data['YC'][year]['comments']
        print(f"Total comments for year {year}: {len(comments)}")
        
        # Process in batches
        batch_size = 1000
        for i in tqdm(range(0, len(comments), batch_size)):
            batch = comments[i:i + batch_size]
            batch_lower = [comment.lower() for comment in batch]
            
            # Count occurrences for each subcategory
            for j, subcategory in enumerate(subcategories):
                if subcategory:
                    headcategory = df.iloc[j]['Headcategory']
                    matches = sum(1 for comment in batch_lower if subcategory in comment)
                    yearly_counts[year_int][headcategory] += matches
    
    return yearly_counts, total_posts_by_year, script_dir

def create_smooth_plot(yearly_counts, total_posts_by_year, script_dir):
    # Convert to DataFrame for easier plotting
    years = sorted(yearly_counts.keys())
    headcategories = list(yearly_counts[years[0]].keys())
    
    # Create DataFrame with normalized percentages
    plot_data = []
    for year in years:
        total_posts = total_posts_by_year[year]
        for headcategory in headcategories:
            count = yearly_counts[year][headcategory]
            percentage = (count / total_posts) * 100 if total_posts > 0 else 0
            plot_data.append({
                'Year': year,
                'Headcategory': headcategory,
                'Percentage': percentage
            })
    
    df_plot = pd.DataFrame(plot_data)
    
    # Create the plot with specific dimensions
    plt.figure(figsize=(12, 6))
    
    # Set style with light gray dotted grid
    plt.grid(True, linestyle=':', color='#E0E0E0', alpha=0.6)
    plt.gca().set_axisbelow(True)
    
    # Define colors and line styles for each headcategory
    styles = {
        "Interpersonal & Leadership Skills": {
            'color': '#1f77b4',  # Blue
            'linestyle': 'none',
            'marker': 'o',
            'markersize': 6
        },
        "Personal Effectiveness & Growth": {
            'color': '#8c564b',  # Brown
            'linestyle': 'none',
            'marker': 'o',
            'markersize': 6
        },
        "conceptual/thinking skills": {
            'color': '#17becf',  # Cyan
            'linestyle': 'none',
            'marker': 'o',
            'markersize': 6
        }
    }
    
    # Plot each headcategory
    for headcategory in headcategories:
        category_data = df_plot[df_plot['Headcategory'] == headcategory].sort_values('Year')
        style = styles[headcategory]
        
        # First plot the markers
        plt.plot(category_data['Year'], category_data['Percentage'],
                label=headcategory,
                color=style['color'],
                linestyle=style['linestyle'],
                marker=style['marker'],
                markersize=style['markersize'],
                markerfacecolor='white',
                markeredgewidth=1.5,
                markeredgecolor=style['color'],
                zorder=2)  # Ensure markers are on top
        
        # Then plot the lines with appropriate style
        if headcategory == "conceptual/thinking skills":
            plt.plot(category_data['Year'], category_data['Percentage'],
                    color=style['color'],
                    linestyle=':',  # Dotted line
                    linewidth=4,  # Increased thickness
                    zorder=1)
        elif headcategory == "Personal Effectiveness & Growth":
            plt.plot(category_data['Year'], category_data['Percentage'],
                    color=style['color'],
                    linestyle='--',  # Dashed line
                    linewidth=4,  # Increased thickness
                    zorder=1)
        else:  # Interpersonal & Leadership Skills
            plt.plot(category_data['Year'], category_data['Percentage'],
                    color=style['color'],
                    linestyle='-',  # Solid line
                    linewidth=4,  # Increased thickness
                    zorder=1)
    
    # Customize plot
    plt.title('Normalized Skill Category Trends', fontsize=12, pad=20)
    plt.xlabel('Year', fontsize=10)
    plt.ylabel('Mentions per Job Post (%)', fontsize=10)
    
    # Create custom legend with combined markers and line styles
    legend_elements = []
    for headcategory in headcategories:
        style = styles[headcategory]
        # Create combined line and marker for each category
        if headcategory == "conceptual/thinking skills":
            line = plt.Line2D([0], [0], 
                          color=style['color'],
                          marker=style['marker'],
                          markersize=style['markersize'],
                          markerfacecolor='white',
                          markeredgewidth=1.5,
                          markeredgecolor=style['color'],
                          linestyle=':',  # Dotted
                          linewidth=4,
                          label=headcategory)
        elif headcategory == "Personal Effectiveness & Growth":
            line = plt.Line2D([0], [0], 
                          color=style['color'],
                          marker=style['marker'],
                          markersize=style['markersize'],
                          markerfacecolor='white',
                          markeredgewidth=1.5,
                          markeredgecolor=style['color'],
                          linestyle='--',  # Dashed
                          linewidth=4,
                          label=headcategory)
        else:  # Interpersonal & Leadership Skills
            line = plt.Line2D([0], [0], 
                          color=style['color'],
                          marker=style['marker'],
                          markersize=style['markersize'],
                          markerfacecolor='white',
                          markeredgewidth=1.5,
                          markeredgecolor=style['color'],
                          linestyle='-',  # Solid
                          linewidth=4,
                          label=headcategory)
        legend_elements.append(line)
    
    # Position legend inside the plot in the upper right
    plt.legend(handles=legend_elements,
              bbox_to_anchor=(1.02, 0.98),
              loc='upper right',
              frameon=True,
              framealpha=0.9,
              edgecolor='none',
              facecolor='white',
              ncol=1)  # Single column layout
    
    # Set axis limits and ticks
    plt.ylim(0, 30)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))
    
    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot
    output_path = os.path.join(script_dir, "skills_trends_normalized_11_filtered.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as: {output_path}")
    plt.close()

def main():
    yearly_counts, total_posts_by_year, script_dir = count_yearly_occurrences()
    create_smooth_plot(yearly_counts, total_posts_by_year, script_dir)

if __name__ == "__main__":
    main() 
