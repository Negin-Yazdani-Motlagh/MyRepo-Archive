import json
import os
import pandas as pd
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from datetime import datetime

def load_skills_dictionary():
    # Load Dictionary 9.1 AILLM
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (9.1).xlsx")
    
    print("Loading Dictionary 9.1 AILLM...")
    df = pd.read_excel(excel_path)
    
    # Create a dictionary to store skills by category
    skills_dict = {}
    for _, row in df.iterrows():
        category = row['Headcategory']
        subcategory = str(row['Subcategory']).lower() if pd.notna(row['Subcategory']) else None
        # Skip entries containing 'responsible' or 'responsibility'
        if subcategory and 'responsible' not in subcategory and 'responsibility' not in subcategory:
            if category not in skills_dict:
                skills_dict[category] = []
            skills_dict[category].append(subcategory)
    
    return skills_dict

def count_skills_in_text(text, skills_dict):
    text = text.lower()
    skill_counts = defaultdict(lambda: defaultdict(int))
    
    for category, skills in skills_dict.items():
        for skill in skills:
            if skill in text:
                skill_counts[category][skill] += 1
    
    return skill_counts

def analyze_json_structure(data):
    """Analyze and print the structure of the JSON data"""
    if isinstance(data, dict):
        print("Dictionary with keys:", list(data.keys()))
        # Print structure of first item
        first_key = list(data.keys())[0]
        print(f"\nStructure of first item ({first_key}):")
        analyze_json_structure(data[first_key])
    elif isinstance(data, list):
        print("List with length:", len(data))
        if data:
            print("\nStructure of first list item:")
            analyze_json_structure(data[0])
    else:
        print("Value type:", type(data))

def analyze_job_posts():
    # Load skills dictionary
    skills_dict = load_skills_dictionary()
    
    # Get the path to the JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "JSON", "AI_ML_Job_Posts.json")
    
    print(f"\nAnalyzing JSON file: {json_path}")
    
    # Load the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the YC data which contains all years
    yc_data = data['YC']
    
    # Initialize results dictionary
    results = {}
    
    # Process each year (excluding 2011 and 2025)
    years = sorted(year for year in yc_data.keys() if year.isdigit() and year not in ['2011', '2025'])
    for year in years:
        print(f"\nProcessing year {year}...")
        year_data = yc_data[year]
        comments = year_data['comments']
        
        # Initialize year data with total posts and empty categories
        results[year] = {
            'total_posts': year_data['total_job_posts'],
            'categories': defaultdict(int)
        }
        
        # Process each comment
        if isinstance(comments, list):
            for comment in comments:
                skill_counts = count_skills_in_text(comment, skills_dict)
                for category, subcategories in skill_counts.items():
                    # Sum up all subcategory occurrences for the category
                    results[year]['categories'][category] += sum(subcategories.values())
    
    # Convert defaultdict to regular dict for JSON serialization
    for year in results:
        results[year]['categories'] = dict(results[year]['categories'])
    
    # Save results to JSON
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headcategory_occurrences.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    
    # Prepare data for plotting
    years_list = sorted(results.keys())
    categories = set()
    for year_data in results.values():
        categories.update(year_data['categories'].keys())
    categories = sorted(categories)
    
    # Create normalized data for plotting
    plot_data = {category: [] for category in categories}
    for year in years_list:
        total_posts = results[year]['total_posts']
        for category in categories:
            # Normalization formula: occurrences / total_posts for that specific year
            # This is NOT an average - it's the exact proportion for that year
            normalized_value = results[year]['categories'].get(category, 0) / total_posts
            plot_data[category].append(normalized_value)
            
        # Print normalized values for each year
        print(f"\nYear {year}:")
        print(f"Total job posts: {total_posts}")
        sorted_categories = sorted(
            [(cat, results[year]['categories'].get(cat, 0) / total_posts) 
             for cat in categories],
            key=lambda x: x[1],
            reverse=True
        )
        print("Normalized headcategory occurrences (occurrences/total posts for this year):")
        for category, norm_value in sorted_categories:
            print(f"{norm_value:.3f} - {category}")
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Define colors and line styles
    colors = ['#1f77b4', '#8c564b', '#17becf']  # Specified colors
    line_styles = ['-', '--', ':']  # Different line styles
    
    # Get top 3 categories based on average normalized values across all years
    # This is only used to select which categories to plot
    category_averages = {}
    for category in categories:
        category_averages[category] = sum(plot_data[category]) / len(plot_data[category])
    top_3_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)[:3]
    top_3_names = [cat[0] for cat in top_3_categories]
    
    # Plot only top 3 categories
    for category, color, line_style in zip(top_3_names, colors, line_styles):
        plt.plot(years_list, plot_data[category], 
                marker='o',  # Add markers for exact data points
                label=category, 
                color=color, 
                linestyle=line_style,
                linewidth=2, 
                markersize=8)
    
    plt.title('Top 3 Normalized Skill Category Trends Over Time\n(Exact Occurrences / Total Posts for Each Year)', 
              fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Normalized Occurrence', fontsize=12)
    plt.legend(loc='upper right', fontsize=10)  # Legend in upper right
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(years_list, rotation=45)
    
    # Format y-axis as percentages
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills_trends_normalized.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {plot_path}")
    plt.close()

if __name__ == "__main__":
    analyze_job_posts() 
