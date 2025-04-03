import pandas as pd
import json
import numpy as np
from tqdm import tqdm
import os

def safe_str(value):
    if pd.isna(value):
        return ""
    return str(value).lower()

def count_occurrences():
    # Set up correct file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (11).xlsx")
    json_path = os.path.join(workspace_dir, "JSON", "Filtered_Job_Posts.json")
    
    print("Loading Excel file...")
    df = pd.read_excel(excel_path)
    
    print("Loading JSON file...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize counts array
    counts = np.zeros(len(df))
    
    # Convert subcategories to lowercase for case-insensitive matching
    subcategories = df['Subcategory'].apply(safe_str).values
    
    # Process each year's comments
    total_posts = 0
    for year in data['YC']:
        total_posts += len(data['YC'][year]['comments'])
    
    print(f"\nProcessing {total_posts} job posts...")
    
    # Process in batches for efficiency
    batch_size = 1000
    for year in data['YC']:
        comments = data['YC'][year]['comments']
        for i in tqdm(range(0, len(comments), batch_size), desc=f"Processing {year}"):
            batch = comments[i:i + batch_size]
            
            # Convert batch to lowercase
            batch = [comment.lower() for comment in batch]
            
            # Count occurrences for each subcategory
            for j, subcategory in enumerate(subcategories):
                if subcategory:  # Skip empty strings
                    # Count occurrences in batch
                    matches = [subcategory in comment for comment in batch]
                    counts[j] += np.sum(matches)
    
    # Add counts to dataframe
    df['count'] = counts
    
    # Save results
    output_file = os.path.join(script_dir, "count_11_filtered.xlsx")
    df.to_excel(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("==================")
    print(f"Total job posts processed: {total_posts}")
    print("\nTop 10 most frequent subcategories:")
    top_10 = df.nlargest(10, 'count')
    for _, row in top_10.iterrows():
        print(f"{row['Subcategory']}: {row['count']} occurrences")
    
    print("\nCounts by headcategory:")
    headcategory_counts = df.groupby('Headcategory')['count'].sum().sort_values(ascending=False)
    for headcategory, count in headcategory_counts.items():
        print(f"{headcategory}: {count} total occurrences")

if __name__ == "__main__":
    count_occurrences() 
