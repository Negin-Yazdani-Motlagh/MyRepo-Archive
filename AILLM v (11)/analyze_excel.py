import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def analyze_excel():
    # Load Dictionary 11 AILLM
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "Dictionary of soft skills (11).xlsx")
    
    print("Loading Dictionary 11 AILLM...")
    df = pd.read_excel(excel_path)
    
    # Count occurrences of each headcategory
    headcategory_counts = df['Headcategory'].value_counts()
    
    # Create a bar plot
    plt.figure(figsize=(12, 6))
    headcategory_counts.plot(kind='bar')
    plt.title('Number of Skills per Headcategory')
    plt.xlabel('Headcategory')
    plt.ylabel('Number of Skills')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(script_dir, "headcategory_distribution.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save counts to text file
    output_path = os.path.join(script_dir, "headcategory_counts.txt")
    with open(output_path, 'w') as f:
        f.write("Headcategory Counts:\n\n")
        for category, count in headcategory_counts.items():
            f.write(f"{count} - {category}\n")
    
    print(f"\nResults saved to: {output_path}")
    print(f"Plot saved to: {plot_path}")
    
    # Print summary
    print("\nHeadcategory Counts:")
    for category, count in headcategory_counts.items():
        print(f"{count} - {category}")

if __name__ == "__main__":
    analyze_excel() 
