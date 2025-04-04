import json
import os
import matplotlib.pyplot as plt

def load_and_combine_data():
    # Get workspace directory
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load Dictionary 9.1 data
    dict9_path = os.path.join(workspace_dir, "Dictionary_9.1_ All", "yearly_skills_summary_simplified.json")
    print("Loading Dictionary 9.1 data...")
    with open(dict9_path, 'r', encoding='utf-8') as f:
        dict9_data = json.load(f)
    
    # Load Dictionary 11 data
    dict11_path = os.path.join(workspace_dir, "Dictionary_11_All", "yearly_skills_dict11_summary.json")
    print("Loading Dictionary 11 data...")
    with open(dict11_path, 'r', encoding='utf-8') as f:
        dict11_data = json.load(f)
    
    # Prepare data for plotting
    years = sorted(dict9_data.keys())
    
    # Dictionary 9.1 combined line (Communication + Collaboration + Customer Service)
    dict9_combined = []
    for year in years:
        total = (
            dict9_data[year]["categories"]["Communication Skills"] +
            dict9_data[year]["categories"]["Collaboration and Team Dynamics"] +
            dict9_data[year]["categories"]["Customer Service and Client Management"]
        )
        # Normalize by total posts
        normalized = (total / dict9_data[year]["total_posts"]) * 100
        dict9_combined.append(normalized)
    
    # Dictionary 11 Interpersonal & Leadership Skills line
    dict11_interpersonal = []
    for year in years:
        total = dict11_data[year]["categories"]["Interpersonal & Leadership Skills"]
        # Normalize by total posts
        normalized = (total / dict11_data[year]["total_posts"]) * 100
        dict11_interpersonal.append(normalized)
    
    return years, dict9_combined, dict11_interpersonal

def create_combined_plot(years, dict9_combined, dict11_interpersonal):
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot Dictionary 9.1 combined line
    plt.plot(years, dict9_combined, 
             marker='o', 
             color='red', 
             label='Dictionary 9.1: Communication + Collaboration + Customer Service')
    
    # Plot Dictionary 11 Interpersonal line
    plt.plot(years, dict11_interpersonal, 
             marker='s', 
             color='blue', 
             linestyle='--', 
             label='Dictionary 11: Interpersonal & Leadership Skills')
    
    # Customize plot
    plt.title('Comparison of Combined Skills vs Interpersonal Skills', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Percentage of Posts (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plot_path = os.path.join(workspace_dir, "JSON", "combined_vs_interpersonal_trends.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nSaved visualization to {plot_path}")

def main():
    # Load and combine data
    years, dict9_combined, dict11_interpersonal = load_and_combine_data()
    
    # Create and save plot
    create_combined_plot(years, dict9_combined, dict11_interpersonal)
    
    # Print sample data points
    print("\nSample data points (first year):")
    print(f"Year: {years[0]}")
    print(f"Dictionary 9.1 Combined: {dict9_combined[0]:.2f}%")
    print(f"Dictionary 11 Interpersonal: {dict11_interpersonal[0]:.2f}%")

if __name__ == "__main__":
    main() 
