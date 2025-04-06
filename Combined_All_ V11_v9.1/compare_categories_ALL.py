import os
import pandas as pd
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def load_dict91_skills():
    # Load Dictionary 9.1 ALL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(os.path.dirname(script_dir), 
                             "Dictionary_9.1_ All", "Dictionary of soft skills (9.1).xlsx")
    
    print("Loading Dictionary 9.1 ALL...")
    print(f"Excel file path: {excel_path}")
    df = pd.read_excel(excel_path)
    
    # Create a dictionary to store skills by category
    skills_dict = {}
    for _, row in df.iterrows():
        category = row['Headcategory']
        subcategory = str(row['Subcategory']).lower() if pd.notna(row['Subcategory']) else None
        if subcategory:
            if category not in skills_dict:
                skills_dict[category] = []
            skills_dict[category].append(subcategory)
    
    return skills_dict

def load_dict11_skills():
    # Load Dictionary 11 All
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(os.path.dirname(script_dir), 
                             "Dictionary_11_All", "Dictionary of soft skills (11).xlsx")
    
    print("Loading Dictionary 11 All...")
    print(f"Excel file path: {excel_path}")
    df = pd.read_excel(excel_path)
    
    # Create a dictionary to store skills by category
    skills_dict = {}
    for _, row in df.iterrows():
        category = row['Headcategory']
        subcategory = str(row['Subcategory']).lower() if pd.notna(row['Subcategory']) else None
        if subcategory:
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

def analyze_job_posts():
    # Load both dictionaries
    dict91_skills = load_dict91_skills()
    dict11_skills = load_dict11_skills()
    
    # Get the path to the JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "JSON", "Yearly_Job_Posts.json")
    
    print(f"\nAnalyzing JSON file: {json_path}")
    
    # Load the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the YC data which contains all years
    yc_data = data['YC']
    
    # Initialize results dictionary
    results = {
        'dict91_combined': {},
        'dict11_interpersonal': {}
    }
    
    # Process each year (excluding 2011 and 2025)
    years = sorted(year for year in yc_data.keys() if year.isdigit() and year not in ['2011', '2025'])
    for year in years:
        print(f"\nProcessing year {year}...")
        year_data = yc_data[year]
        comments = year_data['comments']
        
        # Initialize year data with total posts and empty categories
        results['dict91_combined'][year] = {
            'total_posts': year_data['total_job_posts'],
            'count': 0
        }
        results['dict11_interpersonal'][year] = {
            'total_posts': year_data['total_job_posts'],
            'count': 0
        }
        
        # Process each comment
        if isinstance(comments, list):
            for comment in comments:
                # Count for Dictionary 9.1 combined categories
                dict91_counts = count_skills_in_text(comment, dict91_skills)
                for category in ['Communication Skills', 'Collaboration and Team Dynamics', 'Customer Service']:
                    if category in dict91_counts:
                        results['dict91_combined'][year]['count'] += sum(dict91_counts[category].values())
                
                # Count for Dictionary 11 Interpersonal Skills
                dict11_counts = count_skills_in_text(comment, dict11_skills)
                if 'Interpersonal & Leadership Skills' in dict11_counts:
                    results['dict11_interpersonal'][year]['count'] += sum(dict11_counts['Interpersonal & Leadership Skills'].values())
    
    # Save results to JSON
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "combined_categories_ALL.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    
    # Prepare data for plotting
    years_list = sorted(years)
    
    # Create normalized data for plotting
    dict91_normalized = []
    dict11_normalized = []
    
    for year in years_list:
        # Dictionary 9.1 combined categories
        dict91_normalized.append(results['dict91_combined'][year]['count'] / results['dict91_combined'][year]['total_posts'])
        # Dictionary 11 Interpersonal Skills
        dict11_normalized.append(results['dict11_interpersonal'][year]['count'] / results['dict11_interpersonal'][year]['total_posts'])
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Define colors and line styles
    colors = ['#1f77b4', '#8c564b']  # Specified colors
    line_styles = ['-', '--']  # Different line styles
    
    # Plot both categories
    plt.plot(years_list, dict91_normalized, 
            marker='o',  # Add markers for exact data points
            label='Dictionary 9.1 ALL (Communication + Collaboration + Customer Service)', 
            color=colors[0], 
            linestyle=line_styles[0],
            linewidth=2, 
            markersize=8)
    
    plt.plot(years_list, dict11_normalized, 
            marker='o',  # Add markers for exact data points
            label='Dictionary 11 All (Interpersonal & Leadership Skills)', 
            color=colors[1], 
            linestyle=line_styles[1],
            linewidth=2, 
            markersize=8)
    
    plt.title('Comparison of Combined Categories (ALL)\n(Exact Occurrences / Total Posts for Each Year)', 
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
    plot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "combined_categories_ALL_comparison.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {plot_path}")
    plt.close()
    
    # Print summary of normalized values
    print("\nNormalized values for each year:")
    for year, dict91_val, dict11_val in zip(years_list, dict91_normalized, dict11_normalized):
        print(f"\nYear {year}:")
        print(f"Dictionary 9.1 ALL Combined: {dict91_val:.3f}")
        print(f"Dictionary 11 All Interpersonal: {dict11_val:.3f}")

if __name__ == "__main__":
    analyze_job_posts() 
