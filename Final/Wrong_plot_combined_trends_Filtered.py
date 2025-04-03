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

def get_customer_service_trend():
    # Set up correct file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "count_11_filtered.xlsx")
    json_path = os.path.join(os.path.dirname(script_dir), "JSON", "Filtered_Job_Posts.json")
    
    print("Loading Excel file for Customer Service...")
    df = pd.read_excel(excel_path)
    
   
    df['Subcategory_lower'] = df['Subcategory'].apply(safe_str)
    df = df[~df['Subcategory_lower'].isin(['motivated', 'responsibility'])]
    
    print("Loading JSON file...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize yearly counts
    yearly_counts = {}
    total_posts_by_year = {}
    
    # Get subcategories for Customer Service
    subcategories = df[df['Headcategory'] == 'Customer Service']['Subcategory'].apply(safe_str).values
    
    # Process each year
    for year in data['YC']:
        year_int = int(year)
        if year_int in [2011, 2025]:  # Skip 2011 and 2025
            continue
        comments = data['YC'][year]['comments']
        total_posts_by_year[year_int] = len(comments)
        matches = 0
        
        # Process in batches
        batch_size = 1000
        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            batch = [comment.lower() for comment in batch]
            
            for subcategory in subcategories:
                if subcategory:
                    matches += sum(1 for comment in batch if subcategory in comment)
        
        yearly_counts[year_int] = matches
    
    # Calculate percentages
    percentages = {year: (count / total_posts_by_year[year]) * 100 
                  for year, count in yearly_counts.items()}
    
    return percentages

def get_interpersonal_leadership_trend():
    # Load data from Dictionary 11
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "count_11_filtered.xlsx")
    json_path = os.path.join(os.path.dirname(script_dir), "JSON", "Filtered_Job_Posts.json")
    
    print("Loading Excel file for Interpersonal & Leadership Skills...")
    df = pd.read_excel(excel_path)
    
    # Filter out 'motivated' and 'responsibility' subcategories
    df['Subcategory_lower'] = df['Subcategory'].apply(safe_str)
    df = df[~df['Subcategory_lower'].isin(['motivated', 'responsibility'])]
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    yearly_counts = {}
    total_posts_by_year = {}
    
    # Get subcategories for Interpersonal & Leadership Skills
    subcategories = df[df['Headcategory'] == 'Interpersonal & Leadership Skills']['Subcategory'].apply(safe_str).values
    
    # Process each year
    for year in data['YC']:
        year_int = int(year)
        if year_int in [2011, 2025]:  # Skip 2011 and 2025
            continue
        comments = data['YC'][year]['comments']
        total_posts_by_year[year_int] = len(comments)
        matches = 0
        
        # Process in batches
        batch_size = 1000
        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            batch = [comment.lower() for comment in batch]
            
            for subcategory in subcategories:
                if subcategory:
                    matches += sum(1 for comment in batch if subcategory in comment)
        
        yearly_counts[year_int] = matches
    
    # Calculate percentages
    percentages = {year: (count / total_posts_by_year[year]) * 100 
                  for year, count in yearly_counts.items()}
    
    return percentages

def create_combined_plot():
    # Get data for all trends
    customer_service = get_customer_service_trend()
    interpersonal_leadership = get_interpersonal_leadership_trend()
    
    # Communication Skills data (excluding 2011 and 2025)
    communication_data = {
        2012: 6.8, 2013: 8.2, 2014: 12.1, 2015: 10.8,
        2016: 7.8, 2017: 7.5, 2018: 7.2, 2019: 7.8, 2020: 8.2,
        2021: 8.5, 2022: 9.1, 2023: 8.4, 2024: 9.2
    }
    
    # Collaboration data (excluding 2011 and 2025)
    collaboration_data = {
        2012: 2.8, 2013: 4.2, 2014: 6.8, 2015: 5.9,
        2016: 4.5, 2017: 4.4, 2018: 5.2, 2019: 6.0, 2020: 5.8,
        2021: 5.5, 2022: 5.2, 2023: 5.0, 2024: 5.1
    }
    
    # Combine all skills
    combined_skills = {}
    all_years = sorted(set(customer_service.keys()) | set(communication_data.keys()))
    
    for year in all_years:
        # Sum the percentages for each year
        combined_value = 0
        if year in communication_data:
            combined_value += communication_data[year]
        if year in collaboration_data:
            combined_value += collaboration_data[year]
        if year in customer_service:
            combined_value += customer_service[year]
        combined_skills[year] = combined_value
    
    # Create DataFrame for plotting
    plot_data = []
    
    # Add combined skills data
    for year in all_years:
        plot_data.append({
            'Year': year,
            'Skill': 'Combined Communication & Collaboration',
            'Percentage': combined_skills[year]
        })
        if year in interpersonal_leadership:
            plot_data.append({
                'Year': year,
                'Skill': 'Interpersonal & Leadership Skills',
                'Percentage': interpersonal_leadership[year]
            })
    
    df_plot = pd.DataFrame(plot_data)
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    sns.set_style("whitegrid")
    
    # Define colors
    colors = {
        'Combined Communication & Collaboration': '#e74c3c',  # Red
        'Interpersonal & Leadership Skills': '#3498db'  # Blue
    }
    
    # Plot each skill with smooth lines
    for skill in df_plot['Skill'].unique():
        skill_data = df_plot[df_plot['Skill'] == skill].sort_values('Year')
        
        # Create smooth line using rolling average
        smooth_data = skill_data.copy()
        smooth_data['Smooth_Percentage'] = smooth_data['Percentage'].rolling(window=2, min_periods=1).mean()
        
        # Then plot the lines with appropriate style
        if skill == 'Combined Communication & Collaboration':
            plt.plot(smooth_data['Year'], smooth_data['Smooth_Percentage'],
                    color=colors[skill],
                    linestyle=':',  # Dotted line
                    linewidth=4,  # Increased thickness
                    zorder=1)
        else:  # Interpersonal & Leadership Skills
            plt.plot(smooth_data['Year'], smooth_data['Smooth_Percentage'],
                    color=colors[skill],
                    linestyle='--',  # Dashed line
                    linewidth=4,  # Increased thickness
                    zorder=1)
    
    # Customize plot
    plt.title('Combined Communication & Collaboration vs Interpersonal & Leadership Skills', 
             fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Percentage of Job Posts', fontsize=12)
    
    # Create custom legend with combined markers and line styles
    legend_elements = []
    for skill in df_plot['Skill'].unique():
        style = {
            'color': colors[skill],
            'marker': 'o' if skill == 'Combined Communication & Collaboration' else 's',
            'markersize': 10,
            'label': skill
        }
        line = plt.Line2D([0], [0], 
                      color=style['color'],
                      marker=style['marker'],
                      markersize=style['markersize'],
                      markerfacecolor='white',
                      markeredgewidth=1.5,
                      markeredgecolor=style['color'],
                      linestyle=':' if skill == 'Combined Communication & Collaboration' else '--',
                      linewidth=4,
                      label=style['label'])
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
    plt.ylim(0, 32)  # Changed from 0.35 to 35 to match percentage scale
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))  # Remove % sign
    
    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "combined_communication_collaboration_vs_interpersonal_hardcoded.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as: {output_path}")
    
    # Print analysis results
    print("\nAnalysis Results:")
    print("================")
    for skill in df_plot['Skill'].unique():
        skill_data = df_plot[df_plot['Skill'] == skill]
        print(f"\n{skill}:")
        print(f"Average percentage: {skill_data['Percentage'].mean():.2f}%")
        print(f"Peak percentage: {skill_data['Percentage'].max():.2f}%")
        print("Recent trend (last 3 years):")
        recent_data = skill_data.nlargest(3, 'Year')
        for _, row in recent_data.iterrows():
            print(f"  {int(row['Year'])}: {row['Percentage']:.2f}%")

if __name__ == "__main__":
    create_combined_plot() 
