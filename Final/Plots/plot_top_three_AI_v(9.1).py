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
    json_path = os.path.join(workspace_dir, "JSON", "Filtered_Job_Posts.json")
    
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

def create_top_three_plot(yearly_counts, total_posts_by_year):
    # Convert to DataFrame for easier plotting
    years = sorted(yearly_counts.keys())
    
    # Filter out years 2011 and 2025
    years = [year for year in years if int(year) not in [2011, 2025]]
    
    # Define top three categories
    top_three = [
        "Communication Skills",
        "Work Ethic and Professionalism",
        "Collaboration and Team Dynamics"
    ]
    
    # Create DataFrame with normalized percentages
    plot_data = []
    for year in years:
        total_posts = total_posts_by_year[year]
        for headcategory in top_three:
            count = yearly_counts[year][headcategory]
            percentage = (count / total_posts) * 100 if total_posts > 0 else 0
            plot_data.append({
                'Year': int(year),
                'Headcategory': headcategory,
                'Percentage': percentage
            })
    
    df_plot = pd.DataFrame(plot_data)
    
    print("\nPlot data summary:")
    print(df_plot.groupby('Headcategory')['Percentage'].describe())
    
    # Create the plot with specific dimensions
    plt.figure(figsize=(12, 6))
    
    # Set style with light gray dotted grid
    plt.grid(True, linestyle=':', color='#E0E0E0', alpha=0.6)
    plt.gca().set_axisbelow(True)
    
    # Define colors and line styles for each headcategory
    styles = {
        "Communication Skills": {
            'color': '#1f77b4',  # Blue
            'linestyle': 'none',
            'marker': 'o',
            'markersize': 6
        },
        "Work Ethic and Professionalism": {
            'color': '#8c564b',  # Brown
            'linestyle': 'none',
            'marker': 'o',
            'markersize': 6
        },
        "Collaboration and Team Dynamics": {
            'color': '#17becf',  # Cyan
            'linestyle': 'none',
            'marker': 'o',
            'markersize': 6
        }
    }
    
    # Plot each headcategory
    for headcategory in top_three:
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
        if headcategory == "Work Ethic and Professionalism":
            plt.plot(category_data['Year'], category_data['Percentage'],
                    color=style['color'],
                    linestyle=(0, (2, 2)),  # Dashed line
                    linewidth=3,  # Increased from 2 to 3
                    zorder=1)
        elif headcategory == "Collaboration and Team Dynamics":
            plt.plot(category_data['Year'], category_data['Percentage'],
                    color=style['color'],
                    linestyle=(0, (1, 1)),  # Dotted line
                    linewidth=3,  # Increased from 2 to 3
                    zorder=1)
        else:
            plt.plot(category_data['Year'], category_data['Percentage'],
                    color=style['color'],
                    linestyle='-',  # Solid line
                    linewidth=3,  # Increased from 2 to 3
                    zorder=1)
    
    # Customize plot
    plt.title('Top 3 Skill Categories', fontsize=12, pad=20)
    plt.xlabel('Year', fontsize=10)
    plt.ylabel('Mentions per Job Post (%)', fontsize=10)
    
    # Create custom legend with combined markers and line styles
    legend_elements = []
    for headcategory in top_three:
        style = styles[headcategory]
        # Create combined line and marker for each category
        if headcategory == "Work Ethic and Professionalism":
            line = plt.Line2D([0], [0], 
                          color=style['color'],
                          marker=style['marker'],
                          markersize=style['markersize'],
                          markerfacecolor='white',
                          markeredgewidth=1.5,
                          markeredgecolor=style['color'],
                          linestyle=(0, (2, 2)),  # Dashed
                          linewidth=4,
                          label=headcategory)
        elif headcategory == "Collaboration and Team Dynamics":
            line = plt.Line2D([0], [0], 
                          color=style['color'],
                          marker=style['marker'],
                          markersize=style['markersize'],
                          markerfacecolor='white',
                          markeredgewidth=1.5,
                          markeredgecolor=style['color'],
                          linestyle=(0, (1, 1)),  # Dotted
                          linewidth=4,
                          label=headcategory)
        else:
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
    plt.ylim(0, 15)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))
    
    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'top_three_skills_filtered.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {output_path}")
    plt.close()

def main():
    yearly_counts, total_posts_by_year = count_yearly_occurrences()
    create_top_three_plot(yearly_counts, total_posts_by_year)

if __name__ == "__main__":
    main() 
