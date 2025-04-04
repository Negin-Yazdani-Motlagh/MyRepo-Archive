import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

def safe_str(value):
    if pd.isna(value):
        return ""
    return str(value).lower()

def load_dictionary11():
    # Load Dictionary 11
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (11).xlsx")
    
    print("Loading Dictionary 11...")
    df = pd.read_excel(excel_path)
    
    # Create a dictionary to store skills by category
    skills_dict = {}
    category_counts = {}  # To store number of subcategories per category
    
    for _, row in df.iterrows():
        category = row['Headcategory']
        subcategory = safe_str(row['Subcategory'])
        if category not in skills_dict:
            skills_dict[category] = []
            category_counts[category] = 0
        if subcategory:  # Only add non-empty subcategories
            skills_dict[category].append(subcategory)
            category_counts[category] += 1
    
    return skills_dict, category_counts

def analyze_yearly_posts():
    # Load Dictionary 11
    skills_dict, category_counts = load_dictionary11()
    
    # Load yearly job posts
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(workspace_dir, "JSON", "Yearly_Job_Posts.json")
    
    print("\nLoading Yearly Job Posts...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        yearly_data = data.get('YC', {})
    
    # Initialize results dictionary
    results = {}
    yearly_summary = {}  # Dictionary for yearly summaries
    normalized_summary = {}  # Dictionary for normalized values
    
    # Process each year
    for year in tqdm(yearly_data.keys(), desc="Processing years"):
        # Get all job posts for the year
        year_posts = yearly_data[year].get('comments', [])
        total_posts = len(year_posts)
        
        # Initialize year data
        results[year] = {
            "total_posts": total_posts,
            "categories": {}
        }
        
        yearly_summary[year] = {
            "total_posts": total_posts,
            "categories": {}
        }
        
        normalized_summary[year] = {
            "total_posts": total_posts,
            "categories": {}
        }
        
        # Initialize counters for each category
        for category in skills_dict:
            results[year]["categories"][category] = {
                "subcategories": {},
                "total_mentions": 0,
                "num_subcategories": category_counts[category]
            }
        
        # Process posts in batches
        batch_size = 1000
        for i in range(0, len(year_posts), batch_size):
            batch = year_posts[i:i + batch_size]
            batch_lower = [post.lower() for post in batch]
            
            # Check each category and its subcategories
            for category, subcategories in skills_dict.items():
                for subcategory in subcategories:
                    # Count occurrences in this batch
                    count = sum(1 for post in batch_lower if subcategory in post)
                    
                    # Update counts
                    if count > 0:
                        if subcategory not in results[year]["categories"][category]["subcategories"]:
                            results[year]["categories"][category]["subcategories"][subcategory] = 0
                        results[year]["categories"][category]["subcategories"][subcategory] += count
                        results[year]["categories"][category]["total_mentions"] += count
        
        # Create simplified yearly summary for each category
        for category in skills_dict:
            category_data = results[year]["categories"][category]
            total_mentions = category_data["total_mentions"]
            yearly_summary[year]["categories"][category] = total_mentions
            
            # Calculate normalized value (percentage of total posts)
            normalized_value = (total_mentions / total_posts) * 100 if total_posts > 0 else 0
            normalized_summary[year]["categories"][category] = normalized_value
    
    # Save results
    output_path = os.path.join(workspace_dir, "JSON", "yearly_skills_dict11_summary.json")
    print(f"\nSaving results to {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(yearly_summary, f, indent=2)
    
    # Save normalized results
    normalized_path = os.path.join(workspace_dir, "JSON", "yearly_skills_dict11_normalized.json")
    print(f"Saving normalized results to {normalized_path}")
    with open(normalized_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_summary, f, indent=2)
    
    # Create visualization
    create_visualization(normalized_summary, workspace_dir)
    
    # Print sample of the structure
    print("\nSample of normalized yearly summary structure:")
    print("===========================================")
    sample_year = list(normalized_summary.keys())[0]
    print(f"\nYear {sample_year}:")
    print(f"Total posts: {normalized_summary[sample_year]['total_posts']}")
    print("\nCategory percentages:")
    for category, percentage in normalized_summary[sample_year]["categories"].items():
        print(f"  - {category}: {percentage:.2f}%")

def create_visualization(normalized_summary, workspace_dir):
    # Prepare data for plotting
    years = sorted(normalized_summary.keys())
    categories = list(next(iter(normalized_summary.values()))["categories"].keys())
    
    # Create figure
    plt.figure(figsize=(15, 8))
    
    # Plot each category
    for category in categories:
        values = [normalized_summary[year]["categories"][category] for year in years]
        plt.plot(years, values, marker='o', label=category)
    
    # Customize plot
    plt.title('Normalized Skill Mentions Over Time (Percentage of Total Posts)', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Percentage of Posts (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(workspace_dir, "JSON", "dict11_skill_trends_normalized.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved visualization to {plot_path}")

if __name__ == "__main__":
    analyze_yearly_posts() 
